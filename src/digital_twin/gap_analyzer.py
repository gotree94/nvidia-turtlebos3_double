#!/usr/bin/env python3
"""
Digital Twin - Gap Analyzer (Sim vs Real)

시뮬레이션 정책 성능 vs 실제 로봇 성능을 비교 분석하여
재학습이 필요한 시점을 자동으로 감지합니다.

Usage:
    # 단일 분석
    python3 src/digital_twin/gap_analyzer.py --db data/episode_db.sqlite
    
    # 연속 모니터링
    python3 src/digital_twin/gap_analyzer.py --watch --interval 300
"""

import os
import sys
import json
import time
import math
import argparse
import numpy as np
from datetime import datetime
from typing import Optional, List, Tuple

# DB 모듈
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_logger import EpisodeDB


class GapAnalyzer:
    """
    Sim-to-Real 갭 분석기
    
    시뮬레이션(Isaac Lab 평가)과 실제 로봇(데이터 로거)의
    성능 차이를 지속적으로 추적하고 재학습 트리거를 발생시킵니다.
    
    분석 메트릭:
        - Success Rate 갭 (Sim - Real)
        - 평균 경로 길이 갭
        - 충돌률 갭
        - 평균 속도 갭
        - 복합 Score (가중치 합)
    """
    
    def __init__(self, db_path: str, config: Optional[dict] = None):
        self.db = EpisodeDB(db_path)
        
        # 기본 설정
        self.config = config or {
            # 재학습 트리거 임계값
            "success_rate_gap_threshold": 0.15,    # 15% 이상 차이 → 트리거
            "collision_rate_gap_threshold": 0.10,  # 10% 이상 차이 → 트리거
            "min_episodes_for_analysis": 10,       # 최소 분석 샘플 수
            "window_size": 50,                     # 최근 N 에피소드 윈도우
            
            # 가중치 (복합 Score 계산용)
            "weight_success_rate": 0.5,
            "weight_collision_rate": 0.3,
            "weight_path_efficiency": 0.2,
        }
        
        # 시뮬레이션 기준 성능 (Isaac Lab에서 미리 측정)
        self.sim_baseline = {}
        
        print(f'[GapAnalyzer] Initialized | db={db_path}')
    
    def set_sim_baseline(self, results: dict):
        """
        시뮬레이션 기준 성능 설정
        
        Args:
            results: evaluate_sim2real.py 출력 형식
                     {
                         "success_rate": 0.95,
                         "avg_path_length": 3.2,
                         "collision_rate": 0.03,
                         "avg_linear_vel": 0.12,
                         "num_trials": 100
                     }
        """
        self.sim_baseline = results
        print(f'[GapAnalyzer] Sim baseline set: '
              f'SR={results.get("success_rate", 0):.1%} '
              f'Col={results.get("collision_rate", 0):.1%}')
    
    def load_sim_baseline_from_file(self, path: str):
        """JSON 파일에서 시뮬레이션 기준 로드"""
        with open(path, 'r') as f:
            data = json.load(f)
        
        sim = data.get("sim_stats", {})
        self.set_sim_baseline({
            "success_rate": sim.get("success_rate", 0),
            "avg_path_length": sim.get("avg_path_length", 0),
            "collision_rate": sim.get("collision_rate", 0),
            "avg_linear_vel": sim.get("avg_linear_vel", 0),
            "num_trials": sim.get("num_trials", 0),
        })
        print(f'[GapAnalyzer] Loaded sim baseline from: {path}')
    
    def analyze(self, policy_id: str) -> dict:
        """
        특정 정책의 Sim-vs-Real 갭 분석
        
        Args:
            policy_id: 분석할 정책 ID
            
        Returns:
            {
                "policy_id": str,
                "num_episodes": int,
                "real_success_rate": float,
                "sim_success_rate": float,
                "success_rate_gap": float,
                "collision_rate_gap": float,
                "composite_score": float,
                "needs_retrain": bool,
                "trigger_reasons": [str],
                "timestamp": str,
            }
        """
        window = self.config["window_size"]
        
        # 실제 로봇 성능 (DB에서)
        rows = self.db.get_recent_episodes(limit=window, policy_id=policy_id)
        completed = [r for r in rows if r[4] is not None]  # end_time IS NOT NULL
        
        result = {
            "policy_id": policy_id,
            "timestamp": datetime.now().isoformat(),
            "num_episodes": len(completed),
            "trigger_reasons": [],
            "needs_retrain": False,
        }
        
        if len(completed) < self.config["min_episodes_for_analysis"]:
            result["warning"] = f"Need {self.config['min_episodes_for_analysis']}+ episodes, got {len(completed)}"
            print(f'[GapAnalyzer] {result["warning"]}')
            return result
        
        # 실제 성능 계산
        successes = sum(1 for r in completed if r[5])  # success column
        result["real_success_rate"] = successes / len(completed)
        
        # 충돌률 (metrics 테이블에서)
        collisions = 0
        for r in completed:
            ep_id = r[0]
            with sqlite3.connect(self.db.db_path) as conn:
                row = conn.execute(
                    "SELECT collisions FROM metrics WHERE episode_id = ?", (ep_id,)
                ).fetchone()
                if row and row[0] > 0:
                    collisions += 1
        result["real_collision_rate"] = collisions / len(completed)
        
        # 시뮬레이션 기준
        sim_sr = self.sim_baseline.get("success_rate", 0)
        sim_cr = self.sim_baseline.get("collision_rate", 0)
        result["sim_success_rate"] = sim_sr
        result["sim_collision_rate"] = sim_cr
        
        # 갭 계산
        sr_gap = sim_sr - result["real_success_rate"]
        cr_gap = result["real_collision_rate"] - sim_cr
        result["success_rate_gap"] = sr_gap
        result["collision_rate_gap"] = cr_gap
        
        # 복합 Score (0~1, 높을수록 재학습 필요)
        composite = (
            self.config["weight_success_rate"] * max(0, sr_gap / (1 - sim_sr + 0.01)) +
            self.config["weight_collision_rate"] * min(1, max(0, cr_gap / (1 - sim_cr + 0.01))) +
            self.config["weight_path_efficiency"] * 0  # 확장 가능
        )
        result["composite_score"] = min(1.0, composite)
        
        # 재학습 트리거 체크
        if sr_gap > self.config["success_rate_gap_threshold"]:
            result["trigger_reasons"].append(
                f"Success rate gap {sr_gap:.1%} > threshold {self.config['success_rate_gap_threshold']:.1%}"
            )
        
        if cr_gap > self.config["collision_rate_gap_threshold"]:
            result["trigger_reasons"].append(
                f"Collision rate gap {cr_gap:.1%} > threshold {self.config['collision_rate_gap_threshold']:.1%}"
            )
        
        if result["composite_score"] > 0.5:
            result["trigger_reasons"].append(
                f"Composite score {result['composite_score']:.2f} > 0.5"
            )
        
        result["needs_retrain"] = len(result["trigger_reasons"]) > 0
        
        return result
    
    def watch_loop(self, policy_id: str, interval: int = 300):
        """
        지속 모니터링 루프
        
        Args:
            policy_id: 모니터링할 정책 ID
            interval: 체크 간격 (초)
        """
        print(f'[GapAnalyzer] Watching policy={policy_id} every {interval}s')
        print(f'  Thresholds: SR_gap>{self.config["success_rate_gap_threshold"]:.0%} '
              f'| CR_gap>{self.config["collision_rate_gap_threshold"]:.0%}')
        print(f'  Press Ctrl+C to stop\n')
        
        while True:
            result = self.analyze(policy_id)
            
            status = "🟢" if not result["needs_retrain"] else "🔴"
            print(f'[{datetime.now().strftime("%H:%M:%S")}] {status} '
                  f'SR: sim={result.get("sim_success_rate", 0):.0%} '
                  f'real={result.get("real_success_rate", 0):.0%} '
                  f'gap={result.get("success_rate_gap", 0):+.1%} | '
                  f'score={result.get("composite_score", 0):.2f} '
                  f'episodes={result.get("num_episodes", 0)}')
            
            if result["needs_retrain"]:
                print(f'  🚨 RETRAIN TRIGGERED:')
                for reason in result["trigger_reasons"]:
                    print(f'    - {reason}')
                print(f'  → Run: python3 src/digital_twin/auto_retrain_pipeline.py')
                print()
            
            time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description="Digital Twin Gap Analyzer")
    parser.add_argument('--db', default='data/episode_db.sqlite', help='Episode DB path')
    parser.add_argument('--policy', default='policy_latest', help='Policy ID to analyze')
    parser.add_argument('--sim-baseline', help='Sim baseline JSON file')
    parser.add_argument('--watch', action='store_true', help='Continuous monitoring mode')
    parser.add_argument('--interval', type=int, default=300, help='Watch interval (seconds)')
    parser.add_argument('--threshold', type=float, default=0.15, help='SR gap threshold')
    
    args = parser.parse_args()
    
    # SQLite3 import (data_logger에서 사용)
    global sqlite3
    import sqlite3
    
    analyzer = GapAnalyzer(args.db)
    
    if args.sim_baseline and os.path.exists(args.sim_baseline):
        analyzer.load_sim_baseline_from_file(args.sim_baseline)
    elif args.sim_baseline:
        print(f'[ERROR] Sim baseline not found: {args.sim_baseline}')
        sys.exit(1)
    
    if args.watch:
        analyzer.config["success_rate_gap_threshold"] = args.threshold
        analyzer.watch_loop(args.policy, args.interval)
    else:
        result = analyzer.analyze(args.policy)
        print(json.dumps(result, indent=2, default=str))
        
        if result.get("needs_retrain"):
            print("\n🚨 Retrain recommended! Run:")
            print("  python3 src/digital_twin/auto_retrain_pipeline.py")


if __name__ == '__main__':
    main()
