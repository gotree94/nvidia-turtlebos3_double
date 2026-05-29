# IsaacSim TurtleBot3 ROS2 Tutorial <br> (turtlebot3 불러오고 ROS2 연결)

* 이번시간에는 ROS의 대표적인 예제인 turtlesim 대신 isaacsim에서 turtlebot을 불러오고
* turtlesim 제어처럼 터미널로 제어를 해보도록 하겠습니다.
* 이를 위해 IsaacSim과 ROS2를 연결하겠습니다.

> **참고 링크**: https://docs.omniverse.nvidia.com/isaacsim/latest/ros2_tutorials/tutorial_ros2_turtlebot.html

---

## 1. URDF Import: Turtlebot

Omniverse Isaac Sim에는 ROS 시스템과의 통합을 용이하게 해주는 여러 도구가 있습니다.
Isaac Sim에는 Omnigraph 노드 형태의 ROS와 ROS2 브리지, URDF 임포터, 그리고 Gazebo/Ignition에 대한 연결을 모두 갖추고 있습니다.

### 학습 목표

해당 예제에서 URDF importer를 사용하여 Turtlebot3를 Isaac Sim으로 가져옵니다.

---

### Importing TurtleBot URDF

먼저 ROS workspace를 set up합니다.

아래 깃허브 레파지토리 링크에서 Isaac Sim ROS Workspace를 Clone합니다.

```bash
cd ~
git clone https://github.com/isaac-sim/IsaacSim-ros_workspaces.git
```

그리고 아래 위치로 이동:

```bash
cd ~/IsaacSim-ros_workspaces/humble_ws/src
```

이 위치에서 turtlebot3 소스 클론:

```bash
git clone -b humble-devel https://github.com/ROBOTIS-GIT/turtlebot3.git turtlebot3
```

#### Isaac Sim에서 Simple Room 불러오기

Isaac Sim을 열고 Content에서 아래 경로로 이동:

```
omniverse://localhost/NVIDIA/Assets/Isaac/4.2/Isaac/Environments/Simple_Room/
```

`simple_room.usd`를 찾아 드래그 앤 드롭하여 Stage에 추가합니다.

---

### Turtlebot 불러오기 (URDF Importer 방식)

1. **Top menu bar**에서 **Isaac Utils > Workflows > URDF Importer** 선택
2. **Fix Base Link** 체크박스 **체크 해제**
3. **Joint Drive Type**을 `Position` → `Velocity`로 변경
4. **Input 섹션**에서 **Input File** 선택 후 아래 경로의 파일 선택:
   ```
   ~/IsaacSim-ros_workspaces/humble_ws/src/turtlebot3/turtlebot3_description/urdf/turtlebot3_burger.urdf
   ```
5. **Import 섹션**에서 **Output Directory**는 `Desktop` 선택
6. **Import** 버튼 클릭

> 💡 **참고**: 이렇게 복잡하게 URDF를 import하는 방법을 보여준 것은, 실제 URDF 파일을 Isaac Sim으로 가져오는 과정(Isaac Utils > Workflows > URDF Importer)을 설명하기 위함입니다. 사실 Isaac Assets에서 `turtlebot`을 검색해서 바로 가져올 수도 있습니다.

---

### Tune the Robot

URDF 가져오기 기능은 일치하는 카테고리가 있는 재료, 물리적 및 조인트 속성을 자동으로 가져옵니다. 하지만 일치하는 카테고리가 없거나 두 시스템 간의 단위가 다른 경우 자동으로 채워지는 값이 정확하지 않을 수 있습니다.

#### 1. Frictional Properties
로봇 바퀴가 미끄러지는 경우 바퀴의 마찰 계수와 지면의 마찰 계수를 변경해보세요.

#### 2. Physical Properties
명확한 질량/관성 속성이 없으면 물리 엔진이 geometry mesh에서 이를 추정합니다. 질량 및 관성 속성을 업데이트하려면:
- 해당 prim의 **Property 탭**에서 **Physics > Rigid Body** 확인
- **Physics > Mass** 범주에서 값 수정 또는 `+Add` 버튼으로 추가

#### 3. Joint Properties
관절이 진동하거나 너무 느리게 움직이는 경우:
- **stiffness(강성)**: 높을수록 목표에 빠르고 강하게 도달
- **damping(감쇠)**: 높을수록 부드럽지만 느려짐
- **Position drive**: 높은 stiffness + 낮은 damping
- **Velocity drive**: stiffness = 0, damping ≠ 0

---

### Differential Controller로 키보드 조작

1. **Menu bar > Isaac Utils > Common Omnigraphs > Differential Controller**
2. **Robot Prim**에 `Add` 버튼 클릭 → `turtlebot3_burger` 선택 → `Select`
3. 아래 값 입력:
   - **wheel radius**: `0.025`
   - **distance between wheels**: `0.16`
   - **Use keyboard Control (WASD)**: ✅ 체크
4. `OK` 버튼 클릭

> 위 값은 Turtlebot3 Burger의 스펙을 참고한 것입니다.

5. **Stage**에 `Graphs` 하위에 `differential_controller`가 생성됨 → 우클릭 > **Open Graph** → Action Graph 창에서 시각적 확인
6. **재생(Play) 버튼** 누르고 **WASD 키**로 조작
7. 로봇이 움직입니다.

---

## 2. Driving TurtleBot via ROS messages

ROS 브릿지에는 사용하기 편리하도록 패키징된 몇 가지 인기 있는 rostopic이 함께 제공됩니다.

