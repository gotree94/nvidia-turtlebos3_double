# 11. Digital Twin Loop: 완전 자동화 파이프라인

> **실시간 데이터 수집 → 갭 분석 → 자동 재학습 → 블루-그린 배포 → 무한 개선 루프**

---

## 1. 개요

Digital Twin Loop은 실제 로봇의 주행 데이터를 지속적으로 수집하고,
시뮬레이션 정책과의 성능 차이(Gap)를 분석하여,
자동으로 재학습 → 배포하는 **Closed-Loop 자동화 파이프라인**입니다.

```
  [실제 로봇] ──주행 데이터──► [Episode DB] ──► [Gap Analyzer]
       ▲                                              │
       │                                      (Gap > Threshold?)
       │                                              │
       │                                     Yes      │       No
       │                                              ▼
       │                                   [Auto Retrain]
       │                                        │
       │                                        ▼
       │                              [Evaluate: SR > 70%?]
       │                                        │
       │                               Yes      │       No
       │                                        ▼
       │                              [Blue-Green Deploy]
       │                                        │
       └──────────◄───[새 정책 배포]────────────┘
```

---

## 2. Phase 7: 데이터 수집 (Data Logger)

### 2.1 EpisodeDB (SQLite 기반 경험 저장소)

실제 로봇의 모든 주행 경험을 구조화된 형태로 저장합니다.

**스키마:**

```sql
-- 에피소드 메타데이터
CREATE TABLE episodes (
    id TEXT PRIMARY KEY,          -- UUID
    robot_id TEXT NOT NULL,       -- 로봇 식별자
    policy_id TEXT NOT NULL,      -- 사용된 정책 버전
    start_time REAL NOT NULL,     -- 시작 timestamp
    end_time REAL,                -- 종료 timestamp
    success BOOL DEFAULT 0,       -- 목표 도달 성공 여부
    goal_x REAL,                  -- 목표 x 좌표
    goal_y REAL,                  -- 목표 y 좌표
    env_config TEXT               -- 환경 설정 (JSON)
);

-- 상태-행동 전이 (Transition)
CREATE TABLE transitions (
    id TEXT PRIMARY KEY,
    episode_id TEXT NOT NULL,     -- 소속 에피소드
    timestamp REAL NOT NULL,      -- 기록 시간
    lidar BLOB,                   -- 36ch downsampled LiDAR
    goal_rel BLOB,                -- 목표 상대 위치 (dx, dy)
    heading_err REAL,             -- 방향 오차
    linear_vel REAL,              -- 선속도 명령
    angular_vel REAL,             -- 각속도 명령
    reward REAL DEFAULT 0,        -- 보상 (추후 계산)
    done BOOL DEFAULT 0           -- 종료 여부
);

-- 성능 메트릭
CREATE TABLE metrics (
    episode_id TEXT PRIMARY KEY,
    path_length REAL DEFAULT 0,    -- 이동 거리
    avg_linear_vel REAL DEFAULT 0, -- 평균 선속도
    avg_angular_vel REAL DEFAULT 0,-- 평균 각속도
    min_lidar REAL DEFAULT 3.5,    -- 최소 LiDAR 거리
    collisions INT DEFAULT 0,      -- 충돌 횟수
    success BOOL DEFAULT 0         -- 성공 여부
);
```

### 2.2 RealWorldDataLogger (ROS2 노드)

```bash
# 데이터 로거 실행
ros2 run digital_twin data_logger

# 또는 직접 실행
python3 src/digital_twin/data_logger.py

# 수집 데이터 확인
python3 -c "
from src.digital_twin.data_logger import EpisodeDB
db = EpisodeDB('data/episode_db.sqlite')
episodes = db.get_recent_episodes(limit=5)
for ep in episodes:
    print(f'Episode {ep[0][:8]}... | policy={ep[2]} | success={ep[5]}')
"
```

**자동 감지 기능:**
- ✅ **목표 도달**: 목표 반경 0.2m 이내 진입 시 에피소드 종료
- ✅ **충돌 감지**: LiDAR 0.15m 이하 3회 연속 → 충돌 판정
- ✅ **타임아웃**: 120초 초과 또는 1000스텝 초과 시 자동 종료
- ✅ **에피소드 자동 분할**: 각 Goal 도달 시도마다 자동 분할 저장

---

## 3. Phase 8: 갭 분석 (Gap Analyzer)

### 3.1 분석 메트릭

