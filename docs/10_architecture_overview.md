# 10. 프로젝트 아키텍처 개요

> **Cosmos → Isaac Sim → RL Training → Sim-to-Real → Dual Robot → Digital Twin**
> 전체 파이프라인을 이해하기 쉽게 설명합니다.

---

## 한 문장 요약

> **Cosmos로 실제 환경을 디지털화 → Isaac Sim에서 합성 데이터 증강 → RL 학습 → Sim-to-Real 전이 → Jetson + RPi 이기종 듀얼 로봇 협업 → 디지털 트윈 피드백 루프**

---

## 1. 전체 흐름 (6단계 파이프라인)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DIGITAL TWIN LOOP                                    │
│                                                                             │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐ │
│  │  Cosmos  │──►│  Isaac   │──►│  Policy  │──►│  Sim-to- │──►│  Dual    │ │
│  │  Reality │   │  Sim     │   │  Training│   │  Real    │   │  Robot   │ │
│  │  Capture │   │  + Data  │   │  (RL)    │   │  Transfe │   │  Deploy  │ │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘ │
│       │              │              │              │              │        │
│       └──────────────┴──────────────┴──────────────┴──────────────┘        │
│                                    │                                       │
│                                    ▼                                       │
│                         실제 환경 피드백 → 디지털 트윈 업데이트                │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Stage 1: Cosmos Reality Capture (실제 환경 디지털화)

실제 주행 공간(실내 3m × 3m)의 데이터를 **NVIDIA Cosmos**로 수집합니다.

```
[실제 환경]                    [Cosmos Capture]
  ┌──────────┐                 ┌──────────────┐
  │ 책상      │                 │ RGB Video    │
  │ 의자      │──Camera/LiDAR──►│ Depth Map    │
  │ 벽        │                 │ Segmentation │
  │ 장애물    │                 │ Edge Map     │
  └──────────┘                 └──────────────┘
```

| Cosmos 모듈 | 역할 | 출력 |
|------------|------|------|
| **Cosmos-Predict2** | Video2World 모델 | 입력 영상의 미래 프레임 예측 |
| **Cosmos-Transfer** | Multi-ControlNet | Isaac Sim 합성 데이터 → 사실적 변환 |
| **Cosmos-Reason** | 물리적 추론 VLM | 장면 이해, 충돌 위험 추론 |
| **CosmosWriter** | Isaac Sim 플러그인 | 5종 모달리티(RGB/Depth/Seg/Edge) 동기화 수집 |

> **포인트**: Cosmos는 단순 센서 기록이 아니라 **World Foundation Model**로 환경의 물리적 구조까지 이해합니다.

---

## 3. Stage 2: Isaac Sim + Data Augmentation (시뮬레이션 데이터 증강)

Cosmos 데이터를 기반으로 **Isaac Sim**에서 가상 환경을 구축하고 데이터를 증강합니다.

```
Cosmos 원본 데이터
       │
       ▼
┌────────────────────────────────────────────────────┐
│              Isaac Sim 가상 환경                     │
│                                                     │
│  • Cosmos 데이터로 환경 재현                          │
│  • 조명/날씨/텍스처를 Domain Randomization           │
│  • Cosmos-Transfer로 Sim→Real 품질 향상             │
│                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ 환경 #1  │  │ 환경 #2  │  │ 환경 #N  │  ...      │
│  │ (원본)   │  │ (변형1)  │  │ (변형N)  │          │
│  └──────────┘  └──────────┘  └──────────┘          │
│                                                     │
│  **256개 병렬 환경** → 학습 효율 256배                │
└────────────────────────────────────────────────────┘
```

| 기술 | 적용 내용 |
|------|----------|
| **Isaac Sim 2025.2** | URDF→USD 변환, PhysX 5 물리 엔진 |
| **Cosmos-Transfer** | 합성 RGB + Edge → 사실적인 텍스처 변환 |
| **Domain Randomization** | 마찰(0.3~1.5), 질량(0.7~1.3x), 센서 노이즈(2cm) |
| **Isaac Lab Manager** | 256개 병렬 환경, GPU 가속 리셋 |

