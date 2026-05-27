# Isaac Sim + Cosmos + Isaac Lab 기반 TurtleBot3 자율주행 풀스택 프로젝트
## 전문가 검토 의견 + 상세 개발 자료

> **대상 시스템**: ASUS ROG Strix SCAR 16 (RTX 5090 24GB, Core Ultra 9, 64GB RAM, Ubuntu 22.04)
> **프로젝트 수준**: 연구/포트폴리오 → 컨설팅 제안용 레퍼런스 시스템

---

## 목차

1. [전문가 종합 검토 의견](#1-전문가-종합-검토-의견)
2. [기술 실현 가능성 분석](#2-기술-실현-가능성-분석)
3. [단계별 상세 개발 가이드](#3-단계별-상세-개발-가이드)
4. [핵심 소스코드 레퍼런스](#4-핵심-소스코드-레퍼런스)
5. [디지털 트윈 루프 구현](#5-디지털-트윈-루프-구현)
6. [Sim-to-Real 갭 분석 방법론](#6-sim-to-real-갭-분석-방법론)
7. [성능 벤치마크 기준표](#7-성능-벤치마크-기준표)
8. [교육 커리큘럼 연계 방안](#8-교육-커리큘럼-연계-방안)
9. [컨설팅 제안서 핵심 포인트](#9-컨설팅-제안서-핵심-포인트)
10. [알려진 기술적 도전과 해결책](#10-알려진-기술적-도전과-해결책)

---

<img src="011.png" width="110%">


## 1. 전문가 종합 검토 의견

### 1.1 프로젝트 아키텍처 평가

**[강점 — 매우 우수한 부분]**

| 평가 항목 | 점수 | 근거 |
|-----------|------|------|
| 기술 스택 최신성 | ★★★★★ | Isaac Sim 2025.2 + Cosmos 2.0 + Isaac Lab 2.1은 현재 NVIDIA Physical AI의 최정점 |
| 파이프라인 완결성 | ★★★★☆ | Capture → Train → Deploy → Feedback 완전 루프 설계 우수 |
| 하드웨어 적합성 | ★★★★★ | RTX 5090은 모든 단계에서 병목 없음 (Isaac Sim 실시간 + 256-env RL 동시 가능) |
| 교육 포트폴리오 가치 | ★★★★★ | 국내 제조/스마트팩토리 컨설팅 시장에서 차별화된 레퍼런스 |
| Digital Twin 설계 | ★★★★☆ | Blue-Green 배포까지 포함한 완성도 높은 설계 |

**[개선 권장 사항 — 현실적 도전 요소]**

1. **Cosmos 2.0 API 안정성**: WFM(World Foundation Model) 및 Transfer 기능은 2025년 현재 엔터프라이즈 라이선스 필요. `cosmos-transfer1` 모델은 NGC 접근 필수이므로 사전 라이선스 확인이 중요합니다.

2. **Zero-shot Sim-to-Real 전이 현실성**: TurtleBot3 Burger 수준에서 Nav2 + RL 하이브리드로 상당 수준 달성 가능하나, 완전 Zero-shot은 도메인 랜덤화(DR)를 충분히 적용해야 합니다. 현실적으로 3~5회의 미세조정(fine-tuning) 이터레이션이 필요합니다.

3. **Digital Twin 갭 분석 15% 임계값**: 절대값보다 상황별 가중치가 더 중요합니다. 충돌 회피 갭과 경로 정확도 갭의 가중치를 다르게 설정해야 합니다.

4. **Jetson Orin Nano 메모리 제약**: 8GB 모델 기준 TensorRT FP16 정책 모델 + ROS2 + Nav2 동시 실행 시 OOM 위험이 있습니다. `jetson_clocks` + SWAP 16GB 설정을 권장합니다.

5. **RPi 5 + Jetson 이기종 DDS 통신**: Domain ID 42로 분리해도 Wi-Fi 환경에서 지연이 발생할 수 있습니다. 유선 이더넷 브릿지(USB-to-Ethernet) 또는 5GHz Wi-Fi 전용 설정을 권장합니다.

### 1.2 아키텍처 수정 제안

기존 5단계 파이프라인에 **실패 안전(Fail-safe) 레이어**를 추가하는 것을 권장합니다:

```
기존: Cosmos → Isaac Sim → Isaac Lab → TensorRT → 배포
제안: Cosmos → Isaac Sim → Isaac Lab → TensorRT → [검증 레이어] → 배포
                                                         ↑
                                              Safety Checker (충돌 예측 시뮬레이션)
                                              Policy Evaluator (성능 임계값 통과 여부)
                                              Rollback Trigger (이상 감지 시 자동 롤백)
```

---

## 2. 기술 실현 가능성 분석

### 2.1 버전별 호환성 매트릭스

```
Isaac Sim 2025.2  ←── 의존 ──→  CUDA 12.4+  ──→  RTX 5090 (Blackwell) ✅
Isaac Lab 2.1     ←── 의존 ──→  Isaac Sim 2025.x  ✅
Cosmos 2.0        ←── 의존 ──→  PyTorch 2.3+ / CUDA 12.x  ✅
ROS2 Humble       ←── 대상 ──→  Ubuntu 22.04 LTS  ✅
ROS2 Jazzy        ←── 대상 ──→  Ubuntu 24.04 LTS  (별도 설치 필요)
JetPack 6.x       ←── 대상 ──→  Jetson Orin Nano  (별도 장치)
```

> ⚠️ **주의**: Isaac Sim 2025.2는 RTX 5090 (Blackwell SM_90) 지원을 공식 확인했으나,
> 일부 OptiX 레이트레이싱 기능은 드라이버 570+ 필요합니다.

### 2.2 리소스 요구량 추정 (RTX 5090 24GB 기준)

| 작업 | GPU VRAM | 시스템 RAM | 예상 시간 |
|------|----------|------------|-----------|
| Isaac Sim 실시간 (HeadFull) | 8~12GB | 16GB | - |
| Isaac Lab PPO (256 env) | 16~20GB | 24GB | ~4시간/1M step |
| Cosmos-Transfer (1080p) | 18~22GB | 32GB | ~5분/장면 |
| TensorRT 변환 (.pt→.plan) | 4GB | 8GB | ~10분 |
| Digital Twin 전체 스택 | 4GB (추론) | 8GB | 상시 |

> RTX 5090 24GB는 모든 단계 개별 실행 기준 여유 있습니다.
> Isaac Sim + Isaac Lab 동시 실행 시 VRAM 한계에 근접할 수 있으므로 주의.

### 2.3 Cosmos 2.0 실제 활용 경로

Cosmos 2.0에는 크게 3가지 활용 경로가 있습니다:

**경로 A — CosmosWriter (Isaac Sim 내장, 즉시 사용 가능)**
```python
# Isaac Sim 내에서 합성 데이터 생성 (Cosmos 라이선스 불필요)
from isaacsim.replicator.cosmos import CosmosWriter
writer = CosmosWriter(output_dir="/data/synthetic")
writer.write(rgb=True, depth=True, semantic_seg=True)
```

**경로 B — Cosmos-Transfer (NGC 라이선스 필요)**
```bash
# Cosmos-Transfer1-7B: Sim → Real 도메인 변환
# https://catalog.ngc.nvidia.com/orgs/nvidia/teams/cosmos/models/cosmos-transfer1
ngc registry model download-version nvidia/cosmos/cosmos-transfer1:1.0
```

**경로 C — Cosmos-Predict (World Foundation Model, 상용 API)**
```python
# 실제 환경 영상으로 미래 상태 예측 (Closed-Loop 검증용)
import cosmos
model = cosmos.WorldModel.from_pretrained("nvidia/cosmos-predict1-5b")
```

**실용적 권장 경로**: 포트폴리오 프로젝트 수준에서는 경로 A(CosmosWriter)로 합성 데이터를 충분히 생성할 수 있습니다. 경로 B/C는 기업 협업 프로젝트 또는 실제 제품화 단계에서 활용하세요.

---

## 3. 단계별 상세 개발 가이드

### Phase 1: 환경 구축 (예상 소요: 1~2일)

#### 1.1 NVIDIA 드라이버 및 CUDA 설정

```bash
#!/bin/bash
# scripts/setup_host.sh 핵심 부분

# NVIDIA Driver 570+ (RTX 5090 필수)
sudo apt-get purge --autoremove nvidia-*
sudo ubuntu-drivers install nvidia:570

# CUDA 12.4 설치
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update && sudo apt-get install cuda-toolkit-12-4

# cuDNN 9.x
sudo apt-get install libcudnn9-cuda-12

# 환경 변수
echo 'export CUDA_HOME=/usr/local/cuda-12.4' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
echo 'export PATH=$CUDA_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# 검증
nvidia-smi  # RTX 5090 24GB 확인
nvcc --version  # CUDA 12.4 확인
```

#### 1.2 Isaac Sim 2025.2 설치

```bash
# Isaac Sim은 pip 설치 방식 (2023.x 이후 변경됨)
conda create -n isaac-sim python=3.10 -y
conda activate isaac-sim

# pip 설치 (NGC 계정 필요)
pip install 'isaacsim[all]' --extra-index-url https://pypi.ngc.nvidia.com

# 또는 Docker 방식 (권장)
docker pull nvcr.io/nvidia/isaac-sim:2025.2.0

# Docker 실행 (X11 포워딩 포함)
docker run --gpus all \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v ~/isaac-workspace:/workspace \
  -p 8211:8211 \
  --name isaac-sim \
  nvcr.io/nvidia/isaac-sim:2025.2.0 \
  bash
```

#### 1.3 Isaac Lab 2.1 설치

```bash
# Isaac Lab은 Isaac Sim 위에서 실행
conda activate isaac-sim

git clone https://github.com/isaac-sim/IsaacLab.git --branch v2.1.0
cd IsaacLab

# 의존성 설치
./isaaclab.sh --install

# 검증 (headless 모드)
python source/standalone/tutorials/00_sim/create_empty.py --headless

# TurtleBot3 환경 체크
python source/standalone/environments/navigation/config/turtlebot3_nav_cfg.py
```

#### 1.4 ROS2 Humble + TurtleBot3 설치

```bash
# ROS2 Humble (Ubuntu 22.04)
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
  http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
  | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update && sudo apt install ros-humble-desktop

# TurtleBot3 패키지
sudo apt install ros-humble-turtlebot3 \
                 ros-humble-turtlebot3-simulations \
                 ros-humble-navigation2 \
                 ros-humble-nav2-bringup \
                 ros-humble-slam-toolbox

# 환경 변수
echo 'source /opt/ros/humble/setup.bash' >> ~/.bashrc
echo 'export TURTLEBOT3_MODEL=burger' >> ~/.bashrc
echo 'export ROS_DOMAIN_ID=42' >> ~/.bashrc
source ~/.bashrc
```

---

### Phase 2: TurtleBot3 모델링 및 시뮬레이션 (예상 소요: 2~3일)

#### 2.1 URDF → USD 변환

```python
# src/urdf/convert_to_usd.py
"""
TurtleBot3 Burger URDF를 Isaac Sim USD 형식으로 변환
"""
import omni.kit.commands
from omni.isaac.urdf import _urdf

def convert_turtlebot3_to_usd(
    urdf_path: str = "/workspace/src/urdf/turtlebot3_burger.urdf",
    usd_output: str = "/workspace/assets/turtlebot3_burger.usd"
):
    # URDF 임포터 설정
    import_config = _urdf.ImportConfig()
    import_config.merge_fixed_joints = False
    import_config.convex_decomp = True
    import_config.import_inertia_tensor = True
    import_config.fix_base = False
    import_config.make_default_prim = True
    import_config.self_collision = False
    import_config.create_physics_scene = True
    import_config.distance_scale = 1.0
    import_config.density = 0.0
    
    # 바퀴 조인트 설정 (속도 제어)
    import_config.default_drive_type = _urdf.UrdfJointTargetType.JOINT_DRIVE_VELOCITY
    import_config.default_drive_strength = 1000.0
    import_config.default_position_drive_damping = 10.0
    
    # 변환 실행
    result, prim_path = omni.kit.commands.execute(
        "URDFParseAndImportFile",
        urdf_path=urdf_path,
        import_config=import_config,
        get_articulation_root=True,
    )
    
    if result:
        print(f"✅ USD 변환 성공: {usd_output}")
        # 스테이지 저장
        import omni.usd
        omni.usd.get_context().save_as_stage(usd_output)
    else:
        print(f"❌ USD 변환 실패: {result}")
    
    return result, prim_path
```

#### 2.2 Isaac Sim 환경 설정 (완전 코드)

```python
# src/isaac_sim/setup_simulation.py
"""
TurtleBot3 Isaac Sim 환경 설정
- 실내 맵 로딩 (병원 / 창고 / 사무실 선택 가능)
- LiDAR / IMU / 카메라 센서 설정
- ROS2 Bridge 연결
- 물리 파라미터 최적화
"""

import omni.isaac.core
import omni.isaac.core.utils.prims as prim_utils
from omni.isaac.core import World
from omni.isaac.core.robots import Robot
from omni.isaac.sensor import Camera, LidarRtx, IMUSensor
from omni.isaac.ros2_bridge import ROS2Publisher, ROS2Subscriber

# 전역 설정
SIMULATION_CONFIG = {
    "physics_dt": 1/200,      # 200Hz 물리 연산
    "rendering_dt": 1/30,     # 30Hz 렌더링
    "gravity": [0, 0, -9.81],
    "robot_usd": "/workspace/assets/turtlebot3_burger.usd",
    "map_usd": "/workspace/assets/maps/hospital_ward.usd",
    "lidar_config": "Velodyne_VLP16",    # 16채널 LiDAR 시뮬레이션
    "ros2_domain_id": 42,
}

class TurtleBot3IsaacSim:
    def __init__(self, config: dict = SIMULATION_CONFIG):
        self.config = config
        self.world = None
        self.robot = None
        self.lidar = None
        self.camera = None
        self.imu = None
        
    def setup_world(self):
        """월드 초기화 및 환경 로딩"""
        self.world = World(
            physics_dt=self.config["physics_dt"],
            rendering_dt=self.config["rendering_dt"],
            stage_units_in_meters=1.0
        )
        
        # 중력 설정
        self.world.scene.add_default_ground_plane()
        
        # 환경 맵 로딩
        prim_utils.create_prim(
            prim_path="/World/Environment",
            prim_type="Xform",
            usd_path=self.config["map_usd"]
        )
        
        print("✅ 월드 설정 완료")
        return self.world
    
    def spawn_robot(self, position=[0, 0, 0.01], orientation=[0, 0, 0, 1]):
        """TurtleBot3 스폰"""
        self.robot = Robot(
            prim_path="/World/TurtleBot3",
            name="turtlebot3",
            usd_path=self.config["robot_usd"],
            position=position,
            orientation=orientation
        )
        self.world.scene.add(self.robot)
        
        # 관절 드라이브 초기화
        self.robot.initialize()
        print(f"✅ 로봇 스폰 완료: {position}")
        return self.robot
    
    def setup_lidar(self):
        """LiDAR 센서 설정 (360° 스캔)"""
        self.lidar = LidarRtx(
            prim_path="/World/TurtleBot3/base_scan/Lidar",
            name="lidar",
            rotation_frequency=10,  # 10Hz 스캔
            valid_range=(0.12, 3.5), # TurtleBot3 LDS-01 스펙
            scan_type="rotary",
            horizontal_fov=360.0,
            vertical_fov=15.0,
            horizontal_resolution=1.0,
            vertical_resolution=2.0,
        )
        print("✅ LiDAR 설정 완료")
        return self.lidar
    
    def setup_ros2_bridge(self):
        """ROS2 Bridge 설정"""
        import omni.graph.core as og
        
        # ROS2 Graph 생성
        (graph, _, _, _) = og.Controller.edit(
            {"graph_path": "/ActionGraph_ROS2", "evaluator_name": "execution"},
            {
                og.Controller.Keys.CREATE_NODES: [
                    ("OnPlaybackTick", "omni.graph.action.OnPlaybackTick"),
                    # LiDAR → /scan
                    ("RtxLidarHelper", "omni.isaac.ros2_bridge.ROS2RtxLidarHelper"),
                    # IMU → /imu/data  
                    ("ImuPublisher", "omni.isaac.ros2_bridge.ROS2ImuPublisher"),
                    # odom → /odom
                    ("OdomPublisher", "omni.isaac.ros2_bridge.ROS2OdometryPublisher"),
                    # /cmd_vel 수신
                    ("TwistSubscriber", "omni.isaac.ros2_bridge.ROS2SubscribeTwist"),
                    # TF
                    ("TfPublisher", "omni.isaac.ros2_bridge.ROS2PublishTransformTree"),
                    # Clock
                    ("ClockPublisher", "omni.isaac.ros2_bridge.ROS2PublishClock"),
                ],
                og.Controller.Keys.SET_VALUES: [
                    ("RtxLidarHelper.inputs:frameId", "base_scan"),
                    ("RtxLidarHelper.inputs:topicName", "/scan"),
                    ("ImuPublisher.inputs:topicName", "/imu/data"),
                    ("OdomPublisher.inputs:topicName", "/odom"),
                    ("TwistSubscriber.inputs:topicName", "/cmd_vel"),
                ],
            }
        )
        print("✅ ROS2 Bridge Graph 설정 완료")
        return graph
    
    def run(self, steps: int = None):
        """시뮬레이션 실행"""
        self.world.reset()
        
        step = 0
        while True:
            if steps and step >= steps:
                break
            self.world.step(render=True)
            step += 1
            
            if step % 1000 == 0:
                print(f"Step {step}: pos={self.robot.get_world_pose()[0][:2]}")

# 실행 엔트리포인트
if __name__ == "__main__":
    sim = TurtleBot3IsaacSim()
    sim.setup_world()
    sim.spawn_robot()
    sim.setup_lidar()
    sim.setup_ros2_bridge()
    sim.run()
```

---

### Phase 3: Isaac Lab RL 학습 (예상 소요: 3~5일)

#### 3.1 TurtleBot3 Navigation 환경 정의

```python
# src/isaac_lab/turtlebot_nav_env.py
"""
Isaac Lab 기반 TurtleBot3 Navigation 환경
- Observation Space: LiDAR 240점 + 목표 방향 + 선속도/각속도
- Action Space: 선속도 [-0.22, 0.22] + 각속도 [-2.84, 2.84]  (TurtleBot3 Burger 스펙)
- Reward: 목표 접근 보상 + 충돌 패널티 + 진동 패널티
"""

from __future__ import annotations
import torch
import math
from dataclasses import dataclass
from typing import Sequence

from omni.isaac.lab.envs import DirectRLEnv, DirectRLEnvCfg
from omni.isaac.lab.scene import InteractiveSceneCfg
from omni.isaac.lab.assets import ArticulationCfg
from omni.isaac.lab.sensors import RayCasterCfg
from omni.isaac.lab.utils import configclass


@configclass
class TurtleBot3NavEnvCfg(DirectRLEnvCfg):
    """TurtleBot3 Navigation 환경 설정"""
    
    # 환경 기본 설정
    episode_length_s: float = 30.0       # 에피소드 최대 30초
    decimation: int = 4                   # 물리 200Hz / 4 = 50Hz 정책 실행
    num_envs: int = 256                   # 병렬 환경 수
    
    # 관측 공간: [lidar_240, goal_angle, goal_dist, linear_vel, angular_vel]
    # = 240 + 1 + 1 + 1 + 1 = 244
    observation_space: int = 244
    
    # 행동 공간: [linear_vel, angular_vel]
    action_space: int = 2
    
    # 보상 스케일
    reward_goal_reach: float = 200.0      # 목표 도달
    reward_progress: float = 5.0         # 목표 방향 접근
    reward_collision: float = -100.0     # 충돌 패널티
    reward_time_penalty: float = -0.1    # 시간 패널티 (효율 유도)
    reward_oscillation: float = -2.0     # 급격한 방향 전환 패널티
    
    # 도메인 랜덤화 (Sim-to-Real 핵심)
    randomize_friction: bool = True
    friction_range: tuple = (0.4, 1.2)
    randomize_mass: bool = True
    mass_scale_range: tuple = (0.8, 1.2)
    randomize_sensor_noise: bool = True
    lidar_noise_std: float = 0.01        # LiDAR 노이즈 표준편차 (m)
    
    # TurtleBot3 Burger 액추에이터 한계
    max_linear_vel: float = 0.22         # m/s
    max_angular_vel: float = 2.84        # rad/s
    
    # 성공 기준
    goal_reach_threshold: float = 0.15  # 15cm 이내
    collision_threshold: float = 0.12   # LiDAR 12cm 이내 = 충돌


class TurtleBot3NavEnv(DirectRLEnv):
    """TurtleBot3 Navigation RL 환경 구현"""
    
    cfg: TurtleBot3NavEnvCfg
    
    def __init__(self, cfg: TurtleBot3NavEnvCfg, render_mode=None):
        super().__init__(cfg, render_mode)
        
        # 목표 위치 텐서 [num_envs, 3]
        self.goal_positions = torch.zeros(
            self.num_envs, 3, device=self.device
        )
        # 이전 로봇 위치 (진행률 계산용)
        self.prev_robot_pos = torch.zeros(
            self.num_envs, 3, device=self.device
        )
        # 진동 감지를 위한 이전 각속도
        self.prev_angular_vel = torch.zeros(
            self.num_envs, 1, device=self.device
        )
        # 에피소드 카운터
        self.episode_step_count = torch.zeros(
            self.num_envs, device=self.device, dtype=torch.long
        )
    
    def _setup_scene(self):
        """씬 설정: 로봇 + 장애물 + 목표"""
        # 로봇 스폰 (병렬)
        self.turtlebot = Articulation(self.cfg.robot_cfg)
        self.scene.articulations["turtlebot"] = self.turtlebot
        
        # LiDAR RayCaster (병렬 환경에서 고속)
        self.lidar = RayCaster(self.cfg.lidar_cfg)
        self.scene.sensors["lidar"] = self.lidar
        
        # 클론링 (병렬 환경 복제)
        self.scene.clone_environments(copy_from_source=False)
        self.scene.filter_collisions(global_prim_paths=[])
        
        # 조명
        light_cfg = sim_utils.DomeLightCfg(
            intensity=3000.0, color=(0.75, 0.75, 0.75)
        )
        light_cfg.func("/World/Light", light_cfg)
    
    def _get_observations(self) -> dict:
        """관측값 계산"""
        # LiDAR 데이터 [num_envs, 240]
        lidar_data = self.lidar.data.ray_hits_w
        lidar_ranges = torch.clamp(
            torch.norm(lidar_data - self.turtlebot.data.root_pos_w.unsqueeze(1), dim=-1),
            0.0, 3.5
        )
        lidar_normalized = lidar_ranges / 3.5  # 정규화
        
        # 목표 방향 계산
        robot_pos = self.turtlebot.data.root_pos_w[:, :2]
        goal_vec = self.goal_positions[:, :2] - robot_pos
        goal_dist = torch.norm(goal_vec, dim=1, keepdim=True)
        
        # 로봇 현재 yaw
        quat = self.turtlebot.data.root_quat_w
        yaw = torch.atan2(
            2*(quat[:,3]*quat[:,2] + quat[:,0]*quat[:,1]),
            1 - 2*(quat[:,1]**2 + quat[:,2]**2)
        ).unsqueeze(1)
        
        goal_angle = torch.atan2(goal_vec[:,1:2], goal_vec[:,0:1]) - yaw
        # 각도 정규화 [-π, π]
        goal_angle = torch.atan2(torch.sin(goal_angle), torch.cos(goal_angle))
        
        # 속도
        linear_vel = self.turtlebot.data.root_lin_vel_w[:, 0:1]
        angular_vel = self.turtlebot.data.root_ang_vel_w[:, 2:3]
        
        # 도메인 랜덤화: LiDAR 노이즈
        if self.cfg.randomize_sensor_noise:
            lidar_normalized += torch.randn_like(lidar_normalized) * 0.003
            lidar_normalized = torch.clamp(lidar_normalized, 0.0, 1.0)
        
        obs = torch.cat([
            lidar_normalized,              # 240
            goal_angle / math.pi,          # 1 (정규화)
            goal_dist / 5.0,               # 1 (정규화)
            linear_vel / self.cfg.max_linear_vel,   # 1
            angular_vel / self.cfg.max_angular_vel, # 1
        ], dim=-1)
        
        return {"policy": obs}
    
    def _get_rewards(self) -> torch.Tensor:
        """보상 계산"""
        robot_pos = self.turtlebot.data.root_pos_w[:, :2]
        goal_pos = self.goal_positions[:, :2]
        
        # 현재 목표까지 거리
        current_dist = torch.norm(goal_pos - robot_pos, dim=1)
        # 이전 스텝 거리
        prev_dist = torch.norm(goal_pos - self.prev_robot_pos[:, :2], dim=1)
        
        # 1. 진행 보상 (목표에 가까워질수록)
        progress_reward = (prev_dist - current_dist) * self.cfg.reward_progress
        
        # 2. 목표 도달 보상
        goal_reached = current_dist < self.cfg.goal_reach_threshold
        goal_reward = goal_reached.float() * self.cfg.reward_goal_reach
        
        # 3. 충돌 패널티 (LiDAR 최소값 기반)
        lidar_min = torch.min(
            self.lidar.data.ray_hits_w.norm(dim=-1), dim=1
        ).values
        collision = lidar_min < self.cfg.collision_threshold
        collision_penalty = collision.float() * self.cfg.reward_collision
        
        # 4. 시간 패널티
        time_penalty = torch.full(
            (self.num_envs,), self.cfg.reward_time_penalty, device=self.device
        )
        
        # 5. 진동(oscillation) 패널티
        angular_vel = self.turtlebot.data.root_ang_vel_w[:, 2]
        ang_vel_change = torch.abs(angular_vel - self.prev_angular_vel.squeeze(1))
        oscillation_penalty = (ang_vel_change > 1.0).float() * self.cfg.reward_oscillation
        
        # 이전 상태 업데이트
        self.prev_robot_pos = self.turtlebot.data.root_pos_w.clone()
        self.prev_angular_vel = angular_vel.unsqueeze(1).clone()
        
        total_reward = (progress_reward + goal_reward + collision_penalty + 
                       time_penalty + oscillation_penalty)
        
        return total_reward
    
    def _get_dones(self) -> tuple:
        """에피소드 종료 조건"""
        robot_pos = self.turtlebot.data.root_pos_w[:, :2]
        goal_pos = self.goal_positions[:, :2]
        dist = torch.norm(goal_pos - robot_pos, dim=1)
        
        # 성공: 목표 도달
        success = dist < self.cfg.goal_reach_threshold
        
        # 실패 조건들
        lidar_min = torch.min(
            self.lidar.data.ray_hits_w.norm(dim=-1), dim=1
        ).values
        collision = lidar_min < self.cfg.collision_threshold
        
        timeout = (self.episode_step_count >= 
                  int(self.cfg.episode_length_s / (self.cfg.decimation * self.cfg.sim_dt)))
        
        terminated = success | collision
        truncated = timeout
        
        return terminated, truncated
    
    def _reset_idx(self, env_ids: Sequence[int]):
        """환경 리셋"""
        super()._reset_idx(env_ids)
        
        # 랜덤 시작 위치
        n = len(env_ids)
        start_pos = torch.zeros(n, 3, device=self.device)
        start_pos[:, :2] = torch.rand(n, 2, device=self.device) * 2.0 - 1.0
        start_pos[:, 2] = 0.01
        
        # 랜덤 목표 위치 (시작으로부터 0.5~3.0m)
        angle = torch.rand(n, device=self.device) * 2 * math.pi
        dist = torch.rand(n, device=self.device) * 2.5 + 0.5
        self.goal_positions[env_ids, 0] = start_pos[:, 0] + dist * torch.cos(angle)
        self.goal_positions[env_ids, 1] = start_pos[:, 1] + dist * torch.sin(angle)
        
        # 도메인 랜덤화: 질량/마찰
        if self.cfg.randomize_mass:
            mass_scale = (torch.rand(n, device=self.device) * 
                         (self.cfg.mass_scale_range[1] - self.cfg.mass_scale_range[0]) + 
                         self.cfg.mass_scale_range[0])
            # Isaac Lab API로 mass randomization 적용
            self.turtlebot.write_root_mass_to_sim(
                mass_scale * self.default_masses[env_ids], env_ids=env_ids
            )
        
        # 에피소드 카운터 리셋
        self.episode_step_count[env_ids] = 0
```

#### 3.2 PPO 학습 실행 스크립트

```python
# src/isaac_lab/train_turtlebot_navigation.py
"""
PPO 학습 실행 스크립트
사용법: python train_turtlebot_navigation.py --num_envs 256 --headless --max_iterations 5000
"""

import argparse
import os
import torch

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_envs", type=int, default=256)
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--max_iterations", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--checkpoint", type=str, default=None)
    parser.add_argument("--log_dir", type=str, default="outputs/training_logs")
    return parser.parse_args()

# PPO 하이퍼파라미터 (TurtleBot3 Navigation 최적화)
PPO_CONFIG = {
    "device": "cuda",
    
    # PPO 핵심 파라미터
    "learning_rate": 3e-4,
    "num_steps": 64,          # 롤아웃 길이
    "num_minibatches": 8,
    "update_epochs": 5,
    "clip_coef": 0.2,
    "ent_coef": 0.01,         # 탐험 장려
    "vf_coef": 0.5,
    "max_grad_norm": 1.0,
    "gae_lambda": 0.95,
    "gamma": 0.99,
    
    # 네트워크 아키텍처
    "actor_hidden_dims": [256, 128, 64],
    "critic_hidden_dims": [256, 128, 64],
    "activation": "elu",
    
    # 학습 스케줄
    "learning_rate_schedule": "adaptive",  # KL 기반 adaptive LR
    "desired_kl": 0.01,
    
    # 저장/로깅
    "save_interval": 200,
    "eval_interval": 100,
}

def create_policy_network(obs_dim: int, action_dim: int, cfg: dict):
    """정책 네트워크 (Actor-Critic)"""
    import torch.nn as nn
    
    def build_mlp(input_dim, hidden_dims, output_dim, activation):
        layers = []
        prev_dim = input_dim
        act_fn = nn.ELU() if activation == "elu" else nn.ReLU()
        for h in hidden_dims:
            layers.extend([nn.Linear(prev_dim, h), act_fn])
            prev_dim = h
        layers.append(nn.Linear(prev_dim, output_dim))
        return nn.Sequential(*layers)
    
    class ActorCritic(nn.Module):
        def __init__(self):
            super().__init__()
            # 공유 인코더 (LiDAR 처리)
            self.lidar_encoder = nn.Sequential(
                nn.Linear(240, 128), nn.ELU(),
                nn.Linear(128, 64), nn.ELU(),
            )
            # 상태 인코더
            self.state_encoder = nn.Sequential(
                nn.Linear(4, 32), nn.ELU(),
            )
            # Actor
            self.actor = build_mlp(96, cfg["actor_hidden_dims"], action_dim, cfg["activation"])
            # Critic
            self.critic = build_mlp(96, cfg["critic_hidden_dims"], 1, cfg["activation"])
            # 로그 표준편차 (학습 가능)
            self.log_std = nn.Parameter(torch.zeros(action_dim))
            
        def forward(self, obs):
            lidar_feat = self.lidar_encoder(obs[:, :240])
            state_feat = self.state_encoder(obs[:, 240:])
            feat = torch.cat([lidar_feat, state_feat], dim=-1)
            
            action_mean = self.actor(feat)
            # 행동 범위 클리핑
            action_mean = torch.tanh(action_mean)
            
            value = self.critic(feat)
            return action_mean, self.log_std.exp(), value
    
    return ActorCritic()

def export_to_onnx(policy, obs_dim: int, save_path: str):
    """학습된 정책을 ONNX로 내보내기"""
    policy.eval()
    dummy_input = torch.zeros(1, obs_dim, device="cuda")
    
    torch.onnx.export(
        policy,
        dummy_input,
        save_path,
        opset_version=17,
        input_names=["observations"],
        output_names=["actions", "log_std", "value"],
        dynamic_axes={
            "observations": {0: "batch_size"},
            "actions": {0: "batch_size"},
        },
        export_params=True,
    )
    print(f"✅ ONNX 내보내기 완료: {save_path}")

if __name__ == "__main__":
    args = parse_args()
    
    # Isaac Lab 앱 초기화
    from omni.isaac.lab.app import AppLauncher
    launcher = AppLauncher(headless=args.headless)
    
    from turtlebot_nav_env import TurtleBot3NavEnv, TurtleBot3NavEnvCfg
    
    # 환경 생성
    env_cfg = TurtleBot3NavEnvCfg()
    env_cfg.num_envs = args.num_envs
    env = TurtleBot3NavEnv(env_cfg)
    
    # 정책 생성
    policy = create_policy_network(
        obs_dim=env_cfg.observation_space,
        action_dim=env_cfg.action_space,
        cfg=PPO_CONFIG
    ).to("cuda")
    
    print(f"📊 정책 파라미터 수: {sum(p.numel() for p in policy.parameters()):,}")
    print(f"🚀 학습 시작: {args.num_envs} 병렬 환경, {args.max_iterations} 이터레이션")
    
    # TensorBoard 로깅 시작
    from torch.utils.tensorboard import SummaryWriter
    writer = SummaryWriter(args.log_dir)
    
    # 학습 루프 (rsl_rl 또는 직접 구현)
    optimizer = torch.optim.Adam(policy.parameters(), lr=PPO_CONFIG["learning_rate"])
    
    best_reward = float('-inf')
    
    for iteration in range(args.max_iterations):
        # 롤아웃 수집
        obs, _ = env.reset()
        episode_rewards = []
        
        # ... (PPO 학습 루프 생략 - rsl_rl 라이브러리 활용 권장)
        
        # 저장
        if iteration % PPO_CONFIG["save_interval"] == 0:
            save_path = f"outputs/checkpoints/policy_iter{iteration}.pt"
            torch.save({
                "iteration": iteration,
                "model_state_dict": policy.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
            }, save_path)
            print(f"💾 체크포인트 저장: {save_path}")
    
    # 최종 ONNX 내보내기
    export_to_onnx(policy, env_cfg.observation_space, "outputs/policy/turtlebot_policy.onnx")
    env.close()
```

---

### Phase 4: TensorRT 변환 및 Jetson 배포 (예상 소요: 1~2일)

#### 4.1 ONNX → TensorRT 변환 스크립트

```bash
#!/bin/bash
# scripts/run_training.sh 핵심 부분 (TensorRT 변환)

# ONNX 모델 검증
python -c "
import onnx, onnxruntime
model = onnx.load('outputs/policy/turtlebot_policy.onnx')
onnx.checker.check_model(model)
print('✅ ONNX 검증 통과')
sess = onnxruntime.InferenceSession('outputs/policy/turtlebot_policy.onnx')
import numpy as np
test_input = np.zeros((1, 244), dtype=np.float32)
output = sess.run(None, {'observations': test_input})
print(f'✅ ONNX 추론 테스트 통과: output shape = {output[0].shape}')
"

# TensorRT 변환 (FP16)
trtexec \
    --onnx=outputs/policy/turtlebot_policy.onnx \
    --saveEngine=outputs/policy/turtlebot_policy_fp16.plan \
    --fp16 \
    --inputIOFormats=fp16:chw \
    --outputIOFormats=fp16:chw \
    --workspace=1024 \
    --minShapes=observations:1x244 \
    --optShapes=observations:1x244 \
    --maxShapes=observations:8x244 \
    --buildOnly \
    --verbose 2>&1 | tee outputs/tensorrt_build.log

echo "✅ TensorRT 변환 완료: outputs/policy/turtlebot_policy_fp16.plan"
```

#### 4.2 Jetson Orin Nano 추론 노드

```python
# src/deployment/jetson_inference_node.py
"""
Jetson Orin Nano TensorRT 실시간 추론 ROS2 노드
- /scan (LaserScan) → 정책 추론 → /cmd_vel (Twist)
- 목표 위치 /goal_pose 수신
- 추론 시간 모니터링 (~5ms 목표)
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32MultiArray

import numpy as np
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit
import math
import time

# Jetson 최적화 설정
JETSON_CONFIG = {
    "model_path": "/opt/turtlebot3/policy/turtlebot_policy_fp16.plan",
    "obs_dim": 244,
    "action_dim": 2,
    "lidar_points": 240,
    "max_linear_vel": 0.22,
    "max_angular_vel": 2.84,
    "goal_reach_threshold": 0.15,
    "collision_threshold": 0.12,
    "inference_hz": 50,  # 50Hz 추론
    "safety_linear_scale": 0.8,  # 안전 여유 20%
}

class TensorRTPolicy:
    """TensorRT FP16 정책 래퍼"""
    
    def __init__(self, model_path: str):
        # TRT 엔진 로딩
        self.logger = trt.Logger(trt.Logger.WARNING)
        with open(model_path, "rb") as f:
            engine_data = f.read()
        
        self.runtime = trt.Runtime(self.logger)
        self.engine = self.runtime.deserialize_cuda_engine(engine_data)
        self.context = self.engine.create_execution_context()
        
        # CUDA 버퍼 할당 (FP16)
        self.input_size = JETSON_CONFIG["obs_dim"] * np.dtype(np.float16).itemsize
        self.output_size = JETSON_CONFIG["action_dim"] * np.dtype(np.float16).itemsize
        
        self.d_input = cuda.mem_alloc(self.input_size)
        self.d_output = cuda.mem_alloc(self.output_size)
        self.stream = cuda.Stream()
        
        print(f"✅ TensorRT 엔진 로딩 완료: {model_path}")
    
    def infer(self, observation: np.ndarray) -> np.ndarray:
        """FP16 추론 실행"""
        obs_fp16 = observation.astype(np.float16)
        
        # CPU → GPU
        cuda.memcpy_htod_async(self.d_input, obs_fp16, self.stream)
        
        # 추론
        self.context.execute_async_v2(
            bindings=[int(self.d_input), int(self.d_output)],
            stream_handle=self.stream.handle
        )
        
        # GPU → CPU
        output = np.empty(JETSON_CONFIG["action_dim"], dtype=np.float16)
        cuda.memcpy_dtoh_async(output, self.d_output, self.stream)
        self.stream.synchronize()
        
        return output.astype(np.float32)


class JetsonInferenceNode(Node):
    """ROS2 추론 노드"""
    
    def __init__(self):
        super().__init__("jetson_rl_policy_node")
        self.get_logger().info("🚀 Jetson RL Policy 노드 시작")
        
        # TensorRT 정책 초기화
        self.policy = TensorRTPolicy(JETSON_CONFIG["model_path"])
        
        # 상태 변수
        self.lidar_data = np.ones(JETSON_CONFIG["lidar_points"]) * 3.5  # 초기값: 최대 범위
        self.goal_pos = np.array([1.0, 0.0])   # 기본 목표 (1m 전방)
        self.robot_pos = np.array([0.0, 0.0])
        self.robot_yaw = 0.0
        self.linear_vel = 0.0
        self.angular_vel = 0.0
        self.goal_reached = False
        
        # 추론 성능 통계
        self.inference_times = []
        self.total_inferences = 0
        
        # Subscribers
        self.scan_sub = self.create_subscription(
            LaserScan, "/scan", self.scan_callback, 10
        )
        self.goal_sub = self.create_subscription(
            PoseStamped, "/goal_pose", self.goal_callback, 10
        )
        self.odom_sub = self.create_subscription(
            Odometry, "/odom", self.odom_callback, 10
        )
        
        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.perf_pub = self.create_publisher(
            Float32MultiArray, "/rl_policy/performance", 10
        )
        
        # 추론 타이머 (50Hz)
        self.inference_timer = self.create_timer(
            1.0 / JETSON_CONFIG["inference_hz"],
            self.inference_callback
        )
        
        # 성능 리포트 타이머 (10초마다)
        self.report_timer = self.create_timer(10.0, self.report_performance)
        
        # Jetson 전력 최적화
        self._setup_jetson_power_mode()
    
    def _setup_jetson_power_mode(self):
        """Jetson 최대 성능 모드 설정"""
        import subprocess
        try:
            subprocess.run(["sudo", "jetson_clocks"], check=True)
            self.get_logger().info("⚡ Jetson Clocks 최대 성능 모드 적용")
        except Exception as e:
            self.get_logger().warn(f"jetson_clocks 실패: {e}")
    
    def scan_callback(self, msg: LaserScan):
        """LiDAR 데이터 수신 및 전처리"""
        ranges = np.array(msg.ranges, dtype=np.float32)
        # NaN/Inf 처리
        ranges = np.where(np.isfinite(ranges), ranges, msg.range_max)
        # 3.5m 클리핑
        ranges = np.clip(ranges, msg.range_min, 3.5)
        
        # 240점으로 다운샘플링 (LDS-01은 360점)
        if len(ranges) == 360:
            indices = np.linspace(0, 359, 240, dtype=int)
            self.lidar_data = ranges[indices]
        elif len(ranges) == 240:
            self.lidar_data = ranges
        else:
            # 임의 크기 → 보간
            x = np.linspace(0, 1, len(ranges))
            x_new = np.linspace(0, 1, 240)
            self.lidar_data = np.interp(x_new, x, ranges)
    
    def goal_callback(self, msg: PoseStamped):
        """목표 위치 수신"""
        self.goal_pos = np.array([
            msg.pose.position.x,
            msg.pose.position.y
        ])
        self.goal_reached = False
        self.get_logger().info(f"🎯 새 목표 설정: ({self.goal_pos[0]:.2f}, {self.goal_pos[1]:.2f})")
    
    def odom_callback(self, msg: Odometry):
        """오도메트리 수신"""
        self.robot_pos = np.array([
            msg.pose.pose.position.x,
            msg.pose.pose.position.y
        ])
        # 쿼터니언 → yaw
        q = msg.pose.pose.orientation
        self.robot_yaw = math.atan2(
            2*(q.w*q.z + q.x*q.y),
            1 - 2*(q.y**2 + q.z**2)
        )
        self.linear_vel = msg.twist.twist.linear.x
        self.angular_vel = msg.twist.twist.angular.z
    
    def _build_observation(self) -> np.ndarray:
        """관측 벡터 구성 [244]"""
        # LiDAR 정규화
        lidar_norm = self.lidar_data / 3.5
        
        # 목표 방향/거리
        goal_vec = self.goal_pos - self.robot_pos
        goal_dist = np.linalg.norm(goal_vec)
        goal_angle = math.atan2(goal_vec[1], goal_vec[0]) - self.robot_yaw
        goal_angle = math.atan2(math.sin(goal_angle), math.cos(goal_angle))  # [-π, π]
        
        obs = np.concatenate([
            lidar_norm,                                                        # 240
            [goal_angle / math.pi],                                            # 1
            [min(goal_dist / 5.0, 1.0)],                                       # 1
            [self.linear_vel / JETSON_CONFIG["max_linear_vel"]],               # 1
            [self.angular_vel / JETSON_CONFIG["max_angular_vel"]],             # 1
        ]).astype(np.float32)
        
        return obs
    
    def inference_callback(self):
        """메인 추론 루프"""
        # 목표 도달 확인
        goal_dist = np.linalg.norm(self.goal_pos - self.robot_pos)
        if goal_dist < JETSON_CONFIG["goal_reach_threshold"]:
            if not self.goal_reached:
                self.get_logger().info(f"🏆 목표 도달! dist={goal_dist:.3f}m")
                self.goal_reached = True
            self._publish_stop()
            return
        
        # 관측 구성
        obs = self._build_observation()
        
        # TensorRT 추론
        t_start = time.perf_counter()
        action = self.policy.infer(obs)
        t_elapsed = (time.perf_counter() - t_start) * 1000  # ms
        
        self.inference_times.append(t_elapsed)
        self.total_inferences += 1
        
        # 행동 → 속도 명령 변환 (tanh 역변환)
        linear_vel = float(action[0]) * JETSON_CONFIG["max_linear_vel"] * JETSON_CONFIG["safety_linear_scale"]
        angular_vel = float(action[1]) * JETSON_CONFIG["max_angular_vel"]
        
        # 안전 레이어: 전방 장애물 감지 시 감속
        front_lidar = np.min(self.lidar_data[100:140])  # 전방 40도
        if front_lidar < 0.3 and linear_vel > 0:
            safety_scale = max(0.0, (front_lidar - 0.12) / 0.18)
            linear_vel *= safety_scale
        
        # 속도 명령 발행
        cmd = Twist()
        cmd.linear.x = float(np.clip(linear_vel, -0.22, 0.22))
        cmd.angular.z = float(np.clip(angular_vel, -2.84, 2.84))
        self.cmd_vel_pub.publish(cmd)
    
    def _publish_stop(self):
        """정지 명령"""
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0
        self.cmd_vel_pub.publish(cmd)
    
    def report_performance(self):
        """추론 성능 리포트"""
        if not self.inference_times:
            return
        
        times = np.array(self.inference_times[-500:])  # 최근 500회
        perf_msg = Float32MultiArray()
        perf_msg.data = [
            float(np.mean(times)),   # 평균 추론 시간 (ms)
            float(np.std(times)),
            float(np.percentile(times, 95)),
            float(self.total_inferences),
        ]
        self.perf_pub.publish(perf_msg)
        
        self.get_logger().info(
            f"📊 추론 성능: 평균={np.mean(times):.2f}ms | "
            f"P95={np.percentile(times, 95):.2f}ms | "
            f"총 {self.total_inferences}회"
        )


def main():
    rclpy.init()
    node = JetsonInferenceNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node._publish_stop()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
```

---

## 5. 디지털 트윈 루프 구현

### 5.1 데이터 로거

```python
# src/digital_twin/data_logger.py
"""
실제 로봇 주행 데이터 수집기
- 10Hz 데이터 로깅 → SQLite Episode DB
- 에피소드 단위 관리 (목표 설정 → 도달/실패)
- 자동 압축 및 정리
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import Odometry

import sqlite3
import json
import time
import threading
import numpy as np
from datetime import datetime
from pathlib import Path

DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS episodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_time REAL NOT NULL,
    end_time REAL,
    goal_x REAL,
    goal_y REAL,
    start_x REAL,
    start_y REAL,
    outcome TEXT,          -- 'success' | 'collision' | 'timeout'
    final_distance REAL,
    total_steps INTEGER,
    policy_version TEXT,
    robot_id TEXT
);

CREATE TABLE IF NOT EXISTS steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    episode_id INTEGER REFERENCES episodes(id),
    timestamp REAL NOT NULL,
    lidar_json TEXT,       -- JSON array of 240 floats
    robot_x REAL,
    robot_y REAL,
    robot_yaw REAL,
    linear_vel REAL,
    angular_vel REAL,
    cmd_linear REAL,
    cmd_angular REAL,
    min_lidar_dist REAL
);

CREATE INDEX IF NOT EXISTS idx_steps_episode ON steps(episode_id);
CREATE INDEX IF NOT EXISTS idx_episodes_time ON episodes(start_time);
"""

class DataLogger(Node):
    """ROS2 데이터 로거 노드"""
    
    def __init__(self, db_path: str = "/opt/turtlebot3/data/episode_db.sqlite",
                 policy_version: str = "v1.0", robot_id: str = "tb3_jetson"):
        super().__init__("data_logger")
        
        self.db_path = db_path
        self.policy_version = policy_version
        self.robot_id = robot_id
        
        # DB 초기화
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.executescript(DB_SCHEMA)
        self.conn.commit()
        self.db_lock = threading.Lock()
        
        # 현재 에피소드
        self.current_episode_id = None
        self.episode_start_time = None
        self.goal_pos = None
        self.start_pos = None
        self.step_buffer = []
        self.step_count = 0
        
        # 최신 센서 데이터
        self.latest_scan = None
        self.latest_odom = None
        self.latest_cmd = None
        
        # Subscribers
        self.scan_sub = self.create_subscription(
            LaserScan, "/scan", self._scan_cb, 10
        )
        self.odom_sub = self.create_subscription(
            Odometry, "/odom", self._odom_cb, 10
        )
        self.cmd_sub = self.create_subscription(
            Twist, "/cmd_vel", self._cmd_cb, 10
        )
        self.goal_sub = self.create_subscription(
            PoseStamped, "/goal_pose", self._goal_cb, 10
        )
        
        # 10Hz 로깅 타이머
        self.log_timer = self.create_timer(0.1, self._log_step)
        # 버퍼 플러시 타이머 (5초)
        self.flush_timer = self.create_timer(5.0, self._flush_buffer)
        
        self.get_logger().info(f"📊 데이터 로거 시작: {db_path}")
    
    def _goal_cb(self, msg: PoseStamped):
        """새 목표 설정 → 에피소드 시작"""
        # 이전 에피소드가 있으면 종료
        if self.current_episode_id is not None:
            self._end_episode("timeout")
        
        self.goal_pos = np.array([msg.pose.position.x, msg.pose.position.y])
        
        if self.latest_odom:
            self.start_pos = np.array([
                self.latest_odom.pose.pose.position.x,
                self.latest_odom.pose.pose.position.y
            ])
        else:
            self.start_pos = np.zeros(2)
        
        # 에피소드 DB 삽입
        now = time.time()
        with self.db_lock:
            cursor = self.conn.execute(
                "INSERT INTO episodes (start_time, goal_x, goal_y, start_x, start_y, "
                "policy_version, robot_id) VALUES (?,?,?,?,?,?,?)",
                (now, float(self.goal_pos[0]), float(self.goal_pos[1]),
                 float(self.start_pos[0]), float(self.start_pos[1]),
                 self.policy_version, self.robot_id)
            )
            self.current_episode_id = cursor.lastrowid
            self.conn.commit()
        
        self.episode_start_time = now
        self.step_count = 0
        self.get_logger().info(f"📍 에피소드 {self.current_episode_id} 시작")
    
    def _end_episode(self, outcome: str):
        """에피소드 종료 기록"""
        if self.current_episode_id is None:
            return
        
        # 버퍼 플러시
        self._flush_buffer()
        
        final_dist = 0.0
        if self.latest_odom and self.goal_pos is not None:
            pos = np.array([
                self.latest_odom.pose.pose.position.x,
                self.latest_odom.pose.pose.position.y
            ])
            final_dist = float(np.linalg.norm(self.goal_pos - pos))
        
        with self.db_lock:
            self.conn.execute(
                "UPDATE episodes SET end_time=?, outcome=?, final_distance=?, total_steps=? "
                "WHERE id=?",
                (time.time(), outcome, final_dist, self.step_count, self.current_episode_id)
            )
            self.conn.commit()
        
        self.get_logger().info(
            f"🏁 에피소드 {self.current_episode_id} 종료: {outcome} | "
            f"거리={final_dist:.3f}m | {self.step_count}스텝"
        )
        self.current_episode_id = None
    
    def _log_step(self):
        """10Hz 스텝 데이터 버퍼링"""
        if (self.current_episode_id is None or 
            self.latest_scan is None or 
            self.latest_odom is None):
            return
        
        odom = self.latest_odom
        scan = self.latest_scan
        cmd = self.latest_cmd
        
        # LiDAR 다운샘플링
        ranges = np.array(scan.ranges, dtype=np.float32)
        ranges = np.where(np.isfinite(ranges), ranges, 3.5)
        if len(ranges) != 240:
            indices = np.linspace(0, len(ranges)-1, 240, dtype=int)
            ranges = ranges[indices]
        
        # yaw 계산
        q = odom.pose.pose.orientation
        yaw = np.arctan2(
            2*(q.w*q.z + q.x*q.y),
            1 - 2*(q.y**2 + q.z**2)
        )
        
        step_data = (
            self.current_episode_id,
            time.time(),
            json.dumps(ranges.tolist()),
            float(odom.pose.pose.position.x),
            float(odom.pose.pose.position.y),
            float(yaw),
            float(odom.twist.twist.linear.x),
            float(odom.twist.twist.angular.z),
            float(cmd.linear.x) if cmd else 0.0,
            float(cmd.angular.z) if cmd else 0.0,
            float(np.min(ranges)),
        )
        
        self.step_buffer.append(step_data)
        self.step_count += 1
        
        # 충돌 감지 → 에피소드 자동 종료
        if np.min(ranges) < 0.12:
            self._end_episode("collision")
    
    def _flush_buffer(self):
        """버퍼를 DB에 플러시"""
        if not self.step_buffer:
            return
        
        buffer_copy = self.step_buffer.copy()
        self.step_buffer.clear()
        
        with self.db_lock:
            self.conn.executemany(
                "INSERT INTO steps (episode_id, timestamp, lidar_json, robot_x, robot_y, "
                "robot_yaw, linear_vel, angular_vel, cmd_linear, cmd_angular, min_lidar_dist) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                buffer_copy
            )
            self.conn.commit()
    
    def _scan_cb(self, msg): self.latest_scan = msg
    def _odom_cb(self, msg): self.latest_odom = msg
    def _cmd_cb(self, msg): self.latest_cmd = msg
```

### 5.2 갭 분석기

```python
# src/digital_twin/gap_analyzer.py
"""
Sim-vs-Real 갭 분석 및 재학습 트리거
주기: 5분 (300초)
갭 기준: 15% 이상 → 재학습 트리거
"""

import sqlite3
import numpy as np
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@dataclass
class GapMetrics:
    """Sim-Real 갭 지표"""
    success_rate_real: float = 0.0      # 실제 로봇 성공률
    success_rate_sim: float = 0.0       # 시뮬레이션 성공률
    avg_collision_rate: float = 0.0     # 충돌율
    avg_path_length: float = 0.0        # 평균 경로 길이 (m)
    avg_reach_time: float = 0.0         # 평균 도달 시간 (s)
    gap_score: float = 0.0              # 종합 갭 점수
    needs_retrain: bool = False
    analysis_time: str = ""
    episode_count: int = 0
    confidence: float = 0.0             # 분석 신뢰도 (에피소드 수 기반)
    
    # 세부 갭 분해
    gap_breakdown: dict = field(default_factory=dict)


class GapAnalyzer:
    """Sim-Real 갭 분석기"""
    
    # 시뮬레이션 기준 성능 (학습 완료 시 측정값)
    SIM_BASELINE = {
        "success_rate": 0.94,       # 시뮬레이션 성공률 94%
        "collision_rate": 0.03,     # 충돌률 3%
        "avg_path_efficiency": 0.87, # 경로 효율성 (실제/최단 경로 비율)
        "avg_reach_time": 12.5,     # 평균 도달 시간 (s)
    }
    
    # 갭 임계값 (가중치 반영)
    GAP_WEIGHTS = {
        "success_rate": 0.40,       # 성공률 갭 (가장 중요)
        "collision_rate": 0.35,     # 충돌률 갭 (안전)
        "path_efficiency": 0.15,    # 경로 효율
        "reach_time": 0.10,         # 도달 시간
    }
    RETRAIN_THRESHOLD = 0.15        # 15% 가중 갭
    MIN_EPISODES = 10               # 최소 분석 에피소드 수
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def analyze(self, window_hours: float = 1.0) -> GapMetrics:
        """최근 N시간 에피소드 분석"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        # 최근 에피소드 쿼리
        cutoff = datetime.now() - timedelta(hours=window_hours)
        cutoff_ts = cutoff.timestamp()
        
        episodes = conn.execute("""
            SELECT e.*, 
                   (e.end_time - e.start_time) as duration,
                   COUNT(s.id) as step_count,
                   AVG(s.min_lidar_dist) as avg_min_dist
            FROM episodes e
            LEFT JOIN steps s ON s.episode_id = e.id
            WHERE e.start_time > ? AND e.end_time IS NOT NULL
            GROUP BY e.id
            ORDER BY e.start_time DESC
        """, (cutoff_ts,)).fetchall()
        conn.close()
        
        metrics = GapMetrics(
            analysis_time=datetime.now().isoformat(),
            episode_count=len(episodes)
        )
        
        if len(episodes) < self.MIN_EPISODES:
            metrics.confidence = len(episodes) / self.MIN_EPISODES
            logger.info(f"분석 데이터 부족: {len(episodes)}/{self.MIN_EPISODES} 에피소드")
            return metrics
        
        # 지표 계산
        outcomes = [e["outcome"] for e in episodes]
        durations = [e["duration"] for e in episodes if e["duration"]]
        
        real_success_rate = outcomes.count("success") / len(outcomes)
        real_collision_rate = outcomes.count("collision") / len(outcomes)
        real_avg_time = np.mean(durations) if durations else 0.0
        
        # 경로 효율성 (실제 이동 거리 / 직선 거리)
        path_efficiencies = []
        for ep in episodes:
            if ep["outcome"] == "success" and ep["start_x"] is not None:
                direct_dist = np.sqrt(
                    (ep["goal_x"] - ep["start_x"])**2 + 
                    (ep["goal_y"] - ep["start_y"])**2
                )
                if direct_dist > 0.1:  # 너무 짧은 목표 제외
                    # 이동 거리 ≈ 스텝 수 * 이동속도 * 0.1s
                    actual_dist = ep["step_count"] * 0.15 * 0.1  # 근사치
                    efficiency = min(direct_dist / actual_dist, 1.0)
                    path_efficiencies.append(efficiency)
        
        real_path_efficiency = np.mean(path_efficiencies) if path_efficiencies else 0.5
        
        # 갭 계산
        gap_success = max(0, self.SIM_BASELINE["success_rate"] - real_success_rate)
        gap_collision = max(0, real_collision_rate - self.SIM_BASELINE["collision_rate"])
        gap_efficiency = max(0, self.SIM_BASELINE["avg_path_efficiency"] - real_path_efficiency)
        gap_time = max(0, (real_avg_time - self.SIM_BASELINE["avg_reach_time"]) / 
                      self.SIM_BASELINE["avg_reach_time"])
        
        # 가중 갭 점수
        gap_score = (
            gap_success * self.GAP_WEIGHTS["success_rate"] +
            gap_collision * self.GAP_WEIGHTS["collision_rate"] +
            gap_efficiency * self.GAP_WEIGHTS["path_efficiency"] +
            gap_time * self.GAP_WEIGHTS["reach_time"]
        )
        
        metrics.success_rate_real = real_success_rate
        metrics.success_rate_sim = self.SIM_BASELINE["success_rate"]
        metrics.avg_collision_rate = real_collision_rate
        metrics.avg_reach_time = real_avg_time
        metrics.gap_score = gap_score
        metrics.needs_retrain = gap_score >= self.RETRAIN_THRESHOLD
        metrics.confidence = min(1.0, len(episodes) / 30)
        metrics.gap_breakdown = {
            "success_gap": round(gap_success, 4),
            "collision_gap": round(gap_collision, 4),
            "efficiency_gap": round(gap_efficiency, 4),
            "time_gap": round(gap_time, 4),
        }
        
        logger.info(
            f"🔍 갭 분석 완료 | "
            f"성공률: 실제={real_success_rate:.1%} vs 시뮬={self.SIM_BASELINE['success_rate']:.1%} | "
            f"종합 갭: {gap_score:.1%} {'⚠️ 재학습 필요!' if metrics.needs_retrain else '✅ 정상'}"
        )
        
        return metrics
```

---

## 6. Sim-to-Real 갭 분석 방법론

### 6.1 갭 원인 분류 및 대응 전략

| 갭 원인 | 증상 | 대응 방법 |
|---------|------|-----------|
| **센서 노이즈** | 시뮬레이션보다 LiDAR 반응이 불안정 | LiDAR 노이즈 범위 확대 (σ=0.01→0.03) |
| **바닥 마찰 차이** | 미끄러짐, 오버슈팅 | 마찰계수 랜덤화 범위 확대 |
| **모터 응답 지연** | 명령 → 실행 간 딜레이 | 액션 딜레이 랜덤화 (10~30ms) 추가 |
| **조명 변화** | 카메라 기반 로봇에서 인식 실패 | Cosmos-Transfer 도메인 적응 |
| **맵 불일치** | 실제 공간에 없는 장애물 | Isaac Sim에서 실제 공간 스캔 데이터 기반 재구성 |
| **배터리 전압 변동** | 후반부 성능 저하 | 속도 스케일링 랜덤화 추가 |

### 6.2 도메인 랜덤화 파라미터 권장값

```python
# config/domain_randomization.yaml에 반영할 권장 파라미터
DOMAIN_RANDOMIZATION_PARAMS = {
    # 물리 파라미터
    "wheel_friction": {
        "distribution": "uniform",
        "range": [0.4, 1.2],
        "default": 0.8
    },
    "robot_mass_scale": {
        "distribution": "uniform", 
        "range": [0.85, 1.15],
        "default": 1.0
    },
    "floor_friction": {
        "distribution": "uniform",
        "range": [0.3, 1.0],
        "default": 0.7
    },
    
    # 센서 노이즈
    "lidar_gaussian_noise": {
        "distribution": "gaussian",
        "std": 0.025,  # 2.5cm → 실제 LDS-01 스펙 반영
        "max_dropout_rate": 0.05  # 5% 포인트 드롭
    },
    "odom_noise_linear": {
        "distribution": "gaussian",
        "std": 0.02  # 2% 오도메트리 오차
    },
    
    # 액추에이터
    "action_delay_steps": {
        "distribution": "randint",
        "range": [1, 4],  # 1~4 스텝 (5~20ms @ 200Hz)
    },
    "motor_torque_scale": {
        "distribution": "uniform",
        "range": [0.85, 1.15]
    },
    
    # 환경
    "obstacle_position_jitter": {
        "distribution": "gaussian",
        "std": 0.05  # ±5cm 위치 불확실성
    }
}
```

---

## 7. 성능 벤치마크 기준표

### 7.1 학습 성능 목표 (Isaac Lab PPO)

| 지표 | 1M Step | 3M Step | 5M Step (목표) |
|------|---------|---------|---------------|
| 성공률 (Sim) | ~60% | ~85% | ~94% |
| 평균 충돌률 | ~15% | ~8% | ~3% |
| 평균 에피소드 보상 | ~150 | ~480 | ~750 |
| 학습 시간 (RTX 5090) | ~1시간 | ~3시간 | ~5시간 |

### 7.2 실제 로봇 성능 목표 (TurtleBot3 Burger)

| 지표 | 최소 기준 | 목표 | 우수 |
|------|----------|------|------|
| 성공률 (실제) | 70% | 85% | 92%+ |
| 충돌률 | <10% | <5% | <2% |
| 추론 지연 (Jetson Nano) | <20ms | <10ms | <5ms |
| 경로 효율성 | >60% | >80% | >90% |
| 배터리 지속 시간 영향 | -20% | -10% | -5% |

### 7.3 Digital Twin 루프 성능 목표

| 지표 | 기준값 |
|------|--------|
| 데이터 수집 주기 | 10Hz |
| 갭 분석 주기 | 5분 |
| 재학습 트리거 갭 임계값 | 15% |
| 재학습 완료 시간 | <2시간 (fine-tune) |
| Blue-Green 배포 전환 시간 | <30초 |
| 롤백 소요 시간 | <5초 |

---

## 8. 교육 커리큘럼 연계 방안

### 8.1 광주인력개발원 AI/로봇 커리큘럼 통합 방안

```
기존 커리큘럼          →    이 프로젝트 연계
────────────────────────────────────────────────────────
STM32F103 임베디드      →  Jetson Orin Nano 임베디드 + ROS2
Raspberry Pi 4 Linux   →  RPi 5 TurtleBot3 Follower
YOLOv8 비전            →  Isaac Sim 카메라 센서 + 합성 데이터
TurtleBot3 ROS1        →  TurtleBot3 ROS2 Humble + Nav2
강화학습 이론           →  Isaac Lab PPO 실습
FPGA 가속기 설계        →  TensorRT FP16 추론 최적화
FreeRTOS               →  ROS2 DDS + 실시간 제어
```

### 8.2 난이도별 실습 모듈 설계 (12주 집중)

| 주차 | 모듈 | 핵심 실습 | 난이도 |
|------|------|-----------|--------|
| 1~2 | Isaac Sim 기초 | 시뮬레이션 환경 + ROS2 Bridge | ⭐⭐ |
| 3~4 | URDF/USD 모델링 | TurtleBot3 실제↔시뮬 대응 | ⭐⭐⭐ |
| 5~6 | Isaac Lab RL | PPO 학습 + 보상 함수 튜닝 | ⭐⭐⭐⭐ |
| 7 | TensorRT 최적화 | FP16 변환 + Jetson 배포 | ⭐⭐⭐ |
| 8~9 | Sim-to-Real | 갭 분석 + DR 파라미터 조정 | ⭐⭐⭐⭐ |
| 10~11 | Digital Twin | 자동 파이프라인 구축 | ⭐⭐⭐⭐⭐ |
| 12 | 포트폴리오 | 최종 발표 + GitHub 정리 | ⭐⭐ |

---

## 9. 컨설팅 제안서 핵심 포인트

### 9.1 스마트팩토리 적용 시나리오

```
[제조업 적용 예시]
────────────────────────────────────────────────────────────
현재 고객 문제: 공장 내 물류 로봇이 월 2~3회 충돌 발생
               → 생산 중단 + 수리 비용 + 안전 위험

제안 솔루션: Digital Twin Closed-Loop 기반 자율주행
            ① Isaac Sim으로 공장 디지털 트윈 구축 (LiDAR 맵 기반)
            ② RL 정책으로 장애물 회피 학습 (사람, 지게차, 팔레트)
            ③ 실제 운영 중 갭 자동 감지 → 야간 재학습 → 무중단 배포
            
기대 효과:
  - 충돌 발생 90% 감소 (월 2~3회 → 연 2~3회)
  - 새 레이아웃 적응 시간 단축: 3주 수동 프로그래밍 → 2일 자동 재학습
  - 예측 유지보수 연계: 주행 패턴 이상 감지 → 조기 점검 알림
```

### 9.2 차별화 포인트 정리

1. **NVIDIA 공식 최신 스택 활용**: Isaac Sim 2025 + Cosmos 2.0 + Isaac Lab 2.1을 통합한 국내 최초 수준 레퍼런스 구현

2. **완전 자동화 루프**: 사람 개입 없이 데이터 수집 → 갭 분석 → 재학습 → 배포 (경쟁사 대비 유지보수 비용 절감)

3. **엣지 AI 최적화**: Jetson Orin Nano에서 5ms 추론 달성 (일반 Python 30ms 대비 6배 빠름)

4. **이기종 협업**: 고성능(Jetson) + 저비용(RPi 5) 로봇의 ROS2 기반 팀 운영 → 비용 최적화 아키텍처 제시

---

## 10. 알려진 기술적 도전과 해결책

### 10.1 자주 발생하는 문제 및 해결책

**문제 1: Isaac Sim ROS2 Bridge에서 /scan 토픽이 간헐적으로 끊김**
```bash
# 원인: DDS QoS 미스매치
# 해결: RMW_IMPLEMENTATION 명시
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export FASTRTPS_DEFAULT_PROFILES_FILE=/workspace/config/fastrtps.xml

# fastrtps.xml에서 history depth 증가
# <historyMemoryPolicy>DYNAMIC_RESERVE</historyMemoryPolicy>
```

**문제 2: Isaac Lab PPO 학습 중 NaN 보상 발생**
```python
# 원인: 초기 랜덤 위치에서 즉시 충돌
# 해결: 안전 마진이 있는 랜덤 위치 생성
start_pos[:, :2] = torch.rand(n, 2, device=self.device) * 1.5  # 범위 축소
# 추가: 초기 LiDAR 최소값 검사
while True:
    candidates = torch.rand(n, 2) * 1.5 - 0.75
    safe = check_collision_free(candidates, obstacle_map)
    if safe.all():
        break
```

**문제 3: TensorRT 변환 후 ONNX 대비 정확도 저하**
```bash
# 원인: FP16 오버플로우 (특히 tanh 출력)
# 해결: 혼합 정밀도 레이어 지정
trtexec \
    --onnx=policy.onnx \
    --fp16 \
    --precisionConstraints=obey \
    --layerPrecisions="*Tanh*":fp32  # tanh는 FP32 유지
```

**문제 4: Jetson Orin Nano에서 OOM 발생**
```bash
# /etc/systemd/system/ros2-turtlebot.service
# 메모리 최적화 설정
export MALLOC_TRIM_THRESHOLD_=131072
export MALLOC_MMAP_MAX_=65536

# SWAP 설정 (16GB)
sudo fallocate -l 16G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Nav2 경량화: 불필요한 플러그인 비활성화
# nav2_light_params.yaml 사용
```

**문제 5: Digital Twin 갭 분석에서 False Positive (불필요한 재학습 트리거)**
```python
# 원인: 데이터 부족 상태에서 분석
# 해결 1: 신뢰도 기반 임계값 조정
effective_threshold = RETRAIN_THRESHOLD * (1 + (1 - metrics.confidence) * 0.5)
# → 에피소드가 적으면 더 높은 갭이 필요해서 재학습 트리거

# 해결 2: 연속 위반 횟수 체크 (1회 위반으로 바로 재학습 X)
consecutive_violations = 0
if gap_score >= threshold:
    consecutive_violations += 1
if consecutive_violations >= 3:  # 3번 연속 위반 시에만 재학습
    trigger_retrain()
```

---

## 부록: 빠른 참조 명령어

```bash
# ===== 전체 파이프라인 순서 =====

# 1단계: Isaac Sim 시뮬레이션 시작
docker compose -f docker/docker-compose.yaml up -d isaac-sim
docker exec -it isaac-sim /isaac-sim/python.sh src/isaac_sim/setup_simulation.py

# 2단계: Isaac Lab PPO 학습 (RTX 5090, ~5시간)
python src/isaac_lab/train_turtlebot_navigation.py \
    --num_envs 256 --headless --max_iterations 5000 \
    --log_dir outputs/logs/run_$(date +%Y%m%d_%H%M%S)

# 3단계: 정책 변환 (.pt → .onnx → .plan)
bash scripts/run_training.sh

# 4단계: Jetson 배포 (SSH)
scp outputs/policy/turtlebot_policy_fp16.plan jetson:/opt/turtlebot3/policy/
ssh jetson "sudo systemctl restart ros2-turtlebot-policy.service"

# 5단계: Digital Twin 루프 시작
python3 src/digital_twin/orchestrator.py --start \
    --gap-threshold 0.15 --check-interval 300

# 6단계: 성능 모니터링
ros2 topic echo /rl_policy/performance
python3 scripts/evaluate_sim2real.py --plot

# ===== 유용한 디버그 명령어 =====
# TensorRT 엔진 정보
trtexec --loadEngine=outputs/policy/turtlebot_policy_fp16.plan --dumpLayerInfo

# Jetson 리소스 모니터링
jtop  # pip install jetson-stats

# Episode DB 확인
sqlite3 data/episode_db.sqlite "SELECT outcome, COUNT(*) FROM episodes GROUP BY outcome;"

# 갭 분석 즉시 실행
python3 -c "
from src.digital_twin.gap_analyzer import GapAnalyzer
analyzer = GapAnalyzer('data/episode_db.sqlite')
metrics = analyzer.analyze(window_hours=24)
print(f'갭 점수: {metrics.gap_score:.1%}, 재학습 필요: {metrics.needs_retrain}')
"
```

---

*이 문서는 NVIDIA Isaac Sim 2025.2 + Isaac Lab 2.1 + Cosmos 2.0 기준으로 작성되었습니다.*
*하드웨어: ASUS ROG Strix SCAR 16 (RTX 5090 24GB) + Jetson Orin Nano + TurtleBot3 Burger*
*작성일: 2025년 기준 | 광주인력개발원 나무 교수님 전문가 검토용*
