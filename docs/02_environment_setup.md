# 02. 환경 설정 가이드

> **Isaac Sim, Isaac Lab, Cosmos, ROS2 Humble, Jetson Orin Nano 환경 설치**

## 2.1 Isaac Sim 설치 (Docker 기반)

### 2.1.1 사전 확인

```bash
# NVIDIA GPU 드라이버 확인
nvidia-smi
# CUDA 버전 확인
nvcc --version
# Docker 확인
docker --version
# NVIDIA Container Toolkit 확인
docker run --rm --gpus all nvidia/cuda:12.4.0-base-ubuntu22.04 nvidia-smi
```

### 2.1.2 Isaac Sim 2025.2 Docker 이미지 풀

```bash
# 공식 Isaac Sim Docker 이미지
docker pull nvcr.io/nvidia/isaac-sim:2025.2.0

# NGC 계정 필요시 로그인
docker login nvcr.io
# Username: $oauthtoken
# Password: <your-api-key-from-ngc>
```

### 2.1.3 Isaac Sim 컨테이너 실행 스크립트

**`docker/isaac_sim_docker.sh`**:

```bash
#!/bin/bash
# Isaac Sim Docker 실행 스크립트

ISAAC_SIM_IMAGE="nvcr.io/nvidia/isaac-sim:2025.2.0"
CONTAINER_NAME="isaac-sim-ws"
WORKSPACE_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# X11 호스트 설정
if [ -z "$DISPLAY" ]; then
    echo "DISPLAY is not set. Using :0"
    export DISPLAY=:0
fi

xhost +local:docker

docker run -it --rm \
    --name $CONTAINER_NAME \
    --gpus all \
    -e DISPLAY=$DISPLAY \
    -e "ACCEPT_EULA=Y" \
    -e "PRIVACY_CONSENT=Y" \
    -e "OMNI_USER=admin" \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v $WORKSPACE_DIR:/workspace:rw \
    -v ~/.nvidia-omniverse:/root/.nvidia-omniverse:rw \
    -v ~/.cache/ov:/root/.cache/ov:rw \
    -v /usr/share/vulkan/icd.d:/usr/share/vulkan/icd.d:ro \
    --network host \
    --ipc=host \
    --ulimit memlock=-1 \
    --ulimit stack=67108864 \
    $ISAAC_SIM_IMAGE \
    bash
```

### 2.1.4 Isaac Sim 수동 설치 (Native, 비권장)

Docker를 사용할 수 없는 환경에서 직접 설치:

```bash
# Installer 다운로드
wget https://installer.isaac.omniverse.nvidia.com/isaac_sim/IsaacSim-2025.2.0-linux-x86_64.sh

# 설치
chmod +x IsaacSim-2025.2.0-linux-x86_64.sh
./IsaacSim-2025.2.0-linux-x86_64.sh --skip-ov-link

# 환경 변수 설정
echo 'export ISAAC_SIM_PATH="$HOME/.local/share/ov/pkg/isaac_sim-2025.2.0"' >> ~/.bashrc
echo 'alias isaac_sim="$ISAAC_SIM_PATH/isaac-sim.sh"' >> ~/.bashrc
source ~/.bashrc
```

## 2.2 Isaac Lab 설치

### 2.2.1 Conda 환경 설정

```bash
# Miniconda 설치 (없는 경우)
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p ~/miniconda3
~/miniconda3/bin/conda init bash
source ~/.bashrc

# Isaac Lab 환경 생성
conda create -n isaaclab python=3.10 -y
conda activate isaaclab
```

### 2.2.2 Isaac Lab 설치

```bash
# Isaac Lab 클론
git clone https://github.com/isaac-sim/IsaacLab.git ~/IsaacLab
cd ~/IsaacLab

# 심볼릭 링크 설정 (Docker Isaac Sim 경로에 맞춤)
# Docker 사용시: /workspace/.isaac_sim 으로 마운트
# Native 사용시: ISAAC_SIM_PATH 지정
ln -s /workspace/.isaac_sim ~/.isaac_sim  # Docker 경로 예시

# Python 의존성 설치
./isaaclab.sh --install

# 설치 확인
python -m isaaclab_tasks --help

# 환경 목록 보기
python -m isaaclab_tasks --list
```

