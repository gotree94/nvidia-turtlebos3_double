#!/usr/bin/env python3
"""
Digital Twin - Master Orchestrator

전체 디지털 트윈 루프를 통합 관리하는 중앙 오케스트레이터.
6단계 파이프라인의 모든 컴포넌트를 조율하고 자동화합니다.

Usage:
    # 전체 디지털 트윈 시작
    python3 src/digital_twin/orchestrator.py --start
    
    # 상태 확인
    python3 src/digital_twin/orchestrator.py --status
    
    # Web Dashboard 서버 모드
    python3 src/digital_twin/orchestrator.py --serve
"""

import os
import sys
import json
import time
import signal
import threading
import argparse
import subprocess
from datetime import datetime
from typing import Optional, Dict, List
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_logger import EpisodeDB, RealWorldDataLogger
from gap_analyzer import GapAnalyzer
from auto_retrain_pipeline import AutoRetrainPipeline
from policy_registry import PolicyRegistry


class DigitalTwinOrchestrator:
    """
    디지털 트윈 중앙 오케스트레이터
    
    모든 서브시스템을 통합 관리:
        - Data Logger: 실제 주행 데이터 수집
        - Gap Analyzer: Sim-vs-Real 성능 갭 분석
        - Retrain Pipeline: 자동 재학습
        - Policy Registry: 정책 버전 관리
        - Deployment: 블루-그린 배포
    
    상태 머신:
        IDLE → COLLECTING → ANALYZING → RETRAINING → DEPLOYING → MONITORING
          ↑                                                        │
          └────────────────────────────────────────────────────────┘
    """
    
    # 상태 상수
    STATE_IDLE = "idle"
    STATE_COLLECTING = "collecting"
    STATE_ANALYZING = "analyzing"
    STATE_RETRAINING = "retraining"
    STATE_DEPLOYING = "deploying"
    STATE_MONITORING = "monitoring"
    STATE_ERROR = "error"
    
    def __init__(self, config_path: str = "config/digital_twin_config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        
        # 상태
        self.state = self.STATE_IDLE
        self.state_lock = threading.Lock()
        self.running = False
        
        # 서브시스템
        self.registry = PolicyRegistry(
            self.config.get("registry_path", "config/policy_registry.json")
        )
        self.db = EpisodeDB(
            self.config.get("db_path", "data/episode_db.sqlite")
        )
        self.analyzer = GapAnalyzer(
            self.config.get("db_path", "data/episode_db.sqlite"),
            self.config.get("analyzer_config")
        )
        self.pipeline = AutoRetrainPipeline(
            workspace=self.config.get("workspace", "/workspace")
        )
        
        # 모니터링 데이터
        self.metrics_history: List[dict] = []
        self.current_cycle = 0
        self.last_cycle_time = None
        
        print(f'[Orchestrator] Initialized')
        print(f'  State: {self.state}')
        print(f'  Config: {config_path}')
    
    def _load_config(self) -> dict:
        """YAML/JSON 설정 로드"""
        default_config = {
            "workspace": os.path.abspath("."),
            "db_path": "data/episode_db.sqlite",
            "registry_path": "config/policy_registry.json",
            "analyzer_config": {
                "success_rate_gap_threshold": 0.15,
                "collision_rate_gap_threshold": 0.10,
                "min_episodes_for_analysis": 10,
                "window_size": 50,
            },
            "retrain_config": {
                "num_envs": 128,
                "max_iterations": 500,
                "min_success_rate_for_deploy": 0.7,
            },
            "cycle_config": {
                "analysis_interval": 300,      # 5분마다 분석
                "min_cycle_interval": 3600,     # 최소 1시간 간격
                "auto_retrain": True,
            },
            "sim_baseline_path": "results/sim2real_eval.json",
        }
        
        # JSON 설정 파일 로드 시도
        json_path = self.config_path.replace('.yaml', '.json')
        if os.path.exists(json_path):
            with open(json_path) as f:
                loaded = json.load(f)
                default_config.update(loaded)
                print(f'[Orchestrator] Loaded config from: {json_path}')
        elif os.path.exists(self.config_path):
            # YAML 로드 시도 (pyyaml 필요)
            try:
                import yaml
                with open(self.config_path) as f:
                    loaded = yaml.safe_load(f)
                    if loaded:
                        default_config.update(loaded)
                print(f'[Orchestrator] Loaded config from: {self.config_path}')
            except ImportError:
                print(f'[Orchestrator] pyyaml not installed, using defaults')
        else:
            # 기본 설정으로 파일 생성
            os.makedirs(os.path.dirname(self.config_path) or '.', exist_ok=True)
            import yaml
            with open(self.config_path, 'w') as f:
                yaml.dump(default_config, f, default_flow_style=False)
            print(f'[Orchestrator] Created default config: {self.config_path}')
        
        return default_config
    
    def _set_state(self, new_state: str):
        with self.state_lock:
            old_state = self.state
            self.state = new_state
            self._log_event("state_change", {
                "from": old_state,
                "to": new_state,
                "timestamp": datetime.now().isoformat(),
            })
            print(f'[Orchestrator] State: {old_state} → {new_state}')
    
    def _log_event(self, event_type: str, data: dict):
        """이벤트 로깅"""
        log_entry = {
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": data,
        }
        
        log_dir = f"{self.config['workspace']}/logs/orchestrator"
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = f"{log_dir}/events.jsonl"
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def _check_sim_baseline(self):
        """시뮬레이션 기준선 확인/로드"""
        baseline_path = self.config.get("sim_baseline_path")
        if baseline_path and os.path.exists(baseline_path):
            self.analyzer.load_sim_baseline_from_file(baseline_path)
            return True
        
        # 기본값 설정
        print(f'[Orchestrator] ⚠️  No sim baseline found. Using defaults.')
        self.analyzer.set_sim_baseline({
            "success_rate": 0.90,
            "collision_rate": 0.05,
            "avg_path_length": 3.0,
            "avg_linear_vel": 0.12,
            "num_trials": 100,
        })
        return False
    
    def start(self):
        """디지털 트윈 루프 시작"""
        print('\n' + '=' * 70)
        print('🚀 DIGITAL TWIN ORCHESTRATOR STARTING')
        print('=' * 70)
        
        self.running = True
        self._check_sim_baseline()
        self._set_state(self.STATE_MONITORING)
        
        print(f'\n[Orchestrator] Digital Twin Loop Active')
        print(f'  Analysis interval: {self.config["cycle_config"]["analysis_interval"]}s')
        print(f'  Auto retrain: {self.config["cycle_config"]["auto_retrain"]}')
        print(f'  Min cycle interval: {self.config["cycle_config"]["min_cycle_interval"]}s')
        
        # 메인 모니터링 루프
        try:
            while self.running:
                self._monitoring_cycle()
                time.sleep(self.config["cycle_config"]["analysis_interval"])
        except KeyboardInterrupt:
            print('\n[Orchestrator] Shutting down...')
        finally:
            self.running = False
            self._set_state(self.STATE_IDLE)
    
    def _monitoring_cycle(self):
        """모니터링 싸이클"""
        self._set_state(self.STATE_ANALYZING)
        
        active_policy = self.registry.get_active()
        if not active_policy:
            print('[Orchestrator] ⚠️  No active policy. Skipping analysis.')
            self._set_state(self.STATE_MONITORING)
            return
        
        policy_id = active_policy['policy_id']
        
        # 갭 분석
        analysis = self.analyzer.analyze(policy_id)
        
        # 메트릭 기록
        self.metrics_history.append({
            "timestamp": datetime.now().isoformat(),
            "policy_id": policy_id,
            "analysis": analysis,
        })
        
        # 상태 출력
        sr = analysis.get("real_success_rate", 0)
        sr_gap = analysis.get("success_rate_gap", 0)
        score = analysis.get("composite_score", 0)
        num_eps = analysis.get("num_episodes", 0)
        
        status = "🟢" if not analysis.get("needs_retrain") else "🔴"
        print(f'[{datetime.now().strftime("%H:%M:%S")}] {status} '
              f'policy={policy_id[:20]:<20} '
              f'SR={sr:.0%} gap={sr_gap:+.1%} '
              f'score={score:.2f} eps={num_eps}')
        
        # 재학습 트리거
        if analysis.get("needs_retrain") and self.config["cycle_config"]["auto_retrain"]:
            # 최소 간격 체크
            if self.last_cycle_time:
                elapsed = time.time() - self.last_cycle_time
                min_interval = self.config["cycle_config"]["min_cycle_interval"]
                if elapsed < min_interval:
                    print(f'  ⏳ Waiting {min_interval - elapsed:.0f}s before next retrain...')
                    self._set_state(self.STATE_MONITORING)
                    return
            
            print(f'\n  🚨 RETRAIN TRIGGERED')
            for reason in analysis.get("trigger_reasons", []):
                print(f'    - {reason}')
            
            self._execute_retrain_cycle(policy_id)
        
        self._set_state(self.STATE_MONITORING)
    
    def _execute_retrain_cycle(self, base_policy_id: str):
        """재학습 싸이클 실행"""
        self._set_state(self.STATE_RETRAINING)
        self.current_cycle += 1
        cycle_num = self.current_cycle
        
        print(f'\n{"=" * 70}')
        print(f'🔄 Digital Twin Cycle #{cycle_num}')
        print(f'{"=" * 70}')
        
        try:
            new_policy_id = self.pipeline.run_full_cycle(
                db_path=self.config["db_path"],
                base_policy=base_policy_id
            )
            
            if new_policy_id:
                self._set_state(self.STATE_DEPLOYING)
                self.last_cycle_time = time.time()
                
                self._log_event("cycle_complete", {
                    "cycle": cycle_num,
                    "base_policy": base_policy_id,
                    "new_policy": new_policy_id,
                    "timestamp": datetime.now().isoformat(),
                })
                
                print(f'\n✅ Cycle #{cycle_num} complete: {new_policy_id}')
            else:
                print(f'\n⚠️  Cycle #{cycle_num}: Deployment skipped (low SR)')
        
        except Exception as e:
            self._set_state(self.STATE_ERROR)
            self._log_event("cycle_error", {
                "cycle": cycle_num,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            })
            print(f'\n❌ Cycle #{cycle_num} failed: {e}')
    
    def get_status(self) -> dict:
        """전체 상태 리포트"""
        active = self.registry.get_active()
        policies = self.registry.list_policies()
        
        return {
            "state": self.state,
            "running": self.running,
            "current_cycle": self.current_cycle,
            "last_cycle_time": self.last_cycle_time,
            "active_policy": active,
            "total_policies": len(policies),
            "active_policies": len([p for p in policies if p["status"] == "active"]),
            "backup_policies": len([p for p in policies if p["status"] == "backup"]),
            "metrics_history": self.metrics_history[-10:],  # 최근 10개
        }
    
    def status_summary(self):
        """상태 요약 출력"""
        status = self.get_status()
        
        print(f'\n{"=" * 70}')
        print(f'📊 DIGITAL TWIN STATUS')
        print(f'{"=" * 70}')
        print(f'  State:          {status["state"]}')
        print(f'  Running:        {status["running"]}')
        print(f'  Cycle count:    {status["current_cycle"]}')
        
        active = status.get("active_policy")
        if active:
            sr = active.get("evaluation", {}).get("success_rate", 0)
            print(f'  Active policy:  {active["policy_id"]} (SR={sr:.0%})')
        
        print(f'  Policies:       {status["total_policies"]} total, '
              f'{status["active_policies"]} active, '
              f'{status["backup_policies"]} backup')
        
        if status["metrics_history"]:
            last = status["metrics_history"][-1]
            analysis = last.get("analysis", {})
            print(f'  Latest analysis: SR={analysis.get("real_success_rate", 0):.0%} '
                  f'gap={analysis.get("success_rate_gap", 0):+.1%} '
                  f'score={analysis.get("composite_score", 0):.2f}')
        
        print(f'{"=" * 70}\n')

    def stop(self):
        """디지털 트윈 중지"""
        self.running = False
        self._set_state(self.STATE_IDLE)
        print('[Orchestrator] Stopped.')


def main():
    parser = argparse.ArgumentParser(description="Digital Twin Orchestrator")
    parser.add_argument('--start', action='store_true', help='Start DT loop')
    parser.add_argument('--status', action='store_true', help='Show status')
    parser.add_argument('--stop', action='store_true', help='Stop DT loop (send SIGINT)')
    parser.add_argument('--config', default='config/digital_twin_config.yaml',
                       help='Configuration file')
    
    args = parser.parse_args()
    
    orch = DigitalTwinOrchestrator(args.config)
    
    if args.status:
        orch.status_summary()
    elif args.start:
        orch.start()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