| 메트릭 | 계산식 | 임계값 | 의미 |
|--------|--------|--------|------|
| **Success Rate Gap** | Sim_SR - Real_SR | > 15% | 시뮬레이션보다 실제 성능 저하 |
| **Collision Rate Gap** | Real_CR - Sim_CR | > 10% | 실제 환경에서 더 많이 충돌 |
| **Path Efficiency Gap** | Real_Path / Sim_Path | > 1.5x | 실제 경로가 비효율적 |
| **Composite Score** | 가중치 합 | > 0.5 | 종합 점수 |

### 3.2 갭 분석기 실행

```bash
# 1회 분석
python3 src/digital_twin/gap_analyzer.py \
    --db data/episode_db.sqlite \
    --policy policy_20260522 \
    --sim-baseline results/sim2real_eval.json

# 지속 모니터링 모드 (5분 간격)
python3 src/digital_twin/gap_analyzer.py \
    --db data/episode_db.sqlite \
    --policy policy_20260522 \
    --sim-baseline results/sim2real_eval.json \
    --watch --interval 300 --threshold 0.15

# 출력 예시
# [14:30:00] 🟢 SR: sim=95% real=92% gap=-3% | score=0.12 episodes=47
# [14:35:00] 🟢 SR: sim=95% real=90% gap=-5% | score=0.18 episodes=52
# [14:40:00] 🔴 SR: sim=95% real=78% gap=-17% | score=0.58 episodes=55
#   🚨 RETRAIN TRIGGERED:
#     - Success rate gap 17% > threshold 15%
#     → Run: python3 src/digital_twin/auto_retrain_pipeline.py
```

### 3.3 Sim Baseline 설정

Sim Baseline은 Isaac Lab에서 평가한 시뮬레이션 정책의 기준 성능입니다:

```json
{
    "success_rate": 0.95,
    "avg_path_length": 3.2,
    "collision_rate": 0.03,
    "avg_linear_vel": 0.12,
    "num_trials": 100
}
```

```bash
# Sim Baseline 생성
python3 scripts/evaluate_sim2real.py \
    --num_trials 100 --sim-only \
    --output results/sim2real_eval.json
```

---

## 4. Phase 9: 자동 재학습 파이프라인

### 4.1 6단계 파이프라인

```
Step 1 ─── 데이터 수집: Episode DB → Training Dataset
    │
Step 2 ─── Isaac Lab 재학습 (Fine-tuning or Scratch)
    │
Step 3 ─── 시뮬레이션 평가 (SR > 70% 체크)
    │
Step 4 ─── PyTorch → ONNX 변환
    │
Step 5 ─── TensorRT FP16 최적화
    │
Step 6 ─── 블루-그린 배포 + 레지스트리 업데이트
```

### 4.2 실행 명령어

```bash
# 전체 사이클 실행
python3 src/digital_twin/auto_retrain_pipeline.py --full-cycle

# 단계별 실행
python3 src/digital_twin/auto_retrain_pipeline.py --step 1  # 데이터 수집
python3 src/digital_twin/auto_retrain_pipeline.py --step 2  # 재학습
python3 src/digital_twin/auto_retrain_pipeline.py --step 3  # 평가
python3 src/digital_twin/auto_retrain_pipeline.py --step 4  # ONNX
python3 src/digital_twin/auto_retrain_pipeline.py --step 5  # TensorRT
python3 src/digital_twin/auto_retrain_pipeline.py --step 6  # 배포
```

### 4.3 정책 레지스트리 (Policy Registry)

모든 정책 버전을 체계적으로 관리합니다:

```bash
# 전체 정책 목록
python3 src/digital_twin/policy_registry.py --list

# 출력 예시:
# ID                                Status     SR       Col      Deployed
# -------------------------------------------------------------------------
# policy_dt_20260522_120000         active    92%      4%       2026-05-22T12:00:00
# policy_dt_20260521_150000         backup    88%      6%       2026-05-21T15:00:00
# policy_dt_20260520_090000         backup    85%      8%       2026-05-20T09:00:00
# policy_base_v1                    archived  80%      10%      2026-05-01T00:00:00

# Active 정책 확인
python3 src/digital_twin/policy_registry.py --active

# 특정 정책 활성화 (수동 전환)
python3 src/digital_twin/policy_registry.py --activate policy_dt_20260521_150000

# 롤백
python3 src/digital_twin/policy_registry.py --rollback

# 배포 이력
python3 src/digital_twin/policy_registry.py --history
```