### 2.2.3 Isaac Lab TurtleBot3 관련 패키지 설치

```bash
# 추가 의존성
pip install \
    torch>=2.1.0 \
    tensorboard \
    wandb \
    gymnasium \
    hydra-core \
    pyyaml \
    numpy \
    matplotlib \
    opencv-python \
    pillow
```

## 2.3 Cosmos 설치

### 2.3.1 시스템 요구사항 확인

- **GPU**: NVIDIA Ampere 이상 (RTX 3090, RTX 4090, A100, H100)
- **VRAM**: Cosmos-Predict2-2B 최소 16GB, Cosmos-Transfer 최소 24GB
- **CUDA**: 12.4+
- **Python**: 3.10+

### 2.3.2 Cosmos 설치

```bash
# Cosmos 저장소 클론
git clone https://github.com/NVIDIA/Cosmos.git ~/Cosmos
cd ~/Cosmos

# Conda 환경 (Isaac Lab과 별도 권장)
conda create -n cosmos python=3.10 -y
conda activate cosmos

# 의존성 설치
pip install -r requirements.txt

# Cosmos 모델 다운로드
# Hugging Face에서 모델 권한 필요
pip install huggingface_hub
huggingface-cli login
# Token 입력 (https://huggingface.co/settings/tokens)

# Cosmos-Predict2 모델 다운로드
huggingface-cli download nvidia/Cosmos-Predict2-2B-Video2World --local-dir ~/.cache/cosmos/models/Cosmos-Predict2-2B-Video2World

# Cosmos-Transfer 모델 다운로드
huggingface-cli download nvidia/Cosmos-Transfer1-7B --local-dir ~/.cache/cosmos/models/Cosmos-Transfer1-7B
```

### 2.3.3 Cosmos + Isaac Sim 연동 확인

```bash
# Cosmos Writer가 Isaac Sim에서 사용 가능한지 확인
cd ~/IsaacLab
python -c "from omni.replicator.core import WriterRegistry; print(WriterRegistry.get('CosmosWriter'))"
```

## 2.4 ROS2 Humble 환경 구성

### 2.4.1 ROS2 환경 변수 설정

```bash
echo 'source /opt/ros/humble/setup.bash' >> ~/.bashrc
echo 'source /usr/share/colcon_cd/function/colcon_cd.sh' >> ~/.bashrc
echo 'export ROS_DOMAIN_ID=42' >> ~/.bashrc
echo 'export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp' >> ~/.bashrc
source ~/.bashrc
```

### 2.4.2 TurtleBot3 ROS2 패키지 설치

```bash
# TurtleBot3 메타 패키지
sudo apt install -y \
    ros-humble-turtlebot3* \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-robot-localization \
    ros-humble-slam-toolbox

# TurtleBot3 simulation
sudo apt install -y \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-turtlebot3-gazebo

# ROS2 제어
sudo apt install -y \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-robot-localization \
    ros-humble-twist-mux \
    ros-humble-interactive-marker-twist-server
```

### 2.4.3 Colcon 워크스페이스 생성

```bash
mkdir -p ~/colcon_ws/src
cd ~/colcon_ws
colcon build --symlink-install
echo 'source ~/colcon_ws/install/setup.bash' >> ~/.bashrc
source ~/.bashrc
```

## 2.5 Jetson Orin Nano 설정

### 2.5.1 JetPack 6.0 설치

Jetson Orin Nano Developer Kit에 JetPack 6.0을 설치합니다:

```bash
# NVIDIA SDK Manager 사용 (Desktop에서)
# 또는 직접 flash:
# 1. JetPack 6.0 다운로드: https://developer.nvidia.com/embedded/jetpack
# 2. SD 카드에 flashing
sudo apt update && sudo apt upgrade -y
```

### 2.5.2 Jetson 기본 설정