> **포인트**: 실제 환경 1개 → 시뮬레이션에서 **수백 가지 변형 환경**을 생성합니다. 이것이 "데이터 증폭"의 핵심입니다.

---

## 4. Stage 3: RL Training (강화학습)

Isaac Lab에서 PPO(Proximal Policy Optimization) 알고리즘으로 자율주행 정책을 학습합니다.

```
관측 (Observation)                     행동 (Action)
┌──────────────┐                      ┌──────────────┐
│ LiDAR 360°   │                      │ 선속도       │
│ 목표 위치    │───[Policy Network]───►│ 각속도       │
│ Heading Err  │                      │              │
└──────────────┘                      └──────────────┘
         │                                  │
         ▼                                  ▼
┌──────────────────────────────────────────────┐
│            Reward Function                    │
│  ✅ 목표 도달 (+10)  ❌ 충돌 (-10)            │
│  📈 진행 보상 (+5)   🔄 회전 패널티 (-0.1)    │
└──────────────────────────────────────────────┘
```

### 신경망 구조

```
Observation (39 dims)
    │
[Linear 256 → ELU]
    │
[Linear 128 → ELU]
    │
[Linear 64  → ELU]
    │
┌────┴────┐
│  Mean   │  Std
│  (2)    │  (2)
└────┬────┘
    Action: [linear_vel, angular_vel]
```

### PPO 하이퍼파라미터

| 파라미터 | 값 | 설명 |
|---------|-----|------|
| 병렬 환경 | 256 | GPU 가속 벡터화 |
| 학습률 | 3.0e-4 | Adam optimizer |
| 할인율(γ) | 0.99 | 장기 보상 고려 |
| GAE(λ) | 0.95 | 편향-분산 트레이드오프 |
| 클리핑(ε) | 0.2 | 정책 업데이트 안정화 |

> **포인트**: 시뮬레이션에서만 수백만 번 충돌해보면서 스스로 주행 방법을 학습합니다.

---

## 5. Stage 4: Sim-to-Real Transfer (시뮬레이션 → 실제 전이)

학습된 정책을 실제 로봇에 배포합니다.

```
Isaac Sim                     실제 Jetson Orin Nano
┌────────────┐                ┌────────────────────┐
│ Policy     │──ONNX 변환──►  │ TensorRT Engine   │
│ PyTorch    │──FP16 최적화→  │ 5ms 추론          │
│            │                │ 실시간 제어        │
└────────────┘                └────────────────────┘
       │                              │
       ▼                              ▼
Domain Randomization           Zero-shot Transfer
• 마찰 랜덤화                  • 추가 학습 없이
• 질량 랜덤화                  • 시뮬레이션 정책을
• 센서 노이즈                   • 실제 로봇에 즉시 적용
• 조명 변화                   
```

### 변환 파이프라인

```
PyTorch (.pt)
    │
    ▼
[torch.onnx.export]
    │
ONNX (.onnx)
    │   opset=17, fp32
    ▼
[TensorRT trtexec]
    │   --fp16, --workspace=4096
    ▼
TensorRT (.plan) ───► Jetson Orin Nano (5ms 추론)
```

### 추론 성능 비교

| 플랫폼 | 추론 시간 | 전력 | 실시간 가능 |
|--------|-----------|------|-----------|
| RTX 4090 | 0.5ms | 350W | ✅ |
| Jetson Orin Nano (FP16) | 5ms | 15W | ✅ |
| Jetson Orin Nano (INT8) | 3ms | 15W | ✅ |
| Raspberry Pi 5 (CPU) | 150ms | 5W | ❌ |

> **포인트**: Domain Randomization 덕분에 **별도 재학습 없이** 시뮬레이션 정책이 실제 로봇에서 바로 동작합니다(Zero-shot Transfer).

