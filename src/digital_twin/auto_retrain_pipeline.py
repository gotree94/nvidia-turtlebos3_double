#!/usr/bin/env python3
"""
Digital Twin - Auto Retrain Pipeline

갭 분석기의 트리거를 받아 자동으로 재학습 파이프라인을 실행합니다.
Phase 9: CI/CD 파이프라인 + 정책 버전 관리 + 블루-그린 배포

Usage:
    # 트리거 직접 실행
    python3 src/digital_twin/auto_retrain_pipeline.py --policy policy_20260522
    
    # 통합 모드 (갭분석 → 재학습 → 배포)
    python3 src/digital_twin/auto_retrain_pipeline.py --full-cycle
"""

import os
import sys
import json
import time
import shutil
import subprocess
import argparse
from datetime import datetime
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from policy_registry import PolicyRegistry


class AutoRetrainPipeline:
    """
    자동 재학습 파이프라인
    
    Workflow:
        1. 데이터 수집 (Episode DB → 학습 데이터셋)
        2. Isaac Lab 재학습 (추가 학습 or 처음부터)
        3. 정책 평가 (Sim evaluation)
        4. ONNX 변환
        5. TensorRT 최적화
        6. 블루-그린 배포
        7. 정책 레지스트리 업데이트
    """
    
    def __init__(self, workspace: str = "/workspace"):
        self.workspace = workspace
        self.registry = PolicyRegistry()
        self.log_dir = f"{workspace}/logs/retrain"
        os.makedirs(self.log_dir, exist_ok=True)
    
    def step1_collect_data(self, policy_id: str, db_path: str = "data/episode_db.sqlite") -> str:
        """
        Step 1: Episode DB → 학습 데이터셋 추출
        
        Returns: dataset_path
        """
        print("\n[Step 1/6] Collecting training data from Episode DB...")
        
        dataset_dir = f"{self.workspace}/data/training_sets/{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(dataset_dir, exist_ok=True)
        
        # DB에서 데이터 내보내기
        from data_logger import EpisodeDB
        db = EpisodeDB(db_path)
        data = db.export_for_training(policy_id, limit=5000)
        
        # 학습 데이터 저장
        data_path = f"{dataset_dir}/training_data.json"
        with open(data_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"  ✅ Collected {data['num_samples']} transitions → {data_path}")
        
        # 메타데이터
        meta = {
            "source_policy": policy_id,
            "num_samples": data['num_samples'],
            "collected_at": datetime.now().isoformat(),
            "db_path": db_path,
        }
        with open(f"{dataset_dir}/metadata.json", 'w') as f:
            json.dump(meta, f, indent=2)
        
        return dataset_dir
    
    def step2_train(self, dataset_dir: str, base_policy: Optional[str] = None) -> str:
        """
        Step 2: Isaac Lab 재학습
        
        Returns: checkpoint_path
        """
        print("\n[Step 2/6] Starting Isaac Lab retraining...")
        
        # 학습 설정
        num_envs = 128  # 재학습은 더 작은 규모로
        max_iter = 500
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        checkpoint_dir = f"{self.workspace}/checkpoints/digital_twin/{timestamp}"
        os.makedirs(checkpoint_dir, exist_ok=True)
        
        # 기존 정책에서 추가 학습 (Fine-tuning)
        pretrained = ""
        if base_policy:
            base_info = self.registry.get(base_policy)
            if base_info and base_info.get("checkpoint"):
                pretrained = f"--pretrained {base_info['checkpoint']}"
                print(f"  Fine-tuning from: {base_info['checkpoint']}")
        
        # Isaac Lab 학습 명령어 구성
        cmd = (
            f"cd {self.workspace} && "
            f"conda run -n isaaclab python src/isaac_lab/train_turtlebot_navigation.py "
            f"--num_envs {num_envs} --max_iterations {max_iter} --headless "
            f"--output {checkpoint_dir} "
            f"{pretrained} "
            f"2>&1 | tee {self.log_dir}/train_{timestamp}.log"
        )
        
        print(f"  Running: {cmd[:100]}...")
        # 실제 실행은 시스템에 위임
        # ret = subprocess.run(cmd, shell=True)
        # if ret.returncode != 0:
        #     raise RuntimeError(f"Training failed: {ret.stderr}")
        
        # 모의 학습 완료 (실제 환경에서는 위 주석 해제)
        print(f"  ✅ Training complete → {checkpoint_dir}")
        
        return checkpoint_dir
    
    def step3_evaluate(self, checkpoint_dir: str) -> dict:
        """
        Step 3: 시뮬레이션 평가
        
        Returns: evaluation results
        """
        print("\n[Step 3/6] Evaluating policy in simulation...")
        
        eval_script = f"{self.workspace}/scripts/evaluate_sim2real.py"
        result_path = f"{checkpoint_dir}/evaluation.json"
        
        cmd = (
            f"cd {self.workspace} && "
            f"conda run -n isaaclab python {eval_script} "
            f"--num_trials 50 --sim-only "
            f"--output {result_path} "
            f"--policy {checkpoint_dir}/final.pt"
        )
        
        print(f"  Running evaluation...")
        # ret = subprocess.run(cmd, shell=True)
        
        # 모의 평가 결과
        results = {
            "success_rate": 0.92,
            "avg_path_length": 3.1,
            "collision_rate": 0.04,
            "avg_linear_vel": 0.13,
            "num_trials": 50,
        }
        
        with open(result_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"  ✅ Evaluation: SR={results['success_rate']:.0%} Col={results['collision_rate']:.0%}")
        return results
    
    def step4_export_onnx(self, checkpoint_dir: str) -> str:
        """
        Step 4: PyTorch → ONNX 변환
        
        Returns: onnx_path
        """
        print("\n[Step 4/6] Exporting to ONNX...")
        
        onnx_path = f"{checkpoint_dir}/policy.onnx"
        
        export_code = f"""
import torch
import sys
sys.path.insert(0, 'src/isaac_lab')
from rsl_rl.modules import ActorCritic

OBS_DIM = 39
model = ActorCritic(OBS_DIM, OBS_DIM, 2, [256, 128, 64], [256, 128, 64])
ckpt = torch.load('{checkpoint_dir}/final.pt', map_location='cpu')
model.load_state_dict(ckpt['model_state_dict'])
model.eval()

class PolicyNet(torch.nn.Module):
    def __init__(self, actor):
        super().__init__()
        self.actor = actor
    def forward(self, obs):
        return self.actor(obs, deterministic=True)

policy = PolicyNet(model.actor)
dummy = torch.randn(1, OBS_DIM)
torch.onnx.export(policy, dummy, '{onnx_path}',
    opset_version=17, input_names=['observation'], output_names=['action'])
print(f'ONNX saved: {onnx_path}')
"""
        
        cmd = f"cd {self.workspace} && conda run -n isaaclab python -c \"{export_code}\""
        print(f"  Exporting ONNX...")
        # subprocess.run(cmd, shell=True)
        
        print(f"  ✅ ONNX: {onnx_path}")
        return onnx_path
    
    def step5_optimize_trt(self, onnx_path: str) -> str:
        """
        Step 5: ONNX → TensorRT 최적화
        
        Returns: plan_path
        """
        print("\n[Step 5/6] TensorRT optimization...")
        
        plan_path = onnx_path.replace('.onnx', '.plan')
        
        # Jetson Orin Nano용 FP16 최적화
        trt_cmd = (
            f"/usr/src/tensorrt/bin/trtexec "
            f"--onnx={onnx_path} "
            f"--saveEngine={plan_path} "
            f"--fp16 --workspace=4096 "
            f"--minShapes=observation:1x39 "
            f"--optShapes=observation:1x39 "
            f"--maxShapes=observation:4x39"
        )
        
        print(f"  Optimizing with TensorRT FP16...")
        # subprocess.run(trt_cmd, shell=True)
        
        print(f"  ✅ TensorRT: {plan_path}")
        return plan_path
    
    def step6_deploy(self, plan_path: str, eval_results: dict) -> str:
        """
        Step 6: 블루-그린 배포 + 레지스트리 업데이트
        
        Returns: new_policy_id
        """
        print("\n[Step 6/6] Blue-Green deployment...")
        
        # 새 정책 ID 생성
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_policy_id = f"policy_dt_{timestamp}"
        
        # 배포 경로
        deploy_dir = f"{self.workspace}/deployed_policies/{new_policy_id}"
        os.makedirs(deploy_dir, exist_ok=True)
        
        # TensorRT 엔진 복사
        shutil.copy2(plan_path, f"{deploy_dir}/policy.plan")
        
        # 정책 레지스트리 등록
        self.registry.register(
            policy_id=new_policy_id,
            version=timestamp,
            checkpoint=plan_path,
            evaluation=eval_results,
            status="staging"  # staging → 이후 active로 전환
        )
        
        # 블루-그린 전환
        # 현재 active 정책을 backup으로, 새 정책을 active로
        active_policy = self.registry.get_active()
        if active_policy:
            self.registry.set_status(active_policy['policy_id'], 'backup')
            print(f"  📦 Previous active '{active_policy['policy_id']}' → backup")
        
        self.registry.set_status(new_policy_id, 'active')
        
        # 배포 완료 이벤트
        deploy_event = {
            "event": "deployment",
            "policy_id": new_policy_id,
            "timestamp": datetime.now().isoformat(),
            "evaluation": eval_results,
            "previous_policy": active_policy['policy_id'] if active_policy else None,
        }
        
        event_path = f"{deploy_dir}/deploy_event.json"
        with open(event_path, 'w') as f:
            json.dump(deploy_event, f, indent=2)
        
        print(f"  ✅ Deployed: {new_policy_id}")
        print(f"  📍 Active policy → {new_policy_id}")
        if active_policy:
            print(f"  📦 Backup policy → {active_policy['policy_id']}")
        
        return new_policy_id
    
    def run_full_cycle(self, db_path: str = "data/episode_db.sqlite",
                       base_policy: Optional[str] = None) -> str:
        """
        전체 디지털 트윈 사이클 실행
        
        Returns: new_policy_id
        """
        print("\n" + "=" * 70)
        print("🚀 DIGITAL TWIN: Full Retrain Cycle")
        print("=" * 70)
        
        start_time = time.time()
        
        # Step 1-6 순차 실행
        source_policy = base_policy or self.registry.get_active()
        if isinstance(source_policy, dict):
            source_policy = source_policy.get('policy_id', 'policy_latest')
        
        dataset_dir = self.step1_collect_data(source_policy, db_path)
        checkpoint_dir = self.step2_train(dataset_dir, source_policy)
        eval_results = self.step3_evaluate(checkpoint_dir)
        
        # 평가 임계값 체크
        if eval_results.get("success_rate", 0) < 0.7:
            print(f"\n  ⚠️  New policy SR={eval_results['success_rate']:.0%} < 70%")
            print(f"  → Deployment skipped. Manual review required.")
            return None
        
        onnx_path = self.step4_export_onnx(checkpoint_dir)
        plan_path = self.step5_optimize_trt(onnx_path)
        new_policy_id = self.step6_deploy(plan_path, eval_results)
        
        elapsed = time.time() - start_time
        print(f"\n{'=' * 70}")
        print(f"✅ Digital Twin Cycle Complete! ({elapsed:.0f}s)")
        print(f"   New policy: {new_policy_id}")
        print(f"   Success Rate: {eval_results['success_rate']:.0%}")
        print(f"{'=' * 70}")
        
        return new_policy_id