```bash
# 시스템 업데이트
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git cmake vim

# CUDA 환경 변수
echo 'export CUDA_HOME=/usr/local/cuda-12.4' >> ~/.bashrc
echo 'export PATH=$CUDA_HOME/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# Jetson 성능 모드 설정
sudo nvpmodel -m 0  # MAXN 모드 (최대 성능)
sudo jetson_clocks   # 모든 클럭 최대

# SWAP 파일 설정
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### 2.5.3 ROS2 Humble on Jetson

```bash
# ROS2 Humble 설치 (aarch64)
sudo apt update && sudo apt install -y \
    ros-humble-desktop \
    python3-colcon-common-extensions

echo 'source /opt/ros/humble/setup.bash' >> ~/.bashrc
echo 'export ROS_DOMAIN_ID=42' >> ~/.bashrc
echo 'export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp' >> ~/.bashrc
source ~/.bashrc

# TurtleBot3 패키지
sudo apt install -y \
    ros-humble-turtlebot3* \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-slam-toolbox

export TURTLEBOT3_MODEL=burger
echo 'export TURTLEBOT3_MODEL=burger' >> ~/.bashrc
```

### 2.5.4 TensorRT on Jetson

Jetson에는 기본적으로 TensorRT가 포함되어 있습니다:

```bash
# TensorRT 버전 확인
dpkg -l | grep tensorrt

# ONNX Runtime 설치 (aarch64 최적화)
pip install onnxruntime-gpu
```

## 2.6 Raspberry Pi 5 설정 (Dual Robot)

### 2.6.1 Ubuntu 24.04 LTS 설치

```bash
# Raspberry Pi Imager로 Ubuntu 24.04 LTS (64-bit) Server 설치
# 또는 수동 설치:
wget https://cdimage.ubuntu.com/releases/24.04/release/ubuntu-24.04-preinstalled-server-arm64+raspi.img.xz
xz -d ubuntu-24.04-preinstalled-server-arm64+raspi.img.xz
sudo dd if=ubuntu-24.04-preinstalled-server-arm64+raspi.img of=/dev/sdX bs=4M status=progress
```

### 2.6.2 ROS2 Jazzy 설치

```bash
# ROS2 Jazzy (Ubuntu 24.04 기본)
sudo apt update && sudo apt upgrade -y
sudo apt install -y \
    ros-jazzy-desktop \
    python3-colcon-common-extensions \
    ros-jazzy-navigation2 \
    ros-jazzy-nav2-bringup \
    ros-jazzy-slam-toolbox

echo 'source /opt/ros/jazzy/setup.bash' >> ~/.bashrc
echo 'export ROS_DOMAIN_ID=42' >> ~/.bashrc
source ~/.bashrc

# TurtleBot3 패키지 (소스 빌드 필요 - 바이너리 없음)
mkdir -p ~/tb3_ws/src
cd ~/tb3_ws/src
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3.git
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
cd ~/tb3_ws
colcon build --symlink-install
echo 'source ~/tb3_ws/install/setup.bash' >> ~/.bashrc
echo 'export TURTLEBOT3_MODEL=burger' >> ~/.bashrc
source ~/.bashrc
```

## 2.7 Docker Compose 환경

**`docker/docker-compose.yaml`**:

```yaml
version: '3.8'