### 4.4 블루-그린 배포 (Blue-Green Deployment)

무중단 배포를 위한 전략:

```
Before:
  [Active] policy_v1 ← 로봇이 사용 중
  
Step 1: 새 정책 준비 (Staging)
  [Active] policy_v1  [Staging] policy_v2
  
Step 2: 블루-그린 전환 (Atomic symlink switch)
  [Backup] policy_v1  [Active] policy_v2  ← 로봇 즉시 전환
  
Step 3: 문제 발생 시 롤백
  [Active] policy_v1  [Backup] policy_v2  ← 1초 컷 오버
```

```bash
# 블루-그린 배포
bash scripts/deploy_policy.sh outputs/policy/policy.plan policy_dt_v2

# 롤백
bash scripts/deploy_policy.sh --rollback

# 상태 확인
bash scripts/deploy_policy.sh --status
```

### 4.5 정책 버전 관리 전략

```
policy_dt_{yyyymmdd}_{hhmmss}_{상태}
  │          │          │       │
  │          │          │       └── active | backup | archived
  │          │          └── 배포 시각
  │          └── 날짜
  └── Digital Twin 정책
```

---

## 5. Phase 10: 디지털 트윈 오케스트레이터

### 5.1 통합 실행

```bash
# 디지털 트윈 시작
python3 src/digital_twin/orchestrator.py --start

# 상태 확인
python3 src/digital_twin/orchestrator.py --status

# 출력 예시:
# ======================================================================
# 📊 DIGITAL TWIN STATUS
# ======================================================================
#   State:          monitoring
#   Running:        true
#   Cycle count:    3
#   Active policy:  policy_dt_20260522_120000 (SR=92%)
#   Policies:       12 total, 1 active, 2 backup
#   Latest analysis: SR=90% gap=-5% score=0.18
# ======================================================================
```

### 5.2 상태 머신

```
                    ┌──────────┐
                    │   IDLE   │
                    └────┬─────┘
                         │ --start
                         ▼
              ┌─────────────────────┐
              │     MONITORING      │ ◄────────────┐
              │  (5분 간격 분석)     │              │
              └──────────┬──────────┘              │
                         │ Gap > Threshold?        │
                    Yes  │          No             │
                    ┌────┘          └────┐         │
                    ▼                    │         │
              ┌──────────┐              │         │
              │ RETRAIN  │              │         │
              │ (6 Steps)│              │         │
              └─────┬────┘              │         │
                    │ SR > 70%?         │         │
               Yes  │       No          │         │
               ┌────┘       └──┐        │         │
               ▼               ▼        │         │
        ┌──────────┐    ┌────────┐      │         │
        │ DEPLOY   │    │ SKIP   │      │         │
        └─────┬────┘    └────────┘      │         │
              │                         │         │
              └─────────────────────────┘─────────┘
                                        (계속 모니터링)
```

### 5.3 이벤트 로그

모든 이벤트는 `logs/orchestrator/events.jsonl`에 기록됩니다:

```json
{"type": "state_change", "timestamp": "2026-05-22T12:00:00", "data": {"from": "monitoring", "to": "retraining"}}
{"type": "cycle_complete", "timestamp": "2026-05-22T12:45:00", "data": {"cycle": 3, "base_policy": "policy_v2", "new_policy": "policy_v3"}}
{"type": "deployment", "timestamp": "2026-05-22T12:46:00", "data": {"policy_id": "policy_v3", "status": "active"}}
```

---

## 6. 전체 실행 가이드

### 6.1 최초 설정

```bash
# 1. 환경 설정 파일 생성
python3 src/digital_twin/orchestrator.py --start
# config/digital_twin_config.yaml 자동 생성됨

# 2. Sim Baseline 생성
python3 scripts/evaluate_sim2real.py --num_trials 100 --sim-only

# 3. Episode DB 초기화
python3 -c "from src.digital_twin.data_logger import EpisodeDB; EpisodeDB()"
```

### 6.2 정상 운영

```bash
# Terminal 1: 데이터 로거 (Jetson Orin Nano)
ros2 run digital_twin data_logger

# Terminal 2: 디지털 트윈 오케스트레이터 (Desktop)
python3 src/digital_twin/orchestrator.py --start
```

### 6.3 디지털 트윈 루프 전체 구성도