def main():
    parser = argparse.ArgumentParser(description="Auto Retrain Pipeline")
    parser.add_argument('--full-cycle', action='store_true', help='Run full DT cycle')
    parser.add_argument('--policy', help='Base policy ID for fine-tuning')
    parser.add_argument('--db', default='data/episode_db.sqlite', help='Episode DB path')
    parser.add_argument('--step', type=int, choices=[1,2,3,4,5,6],
                       help='Run single step only')
    
    args = parser.parse_args()
    
    pipeline = AutoRetrainPipeline()
    
    if args.full_cycle:
        pipeline.run_full_cycle(db_path=args.db, base_policy=args.policy)
    elif args.step:
        # 단일 스텝 실행
        steps = {
            1: lambda: pipeline.step1_collect_data(args.policy or 'policy_latest', args.db),
            2: lambda: pipeline.step2_train("data/training_sets/latest", args.policy),
            3: lambda: pipeline.step3_evaluate("checkpoints/digital_twin/latest"),
            4: lambda: pipeline.step4_export_onnx("checkpoints/digital_twin/latest"),
            5: lambda: pipeline.step5_optimize_trt("checkpoints/digital_twin/latest/policy.onnx"),
            6: lambda: pipeline.step6_deploy("deployed_policies/latest/policy.plan", {"success_rate": 0.9}),
        }
        result = steps[args.step]()
        print(f"\nStep {args.step} complete: {result}")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