services:
  isaac-sim:
    image: nvcr.io/nvidia/isaac-sim:2025.2.0
    container_name: isaac-sim-ws
    runtime: nvidia
    environment:
      - DISPLAY=${DISPLAY:-:0}
      - ACCEPT_EULA=Y
      - PRIVACY_CONSENT=Y
      - OMNI_USER=admin
      - ROS_DOMAIN_ID=42
      - RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
    volumes:
      - /tmp/.X11-unix:/tmp/.X11-unix:rw
      - ../:/workspace:rw
      - ~/.nvidia-omniverse:/root/.nvidia-omniverse:rw
      - ~/.cache/ov:/root/.cache/ov:rw
      - /usr/share/vulkan/icd.d:/usr/share/vulkan/icd.d:ro
    network_mode: host
    ipc: host
    ulimits:
      memlock: -1
      stack: 67108864
    stdin_open: true
    tty: true
    command: bash

  isaac-lab:
    image: isaac-lab:latest
    build:
      context: .
      dockerfile: Dockerfile.isaac
    container_name: isaac-lab-ws
    runtime: nvidia
    environment:
      - DISPLAY=${DISPLAY:-:0}
      - ROS_DOMAIN_ID=42
    volumes:
      - ../:/workspace:rw
      - ~/.cache:/root/.cache:rw
    network_mode: host
    ipc: host
    ulimits:
      memlock: -1
      stack: 67108864
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    stdin_open: true
    tty: true
    command: bash
```

## 2.8 설치 검증

### 2.8.1 Isaac Sim 검증

```bash
# Docker 컨테이너에서 Isaac Sim 실행
cd docker
bash isaac_sim_docker.sh

# 컨테이너 내부에서:
# Isaac Sim GUI 실행
./isaac-sim.sh

# 또는 headless 모드
./isaac-sim.sh --headless
```

### 2.8.2 Isaac Lab 검증

```bash
conda activate isaaclab

# Cartpole 예제 실행 (설치 검증)
python ~/IsaacLab/scripts/train.py --task Isaac-Cartpole-Direct-v0 --headless --num_envs 64

# 학습 진행 확인 (약 5분)
# tensorboard 확인
tensorboard --logdir logs/
```

### 2.8.3 ROS2 통신 검증

```bash
# Terminal 1: ROS2 listener
ros2 topic echo /chatter

# Terminal 2: ROS2 talker
ros2 topic pub /chatter std_msgs/msg/String "data: 'Hello from Isaac Sim'"

# TurtleBot3 ROS2 토픽 확인
ros2 topic list
ros2 interface show geometry_msgs/msg/Twist
```

### 2.8.4 Jetson 환경 검증

```bash
# Jetson 확인
jtop  # jtop 설치: sudo pip3 install -U jtop

# GPU 활용도 확인
tegrastats

# TensorRT 확인
python3 -c "import tensorrt; print(tensorrt.__version__)"

# PyTorch 확인
python3 -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

## 2.9 환경 구성 체크리스트

- [ ] 호스트: NVIDIA 드라이버 설치 및 GPU 확인 (`nvidia-smi`)
- [ ] 호스트: CUDA Toolkit 12.4+ 설치
- [ ] 호스트: Docker + NVIDIA Container Toolkit 설치
- [ ] 호스트: ROS2 Humble 설치
- [ ] Docker: Isaac Sim 2025.2 이미지 풀
- [ ] Docker: Isaac Sim GUI 실행 확인
- [ ] Conda: Isaac Lab 환경 생성
- [ ] Conda: Isaac Lab 설치 확인 (Cartpole 학습)
- [ ] Conda: Cosmos 환경 생성
- [ ] Conda: Cosmos 모델 다운로드
- [ ] 네트워크: ROS2 도메인 ID 설정
- [ ] Jetson: JetPack 6.0 + ROS2 Humble 설치
- [ ] Jetson: TurtleBot3 패키지 설치
- [ ] Jetson: TensorRT 확인
- [ ] RPi: ROS2 Jazzy 설치 (Dual Robot 시)
- [ ] RPi: TurtleBot3 패키지 빌드

## 2.10 문제 해결

| 문제 | 증상 | 해결 방법 |
|------|------|-----------|
| Isaac Sim GUI 안 뜸 | `Cannot open display` | `xhost +local:docker` 실행, DISPLAY 변수 확인 |
| CUDA out of memory | Isaac Lab 학습 실패 | `--num_envs` 값을 줄이기 (64 → 32 → 16) |
| ROS2 통신 안 됨 | 토픽이 보이지 않음 | `ROS_DOMAIN_ID` 일치 확인, 방화벽 확인 |
| Docker GPU 접근 불가 | `could not select device driver` | `nvidia-ctk runtime configure --runtime=docker` 실행 |
| Isaac Lab 설치 실패 | Python 버전 충돌 | Python 3.10 정확히 사용, conda 환경 재생성 |
| Cosmos OOM | 추론 중 메모리 부족 | 배치 사이즈 1로 설정, fp16 사용 |

