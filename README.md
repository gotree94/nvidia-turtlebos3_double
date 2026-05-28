# NVIDIA TurtleBot3 Dual Autonomous Navigation Project

> **NVIDIA Isaac Sim + Cosmos + Isaac Lab 기반 TurtleBot3 자율주행 풀스택 프로젝트**
> **End-to-End Autonomous Navigation + Digital Twin Closed-Loop**

![Project Status](https://img.shields.io/badge/status-production-green)
![NVIDIA Isaac Sim](https://img.shields.io/badge/Isaac_Sim-2025.2-green)
![NVIDIA Cosmos](https://img.shields.io/badge/Cosmos-2.0-blue)
![NVIDIA Isaac Lab](https://img.shields.io/badge/Isaac_Lab-2.1-purple)
![ROS2](https://img.shields.io/badge/ROS2-Humble/Jazzy-orange)
![Digital Twin](https://img.shields.io/badge/Digital_Twin-Closed_Loop-red)

---

* [출력시간 50%단출](https://www.youtube.com/watch?v=UQV_zaTHvro&t=84s)
* [습기먹은 필라멘트로부터의 탈출](https://www.youtube.com/watch?v=91Iqa7-mGgs)
* [Isaac Sim 터틀봇 2대 옴니로봇 3대 움직이기](https://www.youtube.com/watch?v=2te9wUkFXY4)
* [Isaac Sim Camera](https://www.youtube.com/watch?v=0bJ-wqwF87I)
* [Isaac Sim Turtlebot3 불러오소 ROS2 연결하기](https://www.youtube.com/watch?v=aE3CgfdgYBc&t=9s)
* [URDF Import: Turtlebot](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/ros2_tutorials/tutorial_ros2_turtlebot.html)

---

<img src="TOP.png">


## 📋 프로젝트 개요

이 프로젝트는 **NVIDIA 최신 Physical AI 기술 스택**을 활용하여 TurtleBot3 기반 자율주행 시스템의 **전生命周期**를 구현합니다.

| 단계 | 설명 | 핵심 기술 |
|------|------|-----------|
| **① 환경 디지털화** | 실제 공간을 Cosmos로 캡처 | **Cosmos WFM** |
| **② 데이터 증강** | 합성 데이터 생성 + Sim-to-Real 변환 | **Isaac Sim + Cosmos Transfer** |
| **③ 정책 학습** | GPU 가속 PPO 강화학습 | **Isaac Lab** |
| **④ Sim-to-Real** | 학습 정책 → 실제 로봇 Zero-shot 전이 | **TensorRT** |
| **⑤ 이기종 협업** | Jetson Orin + RPi 5 듀얼 로봇 협업 | **ROS2 + Nav2** |
| **⑥ 디지털 트윈** | 실시간 피드백 → 자동 재학습 → 무한 개선 | **Digital Twin Loop** |

### 핵심 기술 스택

| 기술 | 버전 | 역할 |
|------|------|------|
| **NVIDIA Isaac Sim** | 2025.2+ | 물리 기반 로봇 시뮬레이션 (Omniverse, PhysX 5) |
| **NVIDIA Isaac Lab** | 2.1+ | 강화학습 PPO 트레이닝 프레임워크 |
| **NVIDIA Cosmos** | 2.0 | World Foundation Model, 합성 데이터 생성, Transfer, Policy |
| **NVIDIA Jetson Orin Nano** | JetPack 6+ | 실시간 TensorRT 추론 및 엣지 AI 배포 |
| **ROS2** | Humble / Jazzy | 로봇 미들웨어 및 분산 DDS 통신 |
| **Navigation2 (Nav2)** | 최신 | 경로 계획 및 제어 |
| **Digital Twin** | SQLite + Auto ML | 실시간 데이터 수집 → 갭 분석 → 자동 재학습 → Blue-Green 배포 |

---

## 🔄 전체 파이프라인

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                          DIGITAL TWIN CLOSED-LOOP                                     │
│                                                                                       │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐        │
│  │  Cosmos  │───►│  Isaac   │───►│  Policy  │───►│  Sim-to- │───►│  Dual    │        │
│  │  Reality │    │  Sim     │    │  Training│    │  Real    │    │  Robot   │        │
│  │  Capture │    │  + Data  │    │  (RL)    │    │  Transfe │    │  Deploy  │        │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘        │
│       │               │               │               │               │              │
│       └───────────────┴───────────────┴───────────────┴───────────────┘              │
│                                       │                                              │
│                                       ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────────────────┐   │
│  │                     Digital Twin Loop (자동화 피드백)                         │   │
│  │                                                                              │   │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌───────────┐  │   │
│  │  │  Data Logger │───►│ Gap Analyzer │───►│ Auto Retrain │───►│ Blue-Green│  │   │
│  │  │  (Episode DB)│    │ (Sim vs Real)│    │ Pipeline     │    │  Deploy   │  │   │
│  │  └──────────────┘    └──────────────┘    └──────────────┘    └───────────┘  │   │
│  │                                                                              │   │
│  └──────────────────────────────────────────────────────────────────────────────┘   │
│                                       │                                              │
│                                       ▼                                              │
│                           실제 로봇 → 지속적 개선 (∞)                                  │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 프로젝트 구조 (34 files)

```
nvidia-turtlebos3_double/
│
├── README.md                          # 프로젝트 개요 ◀◀◀ 지금 읽는 중
│
├── docs/                              # ===== 전체 문서 =====
│   ├── 01_prerequisites.md            # 사전 요구사항, 하드웨어 배선, 아키텍처
│   ├── 02_environment_setup.md        # Isaac Sim/Isaac Lab/Cosmos/ROS2/Jetson 설치
│   ├── 03_urdf_modeling.md            # TurtleBot3 Burger URDF 분석 및 USD 변환
│   ├── 04_isaac_sim.md                # Isaac Sim 시뮬레이션 + ROS2 Bridge + Nav2
│   ├── 05_cosmos_integration.md       # CosmosWriter → Transfer → Policy 파이프라인
│   ├── 06_rl_training.md              # Isaac Lab PPO 학습 (보상함수/환경/정책)
│   ├── 07_inference.md                # Jetson Orin Nano TensorRT 실시간 추론
│   ├── 08_dual_robot.md               # RPi 5 + Jetson 이기종 듀얼 로봇 시스템
│   ├── 09_experiments.md              # 6단계 실험 가이드 + 문제해결 체크리스트
│   ├── 10_architecture_overview.md    # 전체 파이프라인 이해를 위한 종합 개요
│   └── 11_digital_twin_loop.md        # 📌 Digital Twin Closed-Loop 상세
│
├── src/                               # ===== 소스 코드 =====
│   ├── urdf/                          # TurtleBot3 URDF (Jetson/RPi 마운트 포함)
│   │   └── turtlebot3_burger.urdf
│   │
│   ├── isaac_sim/                     # Isaac Sim 시뮬레이션 스크립트
│   │   ├── setup_simulation.py        #   시뮬레이션 환경 설정
│   │   └── cosmos_sdg_pipeline.py     #   CosmosWriter 합성 데이터 생성
│   │
│   ├── isaac_lab/                     # Isaac Lab RL 학습
│   │   └── train_turtlebot_navigation.py  # PPO 학습 실행
│   │
│   ├── deployment/                    # 실제 로봇 배포
│   │   ├── jetson_inference_node.py   #   TensorRT 정책 추론 (실행 가능)
│   │   └── multi_robot_launch.py      #   듀얼 로봇 시스템 런치
│   │
│   └── digital_twin/                  # 📌 디지털 트윈 코어 (5개 모듈)
│       ├── data_logger.py             #   Phase 7: 실제 주행 데이터 수집 → SQLite
│       ├── gap_analyzer.py            #   Phase 8: Sim-vs-Real 갭 분석 + 재학습 트리거
│       ├── auto_retrain_pipeline.py   #   Phase 9: 6단계 자동 재학습 파이프라인
│       ├── policy_registry.py         #   Phase 9: 정책 버전 관리 + 블루-그린 배포
│       └── orchestrator.py            #   Phase 10: 중앙 오케스트레이터
│
├── config/                            # ===== 설정 파일 =====
│   ├── nav2_params.yaml               #   TurtleBot3 최적화 Nav2
│   ├── nav2_light_params.yaml         #   RPi 5 경량 Nav2
│   ├── cosmos_config.yaml             #   Cosmos 통합 설정
│   └── digital_twin_config.yaml       # 📌 디지털 트윈 통합 설정
│
├── docker/                            # ===== Docker =====
│   ├── Dockerfile.isaac               #   Isaac Lab + ROS2 Humble 도커
│   └── docker-compose.yaml            #   전체 서비스 오케스트레이션
│
├── scripts/                           # ===== 자동화 스크립트 =====
│   ├── setup_host.sh                  #   Ubuntu 22.04 호스트 자동 셋업
│   ├── setup_jetson.sh                #   Jetson Orin Nano 셋업
│   ├── run_training.sh                #   학습 → ONNX → TensorRT 파이프라인
│   ├── evaluate_sim2real.py           #   Sim-to-Real 갭 평가
│   └── deploy_policy.sh               # 📌 블루-그린 배포 스크립트
│
├── assets/                            # 추가 리소스
└── data/                              # Episode DB, Training sets (런타임 생성)
```

---

## 🚀 빠른 시작

### 1. 시스템 요구사항

| 구성 요소 | 최소 사양 | 권장 사양 | 보유 현황 🖥️ |
|-----------|-----------|-----------|---------------|
| **GPU** | NVIDIA RTX 3060 (12GB) | **NVIDIA RTX 4090 (24GB)** | **NVIDIA RTX 5090 (24GB)** ✅ |
| **CPU** | Intel i7-12xxx / AMD Ryzen 7 | Intel i9 / AMD Ryzen 9 | Core Ultra 9 ✅ |
| **RAM** | 32GB | **64GB** | **64GB** ✅ |
| **Storage** | 100GB | 500GB NVMe SSD | **4TB** ✅ |
| **OS** | **Ubuntu 22.04 LTS** | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS ✅ |
| **Docker** | 24+ | 24+ | - |

> **보유 장비**: ASUS 2025 ROG Strix SCAR 16 (코어 Ultra 9, NVIDIA RTX 5090 24GB, 4TB, 64GB, Ubuntu 22.04 LTS)
>
> ⚠️ 만약 **RAM 32GB**는 Isaac Lab 대규모 병렬 학습(256 env) 시 부족할 수 있습니다. `--num_envs 64`로 조정하거나 SWAP을 활용하세요. RTX 5090 24GB는 권장 사양을 상회하므로 GPU 병목은 없습니다.

### 2. 설치 개요

```bash
# 1. 저장소 준비
git clone <this-repo> nvidia-turtlebos3_double
cd nvidia-turtlebos3_double

# 2. 호스트 환경 자동 설정
bash scripts/setup_host.sh     # NVIDIA driver, CUDA, Docker, ROS2, Conda

# 3. Isaac Sim Docker 이미지
docker pull nvcr.io/nvidia/isaac-sim:2025.2.0

# 4. Isaac Lab 설치
conda activate isaaclab
cd ~/IsaacLab && ./isaaclab.sh --install

# 5. TurtleBot3 ROS2 패키지
mkdir -p ~/tb3_ws/src && cd ~/tb3_ws/src
git clone -b humble https://github.com/ROBOTIS-GIT/turtlebot3.git
cd ~/tb3_ws && colcon build --symlink-install
```

### 3. 전체 실행 워크플로우

```bash
# Step 1: 시뮬레이션 (Desktop)
docker compose -f docker/docker-compose.yaml up isaac-sim
/isaac-sim/python.sh src/isaac_sim/setup_simulation.py

# Step 2: RL 학습 (Desktop)
python src/isaac_lab/train_turtlebot_navigation.py --num_envs 256 --headless

# Step 3: 정책 변환
bash scripts/run_training.sh        # .pt → .onnx → .plan

# Step 4: 실제 로봇 배포 (Jetson Orin Nano)
python3 src/deployment/jetson_inference_node.py \
    --model_path outputs/policy/turtlebot_policy.plan

# Step 5: 디지털 트윈 자동화
python3 src/digital_twin/orchestrator.py --start
```

---

## 🧠 기술 아키텍처

### 시스템 통합 구성

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                        DGX / Desktop (Ubuntu 22.04)                               │
│                                                                                    │
│  ┌─────────────────┐  ┌──────────────┐  ┌────────────────────┐  ┌─────────────┐  │
│  │   Isaac Sim     │  │  Isaac Lab   │  │    Cosmos Suite    │  │ Digital Twin│  │
│  │  (Simulation)   │  │(RL Training) │  │  (WFM + Transfer)  │  │ Orchestrator│  │
│  │  + ROS2 Bridge  │  │  + PPO       │  │  + Data Pipeline   │  │ + Gap       │  │
│  └────────┬────────┘  └──────┬───────┘  └─────────┬──────────┘  │  Analyzer   │  │
│           │                  │                     │             └──────┬──────┘  │
│           └──────────────────┼─────────────────────┼───────────────────┘         │
│                              │                     │                             │
│                              ▼                     ▼                             │
│                    ┌─────────────────────────────────────┐                       │
│                    │        Policy Export Pipeline        │                       │
│                    │  .pt → .onnx → .plan (TensorRT FP16) │                       │
│                    └─────────────────────────────────────┘                       │
└─────────────────────────────────────┬───────────────────────────────────────────┘
                                      │
                          ┌───────────┴───────────┐
                          │                       │
                          ▼                       ▼
┌─────────────────────┐  ┌─────────────────────────────────────────────────────┐
│    Episode DB       │  │           AGX / Jetson Orin Nano                     │
│    (SQLite)         │  │  ┌─────────────────────────────────────────────┐    │
│    data/            │  │  │  Policy Inference (TensorRT, ~5ms)          │    │
│    episode_db.sqlite│  │  │  Data Logger (10Hz) → Episode DB            │    │
└──────────┬──────────┘  │  └─────────────────────────────────────────────┘    │
           │             │                        │                            │
           │             │                        ▼                            │
           │             │  ┌─────────────────────────────────────────────┐    │
           │             │  │  Robot 1: Jetson Orin Nano (Leader)         │    │
           │             │  │  • RL Policy 추론   • TensorRT              │    │
           │             │  └─────────────────────────────────────────────┘    │
           │             └──────────────────┬──────────────────────────────────┘
           │                                │ ROS2 DDS (Domain ID: 42)
           │                                ▼
           │              ┌─────────────────────────────────────────────────────┐
           │              │  Robot 2: Raspberry Pi 5 (Follower)                 │
           │              │  • Nav2 경량    • SLAM 경량    • Formation Control  │
           └──────────────┴─────────────────────────────────────────────────────┘
```

### 디지털 트윈 루프 상세

```
[실제 로봇 주행] ──10Hz──► [Data Logger] ──SQLite──► [Episode DB]
                                                           │
                                                           ▼
                                                    [Gap Analyzer]
                                                    (5분 주기)
                                                           │
                                                   [Gap > 15%?]
                                                    │        │
                                                  Yes        No ──→ 모니터링 유지
                                                    │
                                                    ▼
                                            [Auto Retrain Pipeline]
                                             ① Data Collection
                                             ② Isaac Lab Fine-tune
                                             ③ Sim Evaluation
                                             ④ ONNX Export
                                             ⑤ TensorRT FP16
                                             ⑥ Blue-Green Deploy
                                                    │
                                                    ▼
                                           [Policy Registry]
                                            (버전 관리 + 롤백)
                                                    │
                                                    ▼
                                          [새 정책 → 로봇 배포]
                                                    │
                                                    └──→ 다시 모니터링 (∞)
```

---

## 📚 문서 로드맵

| # | 문서 | 설명 | 난이도 | 주요 코드 |
|---|------|------|--------|----------|
| 01 | [사전 요구사항](docs/01_prerequisites.md) | 시스템 구성, 아키텍처, 하드웨어 배선 | ⭐ | - |
| 02 | [환경 설정](docs/02_environment_setup.md) | Isaac Sim, ROS2, Cosmos, Jetson 설치 | ⭐⭐ | Docker, setup scripts |
| 03 | [URDF 모델링](docs/03_urdf_modeling.md) | TurtleBot3 URDF 구조, USD 변환 | ⭐⭐ | `turtlebot3_burger.urdf` |
| 04 | [Isaac Sim](docs/04_isaac_sim.md) | 시뮬레이션 환경, 센서, ROS2 브릿지 | ⭐⭐⭐ | `setup_simulation.py` |
| 05 | [Cosmos 통합](docs/05_cosmos_integration.md) | 합성 데이터 생성, Transfer, Policy | ⭐⭐⭐ | `cosmos_sdg_pipeline.py` |
| 06 | [RL 학습](docs/06_rl_training.md) | Isaac Lab PPO, 보상 함수, 환경 | ⭐⭐⭐⭐ | `train_turtlebot_navigation.py` |
| 07 | [추론 및 배포](docs/07_inference.md) | Jetson Orin Nano TensorRT 실시간 추론 | ⭐⭐⭐ | `jetson_inference_node.py` |
| 08 | [듀얼 로봇](docs/08_dual_robot.md) | RPi + Jetson 이기종 협업 시스템 | ⭐⭐⭐⭐ | `multi_robot_launch.py` |
| 09 | [실험 가이드](docs/09_experiments.md) | 6단계 테스트 계획, 문제 해결 | ⭐⭐ | `evaluate_sim2real.py` |
| 10 | [아키텍처 개요](docs/10_architecture_overview.md) | 전체 파이프라인 종합 이해 | ⭐ | - |
| **11** | **[디지털 트윈](docs/11_digital_twin_loop.md)** | **📌 자동 피드백 Closed-Loop** | ⭐⭐⭐⭐ | `digital_twin/*.py` |

---

## 🔬 주요 특징

### 1. Cosmos 기반 합성 데이터 증강
Isaac Sim + CosmosWriter로 5종 모달리티(RGB/Depth/Seg/Edge) 수집 → Cosmos-Transfer로 현실감 있는 데이터 변환

### 2. GPU 가속 Isaac Lab PPO 학습
256개 병렬 환경에서 동시 학습, Domain Randomization으로 Sim-to-Real 격차 해소

### 3. Zero-shot Sim-to-Real 전이
TensorRT FP16 최적화로 Jetson Orin Nano에서 5ms 추론, 추가 학습 없이 실제 로봇 즉시 운용

### 4. 이기종 듀얼 로봇 협업
Jetson Orin Nano(Leader, RL Policy) + Raspberry Pi 5(Follower, Nav2) Formation Control

### 5. **Digital Twin Closed-Loop (★)**
실제 주행 데이터 → Gap 분석 → 자동 재학습 → Blue-Green 배포의 완전 자동화 루프

---

## 📊 프로젝트 규모

| 항목 | 값 |
|------|-----|
| **총 파일 수** | 34 |
| **문서** | 11개 (마크다운) |
| **소스 코드** | 9개 (Python) |
| **설정 파일** | 4개 (YAML) |
| **스크립트** | 5개 (Shell/Python) |
| **Docker** | 2개 |
| **총 용량** | ~300KB |

---

## 📄 라이선스

이 프로젝트는 교육 및 연구 목적으로 제공됩니다. 각 구성 요소(NVIDIA, ROS2, TurtleBot3)의 라이선스를 따릅니다.

---

*이 프로젝트는 NVIDIA의 최신 Physical AI 기술 스택(Isaac Sim, Isaac Lab, Cosmos, TensorRT, Jetson)을 기반으로 구축되었습니다.*