### 학습 목표

Turtlebot3가 ROS 네트워크를 통해 주행하고 Twist 메시지를 subscribe 하도록 합니다.

- Turtlebot3에 컨트롤러 추가
- ROS 브리지와 ROS OmniGraph(OG) 노드 소개
- ROS Twist 메시지로 구동되는 로봇 설정

---

### 2.1 Driving the Robot

두 개의 바퀴가 달린 로봇인 Turtlebot3의 경우, 필요한 노드는:
- **Differential Controller**(차동 제어기): 차량 속도를 바퀴 속도로 변환
- **Articulation Controller**(관절 제어기): 명령을 joint drives로 전송

---

### 2.2 Connecting to ROS

Isaac Sim은 특정 메시지의 subscriber/publisher 노드와 유틸리티 노드(Context, Clock 등)를 제공합니다.

ROS 브리지 설정 일반화 단계:
1. Action Graph를 엽니다
2. 원하는 ROS2 topic과 관련된 OG 노드를 추가합니다
3. 필요에 따라 속성(properties)을 수정합니다
4. 데이터 파이프라인을 연결합니다

---

### 2.3 Building the Graph

#### Extensions 확인
**Window > Extensions**에서:
- **ROS bridge**: ❌ 비활성화
- **ROS2 bridge**: ✅ 활성화

#### Action Graph 생성 및 노드 연결

1. **Window > Visual Scripting > Action Graph** 열기
2. **새 Action Graph 아이콘** 클릭
3. 왼쪽 패널에서 필요한 OG 노드 검색 후 드래그 앤 드롭

#### 필요한 노드 및 설정

| 노드 | 역할 |
|------|------|
| **On Playback Tick** | 시뮬레이션 재생 중 틱 생성 |
| **ROS2 Context** | ROS2 DDS 도메인 컨텍스트 생성 |
| **ROS2 Subscribe Twist** | `/cmd_vel` Twist 메시지 구독 |
| **Scale To/From Stage Unit** | 입력값을 stage 단위로 변환 |
| **Break 3-Vector** | 3차원 벡터를 개별 요소로 분해 |
| **Differential Controller** | 차량 속도 → 바퀴 속도 변환 |
| **Articulation Controller** | 관절 구동 명령 전송 |
| **Constant Token** (x2) | wheel_left_joint, wheel_right_joint |
| **Make Array** | 토큰 배열 생성 |

#### 연결 순서

1. **Differential Controller** + **Articulation Controller** 검색 → 드래그 → Velocity Command 연결
2. **Articulation Controller** 선택 > Properties > `targetPrim`에서 `turtlebot3_burger` 선택
3. **Differential Controller** Properties에 wheel radius / distance 입력
4. **Constant Token** 2개 추가 → 각각 `wheel_left_joint`, `wheel_right_joint` 입력
5. **Make Array** 추가 → `+` 버튼으로 입력 2개로 확장 → Constant Token 2개 연결 → Array 출력을 Articulation Controller의 `Joint Names`에 연결
6. **On Playback Tick** 추가 → `deltaSeconds`를 Differential Controller의 `dt`에 연결
7. **ROS2 Subscribe Twist** 추가 → `topicName`을 `/cmd_vel`로 설정
8. **Break 3-Vector** 2개 추가 → Linear X / Angular Z를 Differential Controller에 연결
9. **Scale To/From Stage Unit** 추가 (필요시)

---

### 2.4 Graph Explained

| 노드 | 설명 |
|------|------|
| **On Playback Tick** | 시뮬레이션이 "재생" 중일 때 틱 생성. 수신 노드는 모든 시뮬레이션 단계에서 compute 함수 실행 |
| **ROS2 Context** | ROS2 DDS 컨텍스트 생성. 기본 도메인 ID는 0. 환경변수 `ROS_DOMAIN_ID` 사용 가능 |
| **ROS2 Subscribe Twist** | `/cmd_vel` Twist 메시지 구독 |
| **Scale To/From Stage Unit** | inputs를 stage 단위로 변환 |
| **Break 3-Vector** | Twist 노드 출력(linear/angular 3차원 벡터)을 분해 → Differential Controller에 z축 전진속도/회전속도만 공급 |
| **Articulation Controller** | 대상 로봇에 할당, joint 이름/index를 받아 명령 실행. On Playback Tick에 체크되어 있어 새 메시지가 없어도 이전 명령 유지 |
| **Differential Controller** | 차량 속도 → 바퀴 속도 계산. wheel radius, wheel distance 필요 |

---

### 2.5 Verifying ROS connections

1. **재생(Play) 버튼** 클릭
2. 별도 터미널에서 ROS2 토픽 확인:

```bash
ros2 topic list
```

> ⚠️ **첫 실행 시 오류 발생 가능**:
> ```
> ImportError: /opt/ros/humble/lib/librcl_logging_spdlog.so: undefined symbol: ...
> ```
> 해결 방법: https://cafe.naver.com/isaacsimkr/12 참고

3. Twist 메시지 발행하여 로봇 제어:

```bash
# 앞으로 이동
ros2 topic pub /cmd_vel geometry_msgs/Twist "{'linear': {'x': 0.2, 'y': 0.0, 'z': 0.0}, 'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}}"

# 정지
ros2 topic pub /cmd_vel geometry_msgs/Twist "{'linear': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}}"
```

4. 키보드 텔레옵 설치 및 실행:

```bash
sudo apt-get install ros-$ROS_DISTRO-teleop-twist-keyboard
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