---


2:08 PMClaude 응답: Terminator 터미널 사용법Terminator 터미널 사용법
설치
bashsudo apt install terminator
핵심 단축키
화면 분할
단축키기능Ctrl+Shift+E세로 분할 (좌/우)Ctrl+Shift+O가로 분할 (위/아래)Ctrl+Shift+W현재 패널 닫기
패널 이동
단축키기능Alt+방향키인접 패널로 이동Ctrl+Tab다음 패널로 순환
탭
단축키기능Ctrl+Shift+T새 탭 열기Ctrl+PageUp/Down탭 전환
기타 유용한 기능
단축키기능Ctrl+Shift+X현재 패널 전체화면 토글Ctrl+Shift+Z현재 패널 줌 (나머지 숨김)Ctrl+Shift+F텍스트 검색Ctrl+Shift+C/V복사/붙여넣기Ctrl++ / Ctrl+-글자 크기 조절
실전 활용 예시 (ROS 2 개발)
Terminator는 ROS 2처럼 여러 터미널이 동시에 필요한 작업에 특히 유용합니다.
┌─────────────────┬─────────────────┐
│                 │                 │
│  ros2 launch    │  ros2 topic     │
│  turtlebot3...  │  echo /scan     │
│                 │                 │
├─────────────────┴─────────────────┤
│                                   │
│  rviz2 / rqt_graph 모니터링       │
│                                   │
└───────────────────────────────────┘
레이아웃 저장 (자주 쓰는 배치 저장)
bash# ~/.config/terminator/config 파일로 관리
# GUI에서: 우클릭 → Preferences → Layouts 탭에서 저장 가능
ROS 2 + TurtleBot3 작업 시 패널 3~4개 분할해서 launch, topic echo, rviz2, teleop 동시 실행하면 매우 편리합니다.

---


[원인 분석]
ros2 CLI 도구 바로 뒤에는 핵심 서브 명령어(run, topic, node, launch 등)인 Verb가 와야 합니다. rqt_image_view는 ros2 도구의 직속 하위 명령어가 아닌 독립된 패키지/실행파일이므로 ros2 바로 뒤에 배치하면 문법 오류가 발생합니다.

[해결 방법]
방법 1 (추천): ros2 run 명령어를 통해 패키지명과 실행파일명 명시하기

Bash
ros2 run rqt_image_view rqt_image_view --ros-args -r image:=/rgb
방법 2: 환경 변수가 잡혀있을 경우 단독 실행파일로 직접 호출하기

Bash
rqt_image_view
2. 다중 카메라 토픽 및 데이터 확인 (camera_1, camera_2)
[문제 상황]
환경 내에 camera_1:depth, camera_1:rgb, camera_2:rgb, camera_2:depth 총 4개의 토픽이 관찰됨. 상황에 맞게 개별 혹은 동시 모니터링이 필요함.

[해결 방법]
A. 특정 카메라 피드만 지정하여 실행 (리맵핑 옵션 사용)
Bash
# camera_1의 RGB 및 Depth 영상 확인
ros2 run rqt_image_view rqt_image_view --ros-args -r image:=/camera_1/rgb
ros2 run rqt_image_view rqt_image_view --ros-args -r image:=/camera_1/depth

# camera_2의 RGB 및 Depth 영상 확인
ros2 run rqt_image_view rqt_image_view --ros-args -r image:=/camera_2/rgb
ros2 run rqt_image_view rqt_image_view --ros-args -r image:=/camera_2/depth
B. RQt GUI 내부에서 수동 전환
단순히 rqt_image_view 명령어로 창을 띄운 뒤, 왼쪽 상단의 드롭다운 메뉴를 활용해 camera_1/rgb나 camera_2/depth 등 원하는 토픽을 클릭하며 전환 가능.