---

## 6. Stage 5: Dual Robot Collaboration (듀얼 로봇 협업)

Jetson Orin Nano와 Raspberry Pi 5로 구성된 이기종 듀얼 로봇 시스템이 협업합니다.

```
┌──────────────────────────────────────────────────┐
│              ROS2 DDS 네트워크                     │
│                                                   │
│   ┌─────────────────┐     ┌─────────────────┐    │
│   │  Robot 1        │     │  Robot 2        │    │
│   │  (Jetson Orin)  │     │  (Raspberry Pi 5)│    │
│   │─────────────────│     │─────────────────│    │
│   │  • RL 정책 추론  │     │  • Nav2 경량    │    │
│   │  • TensorRT     │     │  • SLAM 경량    │    │
│   │  • 리더 역할    │◄───►│  • 팔로워 역할  │    │
│   │  • 고성능       │     │  • 저전력       │    │
│   └─────────────────┘     └─────────────────┘    │
│            │                      │               │
│            ▼                      ▼               │
│   ┌──────────────────────────────────────────┐   │
│   │  Formation Controller                    │   │
│   │  • Column (일렬)   • Line (횡대)         │   │
│   │  • Diamond (대각)  • Staggered (지그재그) │   │
│   └──────────────────────────────────────────┘   │
└──────────────────────────────────────────────────┘
```

### 로봇별 역할 분담

| 기능 | Robot 1 (Jetson Orin Nano) | Robot 2 (Raspberry Pi 5) |
|------|---------------------------|--------------------------|
| **정책 추론** | TensorRT 고속 (5ms) | Nav2 경로 계획 |
| **전력** | 25W (MAXN 모드) | 5W |
| **네트워크** | Gigabit Ethernet | Wi-Fi 6 |
| **ROS2** | Humble | Jazzy |
| **역할** | 리더 (Leader) | 팔로워 (Follower) |

### 대형(Formation) 유형

```
Column (일렬)        Line (횡대)         Diamond (대각)     Staggered (지그재그)
  ● 리더           ●──────────●           ●                  ●
  ● 팔로워          0.8m               ●   ●                  ●
  0.8m                                      0.8m
```

> **포인트**: Jetson(고성능) + RPi(경량)의 **이기종 협업**. 각자의 강점을 살려 하나의 시스템처럼 동작합니다.

---

## 7. Stage 6: Digital Twin Loop (디지털 트윈 피드백)

실제 주행 데이터가 다시 학습 파이프라인으로 피드백되어 지속적으로 개선됩니다.

```
                    ┌─────────────────────┐
                    │    PHYSICAL WORLD   │
                    │  ┌───────────────┐  │
                    │  │ Dual Robot    │  │
                    │  │ 실제 주행      │  │
                    │  └───────┬───────┘  │
                    │          │ 실시간 데이터  │
                    └──────────┼──────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────┐
│              DIGITAL TWIN                        │
│                                                   │
│  ┌───────────────────────────────────────────┐    │
│  │  Continuous Improvement Loop               │    │
│  │                                            │    │
│  │  ① 실제 주행 데이터 수집 (궤적, 충돌, 속도)  │    │
│  │  ② Cosmos 정책 업데이트                     │    │
│  │  ③ Isaac Sim에서 재시뮬레이션                │    │
│  │  ④ 발견된 문제점 보완 (추가 학습)             │    │
│  │  ⑤ 개선된 정책 재배포 → ①로 귀환             │    │
│  └───────────────────────────────────────────┘    │
│                                                   │
│  • 실제 환경의 모든 변화가 디지털 공간에 반영        │
│  • 시뮬레이션에서 먼저 테스트 후 실제 적용           │
│  • 시간이 갈수록 정책이 지속적으로 개선              │
└─────────────────────────────────────────────────┘
```

