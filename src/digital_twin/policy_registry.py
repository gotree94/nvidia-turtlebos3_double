#!/usr/bin/env python3
"""
Digital Twin - Policy Registry

정책 버전 관리, 블루-그린 배포, 롤백을 담당합니다.

Usage:
    python3 src/digital_twin/policy_registry.py --list
    python3 src/digital_twin/policy_registry.py --activate policy_id
"""

import os
import json
import time
import argparse
from datetime import datetime
from typing import Optional, List


class PolicyRegistry:
    """
    정책 레지스트리 (JSON 기반)
    
    여러 버전의 정책을 관리하고 블루-그린 배포를 지원합니다.
    
    정책 상태:
        - active: 현재 서비스 중
        - staging: 배포 전 검증 중
        - backup: 이전 버전 (롤백 가능)
        - archived: 기록 보관
        - failed: 배포 실패
    
    레지스트리 파일 구조:
    {
        "policies": {
            "policy_dt_20260522_120000": {
                "policy_id": "policy_dt_20260522_120000",
                "version": "20260522_120000",
                "checkpoint": "/path/to/policy.plan",
                "status": "active",
                "evaluation": { "success_rate": 0.92, ... },
                "created_at": "2026-05-22T12:00:00",
                "deployed_at": "2026-05-22T12:30:00",
                "num_episodes_trained": 5000,
                "notes": "After domain randomization fix"
            },
            ...
        },
        "active_policy": "policy_dt_20260522_120000",
        "history": [ ... ]
    }
    """
    
    def __init__(self, registry_path: str = "config/policy_registry.json"):
        self.registry_path = registry_path
        self._ensure_registry()
    
    def _ensure_registry(self):
        os.makedirs(os.path.dirname(self.registry_path) or '.', exist_ok=True)
        if not os.path.exists(self.registry_path):
            self._write({
                "policies": {},
                "active_policy": None,
                "history": [],
                "last_updated": datetime.now().isoformat(),
            })
    
    def _read(self) -> dict:
        with open(self.registry_path, 'r') as f:
            return json.load(f)
    
    def _write(self, data: dict):
        data["last_updated"] = datetime.now().isoformat()
        with open(self.registry_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def register(self, policy_id: str, version: str, checkpoint: str,
                 evaluation: dict, status: str = "staging",
                 notes: str = "", num_episodes: int = 0) -> bool:
        """새 정책 등록"""
        registry = self._read()
        
        if policy_id in registry["policies"]:
            print(f"[Registry] Policy '{policy_id}' already exists. Updating...")
        
        registry["policies"][policy_id] = {
            "policy_id": policy_id,
            "version": version,
            "checkpoint": checkpoint,
            "status": status,
            "evaluation": evaluation,
            "created_at": datetime.now().isoformat(),
            "deployed_at": None,
            "num_episodes_trained": num_episodes,
            "notes": notes,
        }
        
        self._write(registry)
        print(f"[Registry] ✅ Registered: {policy_id} ({status})")
        return True
    
    def set_status(self, policy_id: str, status: str) -> bool:
        """정책 상태 변경"""
        registry = self._read()
        
        if policy_id not in registry["policies"]:
            print(f"[Registry] ❌ Policy not found: {policy_id}")
            return False
        
        old_status = registry["policies"][policy_id]["status"]
        registry["policies"][policy_id]["status"] = status
        
        if status == "active":
            registry["active_policy"] = policy_id
            registry["policies"][policy_id]["deployed_at"] = datetime.now().isoformat()
            
            # 히스토리 기록
            registry["history"].append({
                "event": "activate",
                "policy_id": policy_id,
                "timestamp": datetime.now().isoformat(),
                "evaluation": registry["policies"][policy_id]["evaluation"],
            })
        
        self._write(registry)
        print(f"[Registry] ✅ {policy_id}: {old_status} → {status}")
        return True
    
    def get_active(self) -> Optional[dict]:
        """현재 active 정책 조회"""
        registry = self._read()
        active_id = registry.get("active_policy")
        if active_id and active_id in registry["policies"]:
            return registry["policies"][active_id]
        return None
    
    def get(self, policy_id: str) -> Optional[dict]:
        """특정 정책 조회"""
        registry = self._read()
        return registry["policies"].get(policy_id)
    
    def list_policies(self, status_filter: Optional[str] = None) -> List[dict]:
        """정책 목록 조회"""
        registry = self._read()
        policies = registry["policies"].values()
        if status_filter:
            policies = [p for p in policies if p["status"] == status_filter]
        return sorted(policies, key=lambda p: p["created_at"], reverse=True)
    
    def rollback(self) -> Optional[str]:
        """
        블루-그린 롤백: 현재 active → backup, 가장 최근 backup → active
        
        Returns: rollback된 정책 ID
        """
        registry = self._read()
        active = self.get_active()
        
        if not active:
            print("[Registry] ❌ No active policy to rollback from")
            return None
        
        # 가장 최근 backup 찾기
        backups = [p for p in registry["policies"].values()
                  if p["status"] == "backup"]
        
        if not backups:
            print("[Registry] ❌ No backup policy found")
            return None
        
        # 가장 최근 backup (정렬은 되어있지만 명시적으로)
        rollback_target = max(backups, key=lambda p: p["created_at"])
        
        # 전환
        self.set_status(active["policy_id"], "backup")
        self.set_status(rollback_target["policy_id"], "active")
        
        # 히스토리
        registry = self._read()
        registry["history"].append({
            "event": "rollback",
            "from": active["policy_id"],
            "to": rollback_target["policy_id"],
            "timestamp": datetime.now().isoformat(),
            "reason": "manual_rollback",
        })
        self._write(registry)
        
        print(f"[Registry] 🔄 Rollback: {active['policy_id']} → {rollback_target['policy_id']}")
        return rollback_target["policy_id"]
    
    def get_history(self, limit: int = 20) -> List[dict]:
        """변경 이력 조회"""
        registry = self._read()
        return registry["history"][-limit:]
    
    def cleanup(self, keep_active: bool = True, max_backups: int = 3):
        """
        오래된 백업 정리
        
        Args:
            keep_active: active 유지
            max_backups: 최대 백업 수
        """
        registry = self._read()
        backups = [p for p in registry["policies"].values()
                  if p["status"] == "backup"]
        
        # 시간순 정렬 (오래된 순)
        backups.sort(key=lambda p: p["created_at"])
        
        # 초과분 아카이브
        to_archive = backups[:-max_backups] if len(backups) > max_backups else []
        
        for p in to_archive:
            self.set_status(p["policy_id"], "archived")
            # 실제 파일도 정리 가능
            if os.path.exists(p["checkpoint"]):
                pass  # 보관 정책에 따라 삭제 또는 유지
            print(f"[Registry] 🗂️ Archived: {p['policy_id']}")


def main():
    parser = argparse.ArgumentParser(description="Policy Registry Manager")
    parser.add_argument('--list', action='store_true', help='List all policies')
    parser.add_argument('--active', action='store_true', help='Show active policy')
    parser.add_argument('--activate', help='Activate a policy')
    parser.add_argument('--rollback', action='store_true', help='Rollback to backup')
    parser.add_argument('--history', action='store_true', help='Show deployment history')
    parser.add_argument('--status', help='Filter by status (active/backup/staging/archived)')
    
    args = parser.parse_args()
    
    reg = PolicyRegistry()
    
    if args.list:
        policies = reg.list_policies(args.status)
        if not policies:
            print("No policies found.")
            return
        
        print(f"\n{'ID':<35} {'Status':<10} {'SR':<8} {'Col':<8} {'Deployed':<20}")
        print('-' * 81)
        for p in policies:
            sr = p.get('evaluation', {}).get('success_rate', 0)
            col = p.get('evaluation', {}).get('collision_rate', 0)
            dep = p.get('deployed_at', '-')[:19] if p.get('deployed_at') else '-'
            pid = p['policy_id'][:34]
            print(f"{pid:<35} {p['status']:<10} {sr:<7.0%} {col:<7.0%} {dep:<20}")
    
    elif args.active:
        active = reg.get_active()
        if active:
            print(json.dumps(active, indent=2, default=str))
        else:
            print("No active policy.")
    
    elif args.activate:
        reg.set_status(args.activate, 'active')
    
    elif args.rollback:
        reg.rollback()
    
    elif args.history:
        for h in reg.get_history():
            print(f"[{h['timestamp'][:19]}] {h['event']}: {h.get('policy_id', h.get('to', '?'))}")


if __name__ == '__main__':
    main()