C. 종합 GUI 툴(rqt)을 활용한 4분할 동시 모니터링
터미널에 rqt 입력하여 실행.

상단 메뉴에서 Plugins -> Visualization -> Image View를 선택해 플러그인을 추가하는 과정을 4번 반복.

4개의 각 플러그인에 camera_1:rgb, camera_1:depth, camera_2:rgb, camera_2:depth를 각각 할당하여 한눈에 모니터링.

3. RViz 설치 및 ROS 버전 혼동 문제 (RViz 1 vs RViz 2)
[문제 상황]
사용자가 Isaac Sim 튜토리얼의 RTX Lidar 설정을 보려고 rviz -d ... 명령어를 실행했으나, Command 'rviz' not found 메시지를 확인하고 sudo apt install rviz로 설치를 진행함.
설치 후 로그에 rviz version 1.14.14가 출력되며 ROS 2 토픽이 비정상적으로 연동될 여지가 생김.

Bash
(base) gotree94@gotree94-ROG-Strix-SCAR-16-G635LX-G635LX:~$ rviz -d ~/IsaacSim-ros_workspaces/humble_ws/src/isaac_tutorials/rviz2/rtx_lidar.rviz 
[ INFO] [1780130112.155977504]: rviz version 1.14.14
[ INFO] [1780130112.156005736]: compiled against Qt version 5.15.2
[ INFO] [1780130112.156009442]: compiled against OGRE version 1.12.10 (Rhagorthua)
[원인 분석]
사용자의 작업 환경은 ROS 2 Humble입니다.

sudo apt install rviz 명령어로 설치되는 기본 패키지는 과거 ROS 1용 RViz(버전 1.x)입니다. ROS 1용 RViz는 ROS 2 환경의 DDS 통신 토픽을 받아오지 못하므로 정상적인 Lidar 데이터 시각화가 불가능합니다.

ROS 2 환경에서는 rviz2 패키지를 명시적으로 설치하고 실행해야 합니다.

[해결 방법]
ROS 2 Humble 전용 RViz 2 설치:

Bash
sudo apt update
sudo apt install ros-humble-rviz2
ROS 2용 RViz 2 실행 명령어 적용:
기존에 잘못 켜진 RViz 1 창을 종료하고, 아래와 같이 명시적으로 rviz2 명령어를 통해 환경 설정(.rviz) 파일을 로드합니다.

Bash
rviz2 -d ~/IsaacSim-ros_workspaces/humble_ws/src/isaac_tutorials/rviz2/rtx_lidar.rviz
(참고) Command Not Found 발생 시 환경 변수 로드:
만약 명령어 호출이 안 될 경우, 현재 터미널 세션에 ROS 2 환경 변수가 유실된 것이므로 아래 명령어를 먼저 수행합니다.