> **포인트**: 여기서 끝이 아닙니다. 실제 주행 데이터가 다시 Cosmos로 들어가서 **디지털 트윈이 스스로 진화하는 루프**를 만듭니다.

---

## 8. 기술 매핑 요약

| 단계 | NVIDIA 기술 | 담당 역할 | 사용자 관점 |
|------|------------|-----------|------------|
| **환경 Capture** | **Cosmos** | 실제 환경을 WFM으로 이해 | 카메라로 공간 스캔 |
| **데이터 증강** | **Isaac Sim + Cosmos Transfer** | 1개 환경 → 256개 변형 | 다양한 조건에서 학습 |
| **정책 학습** | **Isaac Lab (PPO)** | 충돌 없이 수백만 회 학습 | 기다리기만 하면 됨 |
| **Sim→Real** | **TensorRT** | 시뮬레이션 정책 → 실제 로봇 | 정책 파일 복사 |
| **협업 주행** | **ROS2 + Nav2** | 2대 로봇 동시 제어 | 대형 지령 하나로 |
| **디지털 트윈** | **전체 스택 통합** | 지속적 개선 루프 | 로봇이 스스로 발전 |

---

## 9. 기대 효과

### 전통적 방식 vs 본 프로젝트

| 항목 | 전통적 방식 | 본 프로젝트 |
|------|------------|------------|
| **학습 방식** | 실제 로봇으로 1000번 충돌하며 학습 (로봇 파손 위험) | 시뮬레이션에서 수백만 번 학습 후 Zero-shot 전이 |
| **소요 시간** | 약 3개월 | 약 3일 |
| **로봇 대수** | 1대 단독 운용 | 2대 협업 (Jetson + RPi) |
| **주행 능력** | 단순 장애물 회피 | 대형 유지 + SLAM + 충돌 회피 |
| **유지보수** | 수동 재학습 필요 | 자동 디지털 트윈 루프로 지속 개선 |
| **확장성** | 환경 바뀌면 처음부터 재학습 | Cosmos 재캡처 + 재시뮬레이션으로 빠른 적응 |

---

## 10. 프로젝트 구성도

```
nvidia-turtlebos3_double/
├── README.md                        # ← 이 문서의 개요
├── docs/
│   ├── 01_prerequisites.md          # 시스템 요구사항, 하드웨어 배선
│   ├── 02_environment_setup.md      # Isaac Sim/Isaac Lab/Cosmos/ROS2 설치
│   ├── 03_urdf_modeling.md          # TurtleBot3 URDF 분석 및 USD 변환
│   ├── 04_isaac_sim.md              # 시뮬레이션 환경 + ROS2 Bridge + Nav2
│   ├── 05_cosmos_integration.md     # CosmosWriter → Transfer → Policy
│   ├── 06_rl_training.md            # Isaac Lab PPO 학습 (환경/보상/정책)
│   ├── 07_inference.md              # Jetson TensorRT 배포
│   ├── 08_dual_robot.md             # RPi + Jetson 듀얼 로봇
│   ├── 09_experiments.md            # 6단계 테스트 계획
│   └── 10_architecture_overview.md  # ← 지금 읽고 있는 문서
├── src/                             # 실행 가능한 소스 코드
├── config/                          # Nav2, Cosmos 설정 파일
├── docker/                          # Docker 컨테이너 구성
└── scripts/                         # 설치, 학습, 평가 자동화 스크립트
```

---

## 참고: 단계별 문서 연결

```
Stage 1: Cosmos Reality Capture    → docs/05_cosmos_integration.md
Stage 2: Isaac Sim + Augmentation  → docs/04_isaac_sim.md + docs/05_cosmos_integration.md
Stage 3: RL Training               → docs/06_rl_training.md
Stage 4: Sim-to-Real Transfer      → docs/07_inference.md
Stage 5: Dual Robot Collaboration  → docs/08_dual_robot.md
Stage 6: Digital Twin Loop         → docs/09_experiments.md (Continuous Improvement)
```