```
┌──────────────────────────────────────────────────────────────────────────┐
│                     DESKTOP (Ubuntu 22.04 + Isaac Sim)                    │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  Digital Twin Orchestrator                                       │   │
│  │  ┌──────────┐  ┌──────────────┐  ┌──────────────────────────┐   │   │
│  │  │ Analyzer │─►│ Retrain      │─►│ Policy Registry          │   │   │
│  │  │ (Gap)    │  │ Pipeline     │  │ (Blue-Green)             │   │   │
│  │  └────┬─────┘  └──────┬───────┘  └────────────┬─────────────┘   │   │
│  │       │               │                        │                 │   │
│  └───────┼───────────────┼────────────────────────┼─────────────────┘   │
│          │               │                        │                     │
│          ▼               ▼                        ▼                     │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  Simulation Baseline (Isaac Lab Evaluation)                      │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────┬───────────────────────────────────┘
                                       │
                          ┌────────────┴────────────┐
                          │                         │
                          ▼                         ▼
┌─────────────────────┐  ┌─────────────────────────────────────────────┐
│   Episode DB         │  │  Blue-Green Deploy                         │
│   (SQLite)           │  │  deployed_policies/                        │
│   data/              │  │  ├── active → policy_v3                   │
│   episode_db.sqlite  │  │  ├── policy_v1/ (backup)                  │
│                      │  │  ├── policy_v2/ (backup)                  │
│                      │  │  └── policy_v3/ (active) ← TensorRT.plan  │
└──────────────────────┘  └──────────────────┬──────────────────────────┘
                                             │
                                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│                   JETSON ORIN NANO (로봇 1)                          │
│                                                                      │
│  ┌────────────────┐  ┌──────────────┐  ┌────────────────────────┐   │
│  │ Data Logger    │  │ Policy       │  │ TensorRT Engine        │   │
│  │ (ROS2 Node)    │─►│ Inference    │─►│ (symlinked to active)  │   │
│  └───────┬────────┘  └──────────────┘  └────────────────────────┘   │
│          │                                                          │
│          ▼                                                          │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  실시간 데이터 수집 (10Hz)                                     │   │
│  │  /scan → /digital_twin/episode_event                         │   │
│  └──────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 7. 성능 지표 (KPI)

| KPI | 목표 | 측정 방법 |
|-----|------|-----------|
| **Success Rate** | > 90% | DB metrics.success 평균 |
| **Sim-to-Real Gap** | < 10% | Sim_SR - Real_SR |
| **재학습 주기** | < 6시간 | Cycle 완료 시간 |
| **배포 시간** | < 1초 | Blue-Green symlink switch |
| **데이터 수집률** | > 100 ep/day | 일일 episode 수 |
| **롤백 시간** | < 1초 | symlink 변경 시간 |
| **정책 개선율** | +2% per cycle | SR 증가분 |

---

## 8. 파일 구조

```
src/digital_twin/
├── data_logger.py             # Phase 7: 실제 로봇 데이터 수집 + Episode DB
├── gap_analyzer.py            # Phase 8: Sim-vs-Real 갭 분석 + 재학습 트리거
├── auto_retrain_pipeline.py   # Phase 9: 6단계 자동 재학습 파이프라인
├── policy_registry.py         # Phase 9: 정책 버전 관리 + 블루-그린 배포
└── orchestrator.py            # Phase 10: 전체 디지털 트윈 중앙 오케스트레이터

config/digital_twin_config.yaml            # 통합 설정 파일
config/policy_registry.json                # 정책 레지스트리 데이터
scripts/deploy_policy.sh                   # 블루-그린 배포 스크립트
```

---

## 9. 문제 해결

| 문제 | 원인 | 해결 |
|------|------|------|
| DB가 비어 있음 | 로봇이 아직 주행하지 않음 | 로봇으로 몇 회 주행 후 확인 |
| 갭 분석 실패 | Sim Baseline 미설정 | `--sim-baseline` 경로 확인 |
| 재학습 실패 | GPU 메모리 부족 | `retrain_config.num_envs` 감소 |
| 배포 후 정책 안 됨 | TensorRT 엔진 문제 | `deploy_policy.sh --rollback` |
| 오케스트레이터 멈춤 | 예외 발생 | `logs/orchestrator/events.jsonl` 확인 |
| 무한 재학습 루프 | 임계값 너무 낮음 | `success_rate_gap_threshold: 0.15`로 조정 |