Bash
source /opt/ros/humble/setup.bash
rviz2 -d ~/IsaacSim-ros_workspaces/humble_ws/src/isaac_tutorials/rviz2/rtx_lidar.rviz
"""

Save to file
file_name = "ros2_isaac_sim_debugging_report.md"
with open(file_name, "w", encoding="utf-8") as f:
f.write(markdown_content)

print(f"File successfully created: {file_name}")

요청하신 디버깅 내용을 보기 쉽게 정리하여 마크다운(.md) 파일로 생성했습니다. 

명령어 에러 원인 분석부터 카메라 토픽 세부 매핑 방법, 그리고 ROS 1 RViz 혼동 이슈 해결까지 단계별로 상세히 기록해 두었습니다. 나중에 참고하시거나 문서화 자료로 활용하기 좋습니다.

Your Markdown file is ready
[file-tag: code-generated-file-0-1780131303368917888]

### 📝 생성된 마크다운 파일 내용 미리보기

```markdown
# ROS 2 및 Isaac Sim 디버깅 리포트

본 문서는 ROS 2 Humble 환경에서 Isaac Sim 연동 중 발생한 명령어 오류, 이미지 토픽 모니터링 방법, 그리고 RViz 버전 혼동 문제를 해결한 과정을 기록한 디버깅 리포트입니다.

---

## 1. `ros2 rqt_image_view` 실행 오류 및 해결

### [문제 상황]
사용자가 `ros2 rqt_image_view rqt_image_view /rgb` 명령어를 입력했으나 CLI 파싱 에러가 발생함.

### [원인 분석]
`ros2` CLI 도구 바로 뒤에는 핵심 서브 명령어(`run`, `topic`, `node` 등)인 **Verb**가 와야 합니다. `rqt_image_view`는 독립된 패키지/실행파일이므로 `ros2` 바로 뒤에 배치하면 문법 오류가 발생합니다.

### [해결 방법]
* **방법 1 (추천):** `ros2 run` 명령어를 통해 패키지명과 실행파일명 명시하기
  ```bash
  ros2 run rqt_image_view rqt_image_view --ros-args -r image:=/rgb
방법 2: 환경 변수가 잡혀있을 경우 단독 실행파일로 직접 호출하기

Bash
rqt_image_view
2. 다중 카메라 토픽 및 데이터 확인 (camera_1, camera_2)
[문제 상황]
환경 내에 camera_1:depth, camera_1:rgb, camera_2:rgb, camera_2:depth 총 4개의 토픽이 관찰되어 이에 맞는 실행 옵션이 필요함.

[해결 방법]
A. 특정 카메라 피드만 지정하여 실행 (리맵핑 옵션 사용)
Bash
# camera_1의 RGB 및 Depth 영상 확인
ros2 run rqt_image_view rqt_image_view --ros-args -r image:=/camera_1/rgb
ros2 run rqt_image_view rqt_image_view --ros-args -r image:=/camera_1/depth

# camera_2의 RGB 및 Depth 영상 확인
ros2 run rqt_image_view rqt_image_view --ros-args -r image:=/camera_2/rgb
ros2 run rqt_image_view rqt_image_view --ros-args -r image:=/camera_2/depth
B. RQt GUI 내부에서 수동 전환
rqt_image_view 명령어로 창을 띄운 뒤, 왼쪽 상단의 드롭다운 메뉴를 활용해 원하는 토픽을 클릭하며 전환 가능.

C. 종합 GUI 툴(rqt)을 활용한 4분할 동시 모니터링
터미널에 rqt 입력하여 실행.

상단 메뉴에서 Plugins -> Visualization -> Image View를 선택해 플러그인을 추가하는 과정을 4번 반복하여 한 화면에 배치 후 각각 토픽 할당.

3. RViz 설치 및 ROS 버전 혼동 문제 (RViz 1 vs RViz 2)
[문제 상황]
RTX Lidar 설정을 위해 rviz 패키지를 설치했으나, 실행 로그에 rviz version 1.14.14가 출력되며 구버전 프로그램이 실행됨.

[원인 분석]
현재 작업 환경은 ROS 2 Humble입니다.

sudo apt install rviz 명령어로 설치되는 기본 패키지는 과거 ROS 1용 RViz(버전 1.x)입니다. ROS 1용 RViz는 ROS 2 환경의 토픽을 받아오지 못하므로 정상적인 시각화가 불가능합니다.

ROS 2 환경에서는 rviz2 패키지를 사용해야 합니다.

[해결 방법]
ROS 2 Humble 전용 RViz 2 설치:

Bash
sudo apt update
sudo apt install ros-humble-rviz2
ROS 2용 RViz 2 실행 명령어 적용:

Bash
rviz2 -d ~/IsaacSim-ros_workspaces/humble_ws/src/isaac_tutorials/rviz2/rtx_lidar.rviz
(참고) 환경 변수 재로드:
명령어를 찾을 수 없다면 터미널에 ROS 2 환경을 소싱한 후 재실행합니다.

Bash
source /opt/ros/humble/setup.bash
rviz2 -d ~/IsaacSim-ros_workspaces/humble_ws/src/isaac_tutorials/rviz2/rtx_lidar.rviz

