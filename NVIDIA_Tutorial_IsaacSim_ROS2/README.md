# Isaac Lab

## Overview

Isaac Lab is the official robot learning framework for Isaac Sim, providing APIs and examples for reinforcement learning, imitation learning, and more. The framework provides the ability to design tasks in different workflows, including a modular design to easily and efficiently create robot learning environments, while leveraging the latest simulation capabilities.

Some of its core features include:

- Modular configuration-driven system to easily create and modify environments
- Flexible user-designed workflow for optimized performance
- Suite of robot learning environments for training and evaluation
- Support for different reinforcement learning and imitation learning libraries
- Connection to peripheral devices, such as game-pads and keyboards, for collecting demonstrations
- Ability to augment simulation with custom actuator models for sim-to-real transfer

---

## Isaac Lab Resources

For more information and documentation for Isaac Lab, see the following external references:

- [Isaac Lab Repository](https://github.com/isaac-sim/IsaacLab)
- [Isaac Lab Documentation](https://isaac-sim.github.io/IsaacLab/)

---

## Suggested Isaac Sim Tutorials

The following set of tutorials details usage of reinforcement learning related components in Isaac Sim.

- **Robot Setup**
  - [Importing URDF](https://docs.omniverse.nvidia.com/isaacsim/latest/ros2_tutorials/tutorial_ros2_urdf_import.html)
  - [Importing MJCF](https://docs.omniverse.nvidia.com/isaacsim/latest/tutorials/import_mjcf.html)
- **Simulation Fundamentals**
  - [Deploying Policies](https://docs.omniverse.nvidia.com/isaacsim/latest/tutorials/deploy_policy.html)
  - [Rigging a Legged Robot for Policy Inference](https://docs.omniverse.nvidia.com/isaacsim/latest/tutorials/rigging_legged_robot.html)
- **Policy Deployment**
  - [Policy Deployment](https://docs.omniverse.nvidia.com/isaacsim/latest/tutorials/deploy_policy.html)
  - [Policy Deployment in ROS 2](https://docs.omniverse.nvidia.com/isaacsim/latest/ros2_tutorials/tutorial_ros2_policy_deployment.html)
- **Data Generation**
  - [Getting Started with Cloner](https://docs.omniverse.nvidia.com/isaacsim/latest/tutorials/cloner_tutorial.html)
  - [Instanceable Assets](https://docs.omniverse.nvidia.com/isaacsim/latest/tutorials/instanceable_assets.html)
- **Python Scripting**
  - [Python Scripting](https://docs.omniverse.nvidia.com/isaacsim/latest/tutorials/python_scripting.html)

---

## Troubleshooting

### Isaac Lab Troubleshooting

Common Isaac Lab issues and their solutions are documented in the [Isaac Lab Troubleshooting](https://isaac-sim.github.io/IsaacLab/source/refs/troubleshooting.html) page. For general simulation troubleshooting, see [Troubleshooting](https://docs.omniverse.nvidia.com/isaacsim/latest/troubleshooting.html).

---

## Deprecated Frameworks

Isaac Lab will be replacing previously released frameworks for robot learning and reinforcement learning, including IsaacGymEnvs for the Isaac Gym Preview Release, OmniIsaacGymEnvs for Isaac Sim, and Orbit for Isaac Sim.

These frameworks are now deprecated in favor of continuing development in Isaac Lab. We encourage users of these frameworks to migrate your work over to Isaac Lab. Migration guides are available to support the migration process:

- **Migrating from IsaacGymEnvs and Isaac Gym Preview Release**: [link](https://isaac-sim.github.io/IsaacLab/source/migration/isaacgymenvs.html)
- **Migrating from OmniIsaacGymEnvs**: [link](https://isaac-sim.github.io/IsaacLab/source/migration/omniisaacgymenvs.html)
- **Migrating from Orbit**: [link](https://isaac-sim.github.io/IsaacLab/source/migration/orbit.html)

---

## Deploying Policies in Isaac Sim

The objective of this tutorial is to explain the process of deploying a policy trained in Isaac Lab by going through an example and exploring robot definition files.

There are many use cases in which you might want to deploy your policy in Isaac Sim; such as enabling robots to accomplish more complex locomotion, testing and integrating the policy with other stacks such as navigation and localization in simulated environments, and interfacing it using with existing bridges such as ROS 2.

### Learning Objectives

In this tutorial, you will walk through the policy based robot examples:

- H1 and Spot flat terrain policy controller demo
- Training and exporting policies in Isaac Lab
- Reading the environment parameter file from Isaac Lab
- Robot definition class
- Position to torque conversion
- Debugging tips
- Sim to Real deployment

---

## Demos

First activate **Windows > Examples > Robotics Examples** which will open the **Robotics Examples** tab.

### Unitree H1 Humanoid Example

The Unitree H1 humanoid example can be accessed by creating an empty stage.

1. Open the example using **Robotics Examples > POLICY > Humanoid**.
2. Press **LOAD** to open the scene.

This example uses the H1 Flat Terrain Policy trained in Isaac Lab to control the humanoid's locomotion.

**Controls:**

| Action | Key |
|--------|-----|
| Forward | UP ARROW / NUM 8 |
| Turn Left | LEFT ARROW / NUM 4 |
| Turn Right | RIGHT ARROW / NUM 6 |

### Boston Dynamics Spot Quadruped Example

The Boston Dynamics Spot quadruped example can be accessed by creating an empty stage.

1. Open the example using **Robotics Examples > POLICY > Quadruped**.
2. Press **LOAD** to open the scene.

This example uses the Spot Flat Terrain Policy trained in Isaac Lab to control the quadruped's locomotion.

**Controls:**

| Action | Key |
|--------|-----|
| Forward | UP ARROW / NUM 8 |
| Backward | DOWN ARROW / NUM 2 |
| Move Left | LEFT ARROW / NUM 4 |
| Move Right | RIGHT ARROW / NUM 6 |
| Turn Left | N / NUM 7 |
| Turn Right | M / NUM 9 |

> **Note**
> See [Isaac Sim Policy Example Extension](https://docs.omniverse.nvidia.com/isaacsim/latest/tutorials/deploy_policy.html) document for standalone example workflow and the policy files used in the examples.

---

## Training and Exporting Policies in Isaac Lab

### Training

Training the policy from Isaac Lab is the first step to deploying the policy. Consult the Isaac Lab tutorials for training an existing or custom policy.

The policies trained used in the examples above are `Isaac-Velocity-Flat-H1-v0` for the Unitree H1 humanoid and `Isaac-Velocity-Flat-Spot-v0` for the Boston Dynamics Spot robot.

> **Note**
> For example, in Isaac Lab 2.0, use the following command to train the H1 flat terrain policy:
> ```bash
> ./isaaclab.sh -p scripts/reinforcement_learning/rsl_rl/train.py --task Isaac-Velocity-Flat-H1-v0 --headless
> ```

### Exporting

Policies trained using RSL_rl can be exported using the `scripts/reinforcement_learning/rsl_rl/play.py` inside the Isaac Lab workspace. The exported files are generated in the `exported` folder.

It is also possible to inference using a policy trained in a different framework or with an iteration snapshot, however additional data such as neural network structure may be required. Follow the documentation of your desired framework for more information.

> **Note**
> For example, in Isaac Lab 2.0, use the following command to export the H1 flat terrain policy:
> ```bash
> ./isaaclab.sh -p scripts/reinforcement_learning/rsl_rl/play.py --task Isaac-Velocity-Flat-H1-v0 --num_envs 32
> ```

> **Note**
> The trained policy files used in the examples are available to download [here](https://docs.omniverse.nvidia.com/isaacsim/latest/tutorials/deploy_policy.html#training-and-exporting-policies-in-isaac-lab).

---

## Understanding the Environment Parameter File

The `agent.yaml` and `env.yaml` are generated with trained policies to describe the policy configurations and they are located in the `logs/rsl_rl/<task_name>/<time>/params/` folder.

- `agent.yaml` describes the neural network parameters.
- `env.yaml` describes the environment and robot configurations.

The below snippets are taken from `Isaac-Velocity-Flat-H1-v0`.

### Simulation Setup

```yaml
sim:
  dt: 0.005
  render_interval: 4
  gravity: [0.0, 0.0, -9.81]
  enable_scene_query_support: false
  use_fabric: true
  disable_contact_processing: true
  use_gpu_pipeline: true
  device: "cuda:0"
```

The first snippet describes the simulation environment, the simulation physics is required to run at 0.005s (200 Hz), with gravity pointing downwards at 9.81 m/s².

### Robot Setup

The `scene:robot:init_state` section describes the robot's initial position, orientation, velocity, as well as default joint position and velocity.

```yaml
init_state:
  pos: [0.0, 0.0, 1.05]
  rot: [1.0, 0.0, 0.0, 0.0]
  lin_vel: [0.0, 0.0, 0.0]
  ang_vel: [0.0, 0.0, 0.0]
  joint_pos:
    .*_hip_yaw: 0.0
    .*_hip_roll: 0.0
    .*_hip_pitch: -0.28
    .*_knee: 0.79
    .*_ankle: -0.52
    torso: 0.0
    .*_shoulder_pitch: 0.28
    .*_shoulder_roll: 0.0
    .*_shoulder_yaw: 0.0
    .*_elbow: 0.52
  joint_vel:
    .*: 0.0
```

The `scene:robot:init_state:actuators` section below describes the robot joint properties such as effort and velocity limit, stiffness and damping.

```yaml
actuators:
  legs:
    class_type: "ImplicitActuator"
    joint_names_expr:
      - .*_hip_yaw
      - .*_hip_roll
      - .*_hip_pitch
      - .*_knee
      - torso
    effort_limit: 300
    velocity_limit: 100.0
    stiffness:
      .*_hip_yaw: 150.0
      .*_hip_roll: 150.0
      .*_hip_pitch: 200.0
      .*_knee: 200.0
      torso: 200.0
    damping:
      .*_hip_yaw: 5.0
      .*_hip_roll: 5.0
      .*_hip_pitch: 5.0
      .*_knee: 5.0
      torso: 5.0
```

### Observations Parameters

The observation parameters describes the observations required by the policy, as well as scale or clipping factors that need to be applied to the observation.

```yaml
observations:
  policy:
    concatenate_terms: true
    enable_corruption: true
    base_lin_vel:
      func: "base_lin_vel"
      noise:
        func: "uniform_noise"
        operation: add
        n_min: -0.1
        n_max: 0.1
      clip: null
      scale: null
```

### Actions Parameters

The actions parameters describes the action outputted by the policy, as well as scaling factors and offsets that need to be applied to the actions.

```yaml
actions:
  joint_pos:
    class_type: "JointPositionAction"
    asset_name: robot
    debug_vis: false
    joint_names:
      - .*
    scale: 0.5
    offset: 0.0
    use_default_offset: true
```

### Commands Parameters

Finally, the command section describes the type of command for the policy, as well as acceptable command ranges for the policy.

```yaml
commands:
  base_velocity:
    class_type: "UniformVelocityCommand"
    resampling_time_range: [10.0, 10.0]
    debug_vis: true
    asset_name: robot
    heading_command: true
    heading_control_stiffness: 0.5
    rel_standing_envs: 0.02
    rel_heading_envs: 1.0
    ranges:
      lin_vel_x: [0.0, 1.0]
      lin_vel_y: [0.0, 0.0]
      ang_vel_z: [-1.0, 1.0]
      heading: [-3.14159, 3.14159]
```

---

## Policy Controller Class

The robot definition class defines the robot prim, imports the robot policy, sets up the robot configurations, builds the observation tensor, and finally applies the policy control action to the robot.

### Constructor

The Constructor will spawn the robot USD, and create a single articulation object for controlling the robot.

### Load Policy

This class will load in the policy file and the corresponding environment file which the policy controller will use to set up the Isaac Sim environment.

### Initialize

The `initialize` function must be called once after simulation started. The purpose of this function is to match the robot configurations to the policy, by setting the robot effort mode, control mode, joint gains, joint max effort, joint max velocity, and articulation root.

### `_set_articulation_prop`

This function parses the articulation root property and sets these properties to the robot.

### `_compute_action`

This function will compute the action from the observation.

### `_compute_observation`

This function must be overloaded by the inherited class and it is called by `advance()` during every physics step. The purpose of this function is to create an observation tensor in the format expected by the policy. For example, the code snippet below creates the observation tensor for the H1 flat terrain policy.

```python
obs = np.zeros(69)
# Base lin vel
obs[:3] = self._base_vel_lin_scale * lin_vel_b
# Base ang vel
obs[3:6] = self._base_vel_ang_scale * ang_vel_b
# Gravity
obs[6:9] = gravity_b
# Command
obs[9] = self._base_vel_lin_scale * command[0]
obs[10] = self._base_vel_lin_scale * command[1]
obs[11] = self._base_vel_ang_scale * command[2]
# Joint states
current_joint_pos = self.get_joint_positions()
current_joint_vel = self.get_joint_velocities()
obs[12:31] = current_joint_pos - self._default_joint_pos
obs[31:50] = current_joint_vel
# Previous Action
obs[50:69] = self._previous_action
```

> **Note**
> Remember to multiply the observation terms by the observation scale specified in the `env.yaml`.

### Forward

This function must be overloaded by the inherited class and is called every physics step to generate control action for the robot. For example, the code snippet below creates the controls for the H1 flat terrain policy.

```python
if self._policy_counter % self._decimation == 0:
    obs = self._compute_observation(command)
    self.action = self._compute_action(obs)
    self._previous_action = self.action.copy()

action = ArticulationAction(joint_positions=self.default_pos + (self.action * self._action_scale))
self.robot.apply_action(action)

self._policy_counter += 1
```

> **Note**
> - The policy does not need to be called every step, refer to the decimation parameter in `env.yaml`.
> - Remember to multiply the action output by the action scale specified in `env.yaml`.

> **Warning**
> For position based controls, do not use `set_joint_position()` as that will teleport the joint to the desired position.

---

## Position to Torque Controls

Some robots may require torque control as output. If the policy generates position as an output, then you must convert position to torque. There are many ways to do this, here an actuator network is used to convert position to torque.

The actuator network class is defined in `source/extensions/isaacsim.robot.policy.examples/isaacsim/robot/policy/examples/utils/actuator_network.py`. The actuator network policy for the Anymal robot is stored on the Content Browser at **SAMPLES > POLICY > ANYMAL_POLICIES**.

### Import Policy

For our LSTMSeaNetwork implementation, the policy file is loaded into the helper actuator network using the snippet below from the Anymal Flat Terrain Policy class:

```python
def initialize(self, physics_sim_view=None) -> None:
    """
    Initialize the articulation interface, set up drive mode
    """
    super().initialize(physics_sim_view=physics_sim_view, control_mode="effort")

    # Actuator network
    assets_root_path = get_assets_root_path()
    file_content = omni.client.read_file(
        assets_root_path + "/Isaac/Samples/Policies/Anymal_Policies/sea_net_jit2.pt"
    )[2]
    file = io.BytesIO(memoryview(file_content).tobytes())
    self._actuator_network = LstmSeaNetwork()
    self._actuator_network.setup(file, self.default_pos)
    self._actuator_network.reset()
```

### Run the Actuator Network

In the `advance` function, insert the position outputs from the locomotion policy into the actuator network and apply the torque to the robot using the snippet below:

```python
current_joint_pos = self.get_joint_positions()
current_joint_vel = self.get_joint_velocities()

joint_torques, _ = self._actuator_network.compute_torques(
    current_joint_pos, current_joint_vel, self._action_scale * self.action
)

self.set_joint_efforts(joint_torques)
```

---

## Debugging Tips

If your robot doesn't work right away, you can use the following tips to start debugging:

### Verify Your Policy

You can start by verifying that your policy is working properly by playing it in Isaac Lab.

Remember to use the correct `play.py` for your workflow and select the correct task.

### Verify the Robot Joint Properties

#### Robot Joint Order

If the policy is working on Isaac Lab, then you should verify the joint order of the robot, joint properties, and default joint positions.

To see the joint order, open your asset USD, create an articulation with the robot prim, start the simulation, initialize articulation, and call the `dof_names` function.

```python
# Open your USD and PLAY the simulation before running this snippet
prim = Articulation(prim_path=<your_robot_prim_path>)
prim.initialize()
print(str(prim.dof_names))
```

Print out the `dof_names` for both the Isaac Sim asset and the asset you used to train in Isaac Lab, make sure that the names and orders match exactly.

#### Default Joint Position

After you have the joint positions, verify that your default joint positions are inserted correctly. If the joint positions are incorrect, the robot joints will not go to the correct position.

#### Robot Joint Properties

If you observe the joints are moving too much or not enough, then the joint properties may not be set up correctly.

```python
# Open your USD and PLAY the simulation before running this snippet
prim = Articulation(prim_path=<your_robot_prim_path>)
prim.initialize()
print(str(prim.dof_properties))
```

Then, you can compare the joint properties with the env YAML file generated by Isaac Lab. Check the articulation API documentation for the properties for the DOFs.

### Verify the Simulation Environment

If the robot matches exactly and the inference examples are still not working, then it's time to check the simulation parameters.

#### Physics Scene

The physics scene describes the time stepping with **Time Steps Per Second (Hz)**, so take the inverse of the `dt` parameter in the `env.yaml` and set this correctly. Also match the physics scene properties with the physx section of the `env.yaml` file.

### Verify the Observation and Action Tensor

Finally, verify the observation and action tensors, and make sure your tensor structures are correct, the data passed in to the tensors are correct, and the correct scale factors are applied to the input and outputs.

Also, make sure the actions output from the policy matches the expected type of inputs of articulation and are in the correct order to correctly power the robot.

---

## Sim To Real Deployment

Congratulations, your robot and policy are working correctly in Isaac Sim now and you have tested it with the rest of your stack. Now it's time to deploy it on a real robot.

Please read this article on [deploying a reinforcement learning policy to a Spot robot](https://devblogs.nvidia.com/deploying-robust-locomotion-policies-to-a-real-robot/).

## Running a Reinforcement Learning Policy through ROS 2 and Isaac Sim

### Learning Objectives

In this example, you learn to run a reinforcement learning policy through ROS 2 and Isaac Sim. You will learn to:

- Setup a ROS 2 node to publish observations and receive actions from Isaac Sim for the H1 flat terrain locomotion policy
- Setup Isaac Sim environment to run a reinforcement learning policy

---

### Getting Started

#### Prerequisite

- The `torch` package is required to run this sample. Follow the [PyTorch installation instructions](https://pytorch.org/get-started/locally/) to install it (if not already installed). Since PyTorch will run on a separate process, no specific version is required (it doesn't have to match Isaac Sim's PyTorch version).
- Enable the `isaacsim.ros2.bridge` Extension in the Extension Manager window by navigating to **Window > Extensions**.
- This tutorial requires the `h1_fullbody_controller` ROS 2 package, which is provided in the [IsaacSim-ros_workspaces repo](https://github.com/NVIDIA-Omniverse/IsaacSim-ros_workspaces/tree/main/ros2_workspace). Complete [ROS 2 Installation](https://docs.omniverse.nvidia.com/isaacsim/latest/installation/install_ros.html) to make sure the ROS 2 workspace environment is setup correctly.
- This tutorial requires the completion of [Tutorial 13: Rigging a Legged Robot for Locomotion Policy](https://docs.omniverse.nvidia.com/isaacsim/latest/tutorials/rigging_legged_robot.html) to setup the robot joint configurations based on the locomotion policy parameter, see the section below.

> **Hint**
> - If you encounter error: `externally-managed-environment` when installing PyTorch, try installing it in a virtual Python environment.
> - If you encounter `ModuleNotFoundError: No module named 'yaml'`, install PyYaml using pip.

---

### About the H1 Flat Terrain Locomotion Policy

The policy is trained based on the `Isaac-Velocity-Flat-H1-v0` environment from Isaac Lab. This policy tracks a velocity command on a flat terrain for the H1 humanoid robot. The policy is capable of walking forward and turning left/right. The policy does **not** support moving backwards nor sideways.

---

### Set Up Robot Joint Configurations

Follow the steps in [Tutorial 13: Rigging a Legged Robot for Locomotion Policy](https://docs.omniverse.nvidia.com/isaacsim/latest/tutorials/rigging_legged_robot.html) to setup the robot joint configurations based on the locomotion policy parameter. This step is very important, because mismatching the joint configurations can result in unexpected robot behavior.

The H1 flat terrain policy environment definition file is in YAML format.

The angle units specified in the policy environment definition file are in **radians**. The Isaac Sim USD GUI interface expects the angles to be specified in **degrees**.

The rigged H1 robot is available in the content browser at `Isaac/Samples/Rigging/H1/h1_rigged.usd`.

---

### Add IMU Sensor

Use the IMU sensor to obtain the body frame linear acceleration, angular velocity, and orientation. The flat terrain policy requires the linear velocity, angular velocity, and gravity vector from the pelvis link. You need to add an IMU sensor to the pelvis link to compute these values.

You can create an IMU sensor by right clicking on the `/h1/pelvis` and select **Create > Isaac > Sensors > Imu Sensor**.

> **Warning**
> If you add the IMU to a different link, for example, the torso link, you must first transform the IMU data to the pelvis link frame before using it in the policy.

---

### Set up ROS 2 Node for the H1 Humanoid Robot

The ROS 2 node publishes the observations and receives the actions from Isaac Sim. As specified in the environment definition file, the observations requires the following information:

- Body frame linear velocity
- Body frame angular velocity
- Body frame gravity vector
- Command (linear and angular velocity)
- Relative joint position
- Relative joint velocity
- Previous Action

You can obtain the body frame linear velocity, angular velocity, and gravity vector from processing the IMU data. The command is the desired linear and angular velocity of the robot, which can be retrieved from a ROS 2 twist message. The relative joint position and velocity can be computed from the Isaac Sim joint state topic. The previous action is the action applied last iteration and can be tracked by the policy node.

The action is a joint state message, which is a dictionary of joint names and their desired positions.

In this section, we will setup OmniGraph nodes that publishes the observations and receives the actions from Isaac Sim on physics step.

#### Create an On Demand OmniGraph

1. Open the H1 Unitree robot model that you rigged in the [Tutorial 13: Rigging a Legged Robot for Locomotion Policy](https://docs.omniverse.nvidia.com/isaacsim/latest/tutorials/rigging_legged_robot.html) tutorial.
2. Create a scope to hold the ActionGraphs by right clicking on the stage and selecting **Create > Scope**, rename it "Graph".
3. Right click on the stage and select **Create > Visual Scripting > ActionGraph**.
4. Rename the ActionGraph to "ROS_Imu", drag and drop this ActionGraph into the "Graph" scope.
5. Left click on the ActionGraph node, scroll down in the property editor and set the `pipelineStage` to `pipelineStageOnDemand`.

This will ensure the ActionGraph node runs when the Isaac Sim physics steps.

#### Create Imu Publisher Node

This node publishes the IMU data to ROS 2, which contains the body frame linear acceleration, angular velocity, and orientation.

1. Right click on the actionGraph node and select **Open Graph**.
2. Copy the following nodes into the Action graph:
   - **On Physics Step**: This node is triggered when the Isaac Sim physics steps, and runs the entire graph.
   - **ROS2 Context**: This node creates a context for the ROS 2 node.
   - **ROS2 QoS Profile**: This node sets the QoS profile for the ROS 2 node.
   - **Isaac Read IMU Node**: This node reads the IMU data from Isaac Sim.
   - **Isaac Read Simulation Time**: This node reads the simulation time from Isaac Sim.
   - **ROS2 Publish IMU**: This node publishes the IMU data to ROS 2 using the Isaac Read IMU Node and Isaac Read Simulation Time nodes as source.
3. Connect the nodes as shown in the image below.
4. Set the Isaac Read IMU Node input `IMU Prim` to `/h1/pelvis/Imu_Sensor` to read the IMU sensor data.
5. Uncheck input `Read Gravity` of the Isaac Read IMU Node to avoid reading the gravity vector from the pelvis link. This is because we only want the linear and angular velocity from the pelvis link.
6. Check the `Reset on Stop` input of Read Simulation Time node to reset the simulation time when the simulation stops.

### Create Joint State Publisher and Subscriber Nodes

This node publishes the joint states to ROS 2, which contains the joint names, positions, and velocities, and subscribes to the joint state commands from Isaac Sim.

1. Create a new ActionGraph node and rename it to "ROS_Joint_States".
2. Set the `pipelineStage` to `pipelineStageOnDemand`.
3. Copy the following nodes into the Action graph:
   - **On Physics Step**: This node is triggered when the Isaac Sim physics steps, and runs the entire graph.
   - **ROS2 Context**: This node creates a context for the ROS 2 node.
   - **ROS2 QoS Profile**: This node sets the QoS profile for the ROS 2 node.
   - **ROS2 Subscribe Joint State**: This node subscribes to the joint states commands from the external policy node.
   - **ROS2 Publish Joint State**: This node publishes the current joint states to ROS 2 from Isaac Sim.
   - **Isaac Read Simulation Time**: This node reads the simulation time from Isaac Sim.
   - **Articulation Controller**: This node will execute the joint state commands from the Subscribe Joint States node.
4. Connect the nodes as shown in the image below.
5. Set the ROS2 Publish Joint State input `Target Prim` to `/h1`, and `Topic Name` to `/joint_states`.
6. Set the ROS2 Subscribe Joint State input `Topic Name` to `/joint_command`.
7. Set the Articulation Controller input `Target Prim` to `/h1`.
8. Check the `Reset on Stop` input of Read Simulation Time node to reset the simulation time when the simulation stops.

> **Note**
> The completed asset is available in the content browser at `Isaac Sim/Samples/ROS2/Robots/h1_ROS.usd`.

---

### Publish ROS Clock and Set Up Environment

Now that the asset is set up, create a simulation scenario to place the robot in, configure the physics settings, and ROS time publish.

#### Setup Simulation Scenario

1. Create a new file. In the Content Browser, go to `Isaac Sim/Environments/Simple_Warehouse` and drag the `warehouse.usd` asset into the stage.
2. Drag and drop the `h1_ROS.usd` asset that you made earlier into the stage. Set the Z transform to 1.0 so it is above the ground.
3. Create a Physics Scene by right clicking on the stage and selecting **Create > Physics > Physics Scene**.
4. Select the Physics Scene and set **Time Steps Per Second** to 200.
5. Because you only have one robot, use CPU physics for better performance:
   - Uncheck **Enable GPU Dynamics**
   - Set the **Broadphase Type** to MBP

#### Setup ROS 2 Clock Publisher

1. Create a new ActionGraph node and rename it to "ROS_Clock".
2. Set the `pipelineStage` to `pipelineStageOnDemand`.
3. Copy the following nodes into the Action graph:
   - **On Physics Step**: This node is triggered when the Isaac Sim physics steps, and runs the entire graph.
   - **ROS2 Context**: This node creates a context for the ROS 2 node.
   - **ROS2 QoS Profile**: This node sets the QoS profile for the ROS 2 node.
   - **ROS2 Publish Clock**: This node publishes the ROS 2 clock to ROS 2.
   - **Read Simulation Time**: This node reads the simulation time from Isaac Sim.
4. Connect the nodes as shown in the image below.
5. Check the `Reset on Stop` input of Read Simulation Time node to reset the simulation time when the simulation stops.

> **Note**
> The completed environment is available in the content browser at `Isaac Sim/Samples/ROS2/Scenario/h1_ros_locomotion_policy_tutorial.usd`.

---

### Run ROS 2 Policy

The asset is set up, you can run the ROS 2 policy. Build the ROS 2 workspace and source the `setup.bash` file.

Launch the `h1_fullbody_controller` ROS 2 package by running the following command in the environment with PyTorch installed:

```bash
ros2 launch h1_fullbody_controller h1_fullbody_controller.launch.py
```

> **Note**
> This ROS 2 package computes observations and actions using the ROS messages that you published above and the flat terrain locomotion policy. When no command velocities are received, the robot will stand still and maintain balance. Make sure to start the ROS 2 policy **before** starting the simulation, otherwise the robot will fall over.

1. Open the H1 scenario you created earlier and press **PLAY** to start the simulation.
2. In a separate terminal, source ROS and launch `teleop_twist_keyboard` or another desired package to publish Twist messages:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

You can now control the H1 humanoid robot using your keyboard. Try the controls and observe if the robot moves as expected.

| Action | Key |
|--------|-----|
| Forward | `i` |
| Forward + Turn Left | `u` |
| Forward + Turn Right | `o` |
| Turn Left | `j` |
| Turn Right | `l` |
| Stand Still | `k` |

> **Important**
> - Moving backwards is not supported in this version of the policy. Pressing `m`, `,`, `.` key will cause the robot to fall over.
> - Setting linear and angular velocity above 0.75 exceeds the velocity limits of the policy and will cause the robot to fall over.
> - The robot might drift over time when there's no command velocities. This is expected behavior.

---

### Summary

This tutorial covered:

- Creating and setting up a ROS 2 node to publish observations and receive actions from Isaac Sim for the H1 flat terrain locomotion policy.
- Setting up Isaac Sim environment to run a reinforcement learning policy.

---

## Instanceable Assets

Reinforcement learning often requires training in large simulation scenes with multiple clones of the same robots. As we add more and more robots into the simulation environment, the memory consumption also increases for each additional set of robot and mesh assets added. To reduce memory consumption, we can take advantage of USD's Scenegraph Instancing functionality to mark common meshes shared by different copies of the same robots as instanceable.

By doing so, each copy of the robot will reference a single copy of meshes, avoiding the need to create multiple copies of the same meshes in the scene, thus reducing memory usage in the overall simulation environment.

### Learning Objectives

In this tutorial, we will show how to create instanceable assets in Isaac Sim. We will:

- Explain requirements for making assets instanceable
- Use the URDF and MJCF importers to create instanceable assets
- Show utility methods to convert existing assets to instanceable assets

*10-15 Minute Tutorial*

### Getting Started

Please refer to [USD Documentation on Scenegraph Instancing](https://graphics.pixar.com/usd/release/glossary.html#usdglossary-instancing) for more details on instancing.

Please refer to [Tutorial: Import URDF](https://docs.omniverse.nvidia.com/isaacsim/latest/ros2_tutorials/tutorial_ros2_urdf_import.html) and [Tutorial: Import MJCF](https://docs.omniverse.nvidia.com/isaacsim/latest/tutorials/import_mjcf.html) for more details on importer functionalities.

### Hierarchy Requirement for Instanceable Assets

USD prohibits modifying properties of prims on descendants of instanced prims. Therefore, we generally only perform instancing on mesh prims for robot assets, since properties on meshes will not differ across different environments during simulation. However, the transforms of the meshes may be different during simulation when robots in each environment are being moved in varying ways. Thus, we have to define the topology of our robot hierarchy in a specific structure in the asset tree definition in order for the instanceable flag to take action.

To mark any mesh or primitive geometry prim in the asset as instanceable, the mesh prim requires a parent Xform prim to be present, which will be used to add a reference to a master USD file containing definition of the mesh prim.

For example, the following definition **cannot** be marked instanceable:

```
World
  |_ Robot
       |_ Collisions
               |_ Sphere
               |_ Box
```

Instead, it will have to be modified to:

```
World
  |_ Robot
       |_ Collisions
               |_ Sphere_Xform
               |      |_ Sphere
               |_ Box_Xform
                      |_ Box
```

Any references that exist on the original Sphere and Box prims would have to be moved to `Sphere_Xform` and `Box_Xform` prims.

### Using URDF and MJCF Importers

Isaac Sim provides two importers — URDF and MJCF — for converting robot assets to USD format to be used in Isaac Sim. Both importers support the option to import robot assets directly as instanceable assets. By selecting this option, imported assets will be split into two separate USD files that follow the above hierarchy definition. Any mesh data will be written to a USD stage to be referenced by the main USD stage, which contains the main robot definition.

To use the Instanceable option in the importers:

1. First check the **Create Instanceable Asset** option.
2. Then, specify a file path to indicate the location for saving the mesh data in the **Instanceable USD Path** textbox. This will default to `./instanceable_meshes.usd`, which will generate a file `instanceable_meshes.usd` that is saved to the current directory.

Once the asset is imported with these options enabled, you will see the robot definition in the stage — we will refer to this stage as the **master stage**. If we expand the robot hierarchy in the Stage, we will notice that the parent prims that have mesh descendants have been marked as Instanceable and they reference a prim in our Instanceable USD Path USD file. We are also no longer able to modify attributes of descendant meshes.

To add our instanced asset into a new stage, we will simply need to add our master USD file.

### Modifying Existing Assets

Due to limitations of the topology requirement for making assets instanceable, it is not as straightforward to convert existing non-instanceable assets to become instanceable. Here, we will try to provide a few small utility methods to help make the process simpler.

All utilities should be copied into and run from the Script Editor, which can be opened from **Window > Script Editor**.

#### Creating Parent Xforms

First, we need to make sure our existing asset follows the hierarchy constraint defined above, where all mesh prims have a parent XForm prim present that can be used to mark the prim as instanceable. To help with the process of creating new parent prims, we provide a utility method `create_parent_xforms()` below to automatically insert a new Xform prim as a parent of every mesh prim in the stage.

```python
import omni.usd
import omni.client

from pxr import UsdGeom, Sdf

def create_parent_xforms(asset_usd_path, source_prim_path, save_as_path=None):
    """ Adds a new UsdGeom.Xform prim for each Mesh/Geometry prim under source_prim_path.
        Moves material assignment to new parent prim if any exists on the Mesh/Geometry prim.

        Args:
            asset_usd_path (str): USD file path for asset
            source_prim_path (str): USD path of root prim
            save_as_path (str): USD file path for modified USD stage. Defaults to None, will save in same file.
    """
    omni.usd.get_context().open_stage(asset_usd_path)
    stage = omni.usd.get_context().get_stage()

    prims = [stage.GetPrimAtPath(source_prim_path)]
    edits = Sdf.BatchNamespaceEdit()
    while len(prims) > 0:
        prim = prims.pop(0)
        print(prim)
        if prim.GetTypeName() in ["Mesh", "Capsule", "Sphere", "Box"]:
            new_xform = UsdGeom.Xform.Define(stage, str(prim.GetPath()) + "_xform")
            print(prim, new_xform)
            edits.Add(Sdf.NamespaceEdit.Reparent(prim.GetPath(), new_xform.GetPath(), 0))
            continue

        children_prims = prim.GetChildren()
        prims = prims + children_prims

    stage.GetRootLayer().Apply(edits)

    if save_as_path is None:
        omni.usd.get_context().save_stage()
    else:
        omni.usd.get_context().save_as_stage(save_as_path)
```

This method can be run on an existing non-instanced USD file for an asset from the script editor, where:

- `asset_usd_path` is the file path to the current existing USD asset
- `source_prim_path` is the USD prim path to the root prim of the asset
- `save_as_path` is a different file path to save the modified asset to. This can be left unspecified to overwrite the existing file.

```python
create_parent_xforms(
    asset_usd_path=ASSET_USD_PATH,
    source_prim_path=SOURCE_PRIM_PATH,
    save_as_path=SAVE_AS_PATH
)
```

> **Note**
> Any USD Relationships on the referenced meshes will be removed. This is because those USD Relationships originally have targets set to prims in the original prim that may no longer be valid and hence cannot be accessed from the new stage. Common examples of USD Relationships that could exist on the meshes are visual materials, physics materials, and filtered collision pairs. Therefore, it is recommended to set these USD Relationships on the meshes' parent Xforms instead of the meshes themselves.

### Full Conversion Utility

The above method can also be run as part of an overall conversion process, which is defined in the utility below. This utility will first insert new parent prims if `create_xforms=True` is specified, and generate a new USD file that is used for referencing. It will then traverse through the asset tree and mark the parent prim of any mesh or primitive type prims as instanceable, along with inserting a reference to the mesh USD stage.

```python
def convert_asset_instanceable(asset_usd_path, source_prim_path, save_as_path=None, create_xforms=True):
    """ Makes all mesh/geometry prims instanceable.
        Can optionally add UsdGeom.Xform prim as parent for all mesh/geometry prims.
        Makes a copy of the asset USD file, which will be used for referencing.
        Updates asset file to convert all parent prims of mesh/geometry prims to reference cloned USD file.

        Args:
            asset_usd_path (str): USD file path for asset
            source_prim_path (str): USD path of root prim
            save_as_path (str): USD file path for modified USD stage. Defaults to None, will save in same file.
            create_xforms (bool): Whether to add new UsdGeom.Xform prims to mesh/geometry prims.
    """

    if create_xforms:
        create_parent_xforms(asset_usd_path, source_prim_path, save_as_path)
        asset_usd_path = save_as_path

    instance_usd_path = ".".join(asset_usd_path.split(".")[:-1]) + "_meshes.usd"
    omni.client.copy(asset_usd_path, instance_usd_path)
    omni.usd.get_context().open_stage(asset_usd_path)
    stage = omni.usd.get_context().get_stage()

    prims = [stage.GetPrimAtPath(source_prim_path)]
    while len(prims) > 0:
        prim = prims.pop(0)
        if prim:
            if prim.GetTypeName() in ["Mesh", "Capsule", "Sphere", "Box"]:
                parent_prim = prim.GetParent()
                if parent_prim and not parent_prim.IsInstance():
                    parent_prim.GetReferences().AddReference(
                        assetPath=instance_usd_path, primPath=str(parent_prim.GetPath())
                    )
                    parent_prim.SetInstanceable(True)
                    continue

            children_prims = prim.GetChildren()
            prims = prims + children_prims

    if save_as_path is None:
        omni.usd.get_context().save_stage()
    else:
        omni.usd.get_context().save_as_stage(save_as_path)
```

## Summary

This tutorial covered the following topics:

- Requirements for creating instanceable assets
- Using the URDF and MJCF Importers to create instanceable assets
- Making existing assets instanceable


---

## ROS 2

ROS (Robot Operating System) is a set of software libraries and tools for building robotics applications. Isaac Sim is connected to ROS through the ROS 2 bridge extension. We recommend ROS 2 Humble and Jazzy with NVIDIA Isaac Sim.

The following tutorials detail the process of extracting and manipulating synthetic data generated by NVIDIA Isaac Sim and publishing them to your ROS applications.

### ROS 2 Installation

- Install Summary Steps
- Install ROS 2
- Configuring Options and Enabling Internal ROS Libraries
- Enabling the ROS 2 Bridge
- Setting Up Workspaces
- Enabling rclpy, Custom ROS 2 Packages, and Workspaces with Python 3.11
- Included ROS 2 Packages
- Running ROS in Docker Containers

## NVIDIA Isaac ROS

NVIDIA Isaac ROS — a collection of NVIDIA-accelerated, high performance, low latency ROS 2 packages for autonomous robots leveraging Jetson and other NVIDIA platforms.

## ROS 2 Reference Architecture

Overview of the ROS 2 workflow with Isaac Sim and the associated building blocks for integrating Isaac Sim into existing robot software stacks.

## Frequently Used Scenarios

- [ROS 2 Navigation](#ros-2-navigation)
- [ROS2 Joint Control: Extension Python Scripting](#ros2-joint-control-extension-python-scripting)
- [MoveIt 2](#moveit-2)
- [Running a Reinforcement Learning Policy through ROS 2 and Isaac Sim](#running-a-reinforcement-learning-policy-through-ros-2-and-isaac-sim)
- [Simulation Control](#simulation-control)
- [ROS2 Simulation Control](#ros2-simulation-control)

## URDF Import and Export

- [URDF Importer Extension](#urdf-importer-extension)
- [USD to URDF Exporter Extension](#usd-to-urdf-exporter-extension)

## ROS 2 Troubleshooting

Common ROS 2 issues and their solutions are documented in the ROS 2 Troubleshooting page. For general simulation troubleshooting, refer to Troubleshooting.

> **Notes**
> ROS 1 support is deprecated and will be removed in a future release.

---

## ROS 2 Tutorials (Linux and Windows)

### Getting Started with Importing and Controlling

- URDF Import: Turtlebot
- Driving TurtleBot using ROS 2 Messages

### Timing

- ROS 2 Clock
- ROS 2 Publish Real Time Factor (RTF)

### Sensors and Control

- ROS 2 Cameras
- Add Noise to Camera
- Publishing Camera's Data
- RTX Lidar Sensors
- ROS2 Transform Trees and Odometry
- ROS2 Setting Publish Rates
- ROS 2 Quality of Service (QoS)
- ROS2 Joint Control: Extension Python Scripting
- NameOverride Attribute
- ROS 2 Ackermann Controller
- Automatic ROS 2 Namespace Generation
- Running a Reinforcement Learning Policy through ROS 2 and Isaac Sim

### Standalone Workflow

- ROS 2 Bridge in Standalone Workflow

### Connecting with ROS 2 Stacks

- ROS 2 Navigation
- Multiple Robot ROS2 Navigation
- ROS 2 Navigation with Block World Generator
- MoveIt 2

### Additional ROS 2 OmniGraph Nodes

- ROS 2 Generic Publisher and Subscriber
- ROS 2 Generic Server and Client
- ROS 2 Service for Manipulating Prims Attributes

### Customization

- ROS 2 Python Custom Messages
- ROS 2 Python Custom OmniGraph Node
- ROS 2 Custom C++ OmniGraph Node

### Deploying

- ROS 2 Launch

### Simulation Control

- ROS2 Simulation Control

### Troubleshooting

- ROS 2 Troubleshooting

---

# URDF Import: Turtlebot

NVIDIA Isaac Sim has several tools to facilitate integration with ROS systems. There is the ROS2 bridge, a method to import URDF, and much more. This tutorial series gives examples of how to use these tools.

---

## Learning Objectives

In this example, you setup up a Turtlebot3 in Isaac Sim and enable it to drive around.

> If you already have a robot with rigged joints and properties in USD format, and you want to jump straight into using our ROS 2 bridge, go to the next tutorial in the series *Driving TurtleBot using ROS 2 Messages*.

---

## Getting Started

### Prerequisite

- Completed **ROS 2 Installation** so that ROS 2 is available, the ROS 2 extension is enabled, and necessary environment variables are set.
- Basic understanding of ROS workspaces.
- Install `xacro` using the following command:

  ```bash
  sudo apt install ros-$ROS_DISTRO-xacro
  ```

---

## Importing TurtleBot URDF

1. In a ROS-source terminal, clone the Turtlebot3's description package if you haven't done so already.

   ```bash
   git clone -b $ROS_DISTRO https://github.com/ROBOTIS-GIT/turtlebot3.git turtlebot3
   ```

2. Locate the URDF file for Turtlebot3 Burger in `turtlebot3/turtlebot3_description/urdf/turtlebot3_burger.urdf` and navigate to that directory.

   ```bash
   cd turtlebot3/turtlebot3_description/urdf
   ```

3. In the same terminal, pre-process the URDF file to manually remove the namespace arguments values and save to the `tb3_burger_processed.urdf` file:

   ```bash
   namespace=""
   xacro ./turtlebot3_burger.urdf "namespace:=${namespace:+$namespace/}" > tb3_burger_processed.urdf
   ```

4. For the purpose of this tutorial series, use an Isaac environment. Later you can import the robot into any environment of your choosing. Open the environment by going to the **Isaac Sim Content browser** and click `Isaac Sim/Environments/Simple_Room/simple_room.usd`.

   > If you do not want to use the provided environment, make sure there is a **GroundPlane** and a **PhysicsScene** to your environment. Both can be found in `Create > Physics`. You might also need some lighting — play with the various types of lighting in `Create > Light` to get the desired effect.

5. On a new stage, drag the `simple_room.usd` onto the stage, and place it at the origin by zeroing out all the **Translate** components in the **Transform** Property. You may need to zoom in a bit to observe the table inside the room.

6. Click **File > Import**, then locate the URDF file and select it.

7. In the prompt window, select **Referenced Model**. Inside the **Links** section, set to **Moveable Base**. Because this is a mobile robot, change targets of `wheel_left_joint` and `wheel_right_joint` to **Velocity** under the **Joints & Drives** section so that wheels can be properly driven later.

8. Verify that the configuration of the robot matches the expected settings.

9. Click **Import**.

   > After the asset is imported into Isaac Sim, a copy of the `.usd` version of the asset will be automatically saved. You can specify the folder where you want to save the asset in **USD Output**, if it's different than the folder that the `.urdf` file is located in. A folder name matching the `.urdf` file will be created in the specified directory, and the `.usd` file will be inside the newly created folder.

10. When the Turtlebot is first imported, it will be on the table. Place it just above the floor of the room using the gizmo.

11. Press **Play** and validate that you observe the Turtlebot fall onto the floor.

---

## Tune the Robot

Importing the URDF automatically imports material, physical, and joint properties whenever it is available and has matching categories in NVIDIA Isaac Sim. However, in cases where there are no available or matching categories, or if the units are different between the two systems, what gets automatically filled in might not be accurate and changes the robot's behavior. Here are some properties that can be tuned to correct the robot's behavior.

### Frictional Properties

If your robot's wheels are slipping, try changing the friction coefficients of the wheels and potentially the ground as well following steps in **Tutorial 2: Assemble a Simple Robot**.

### Physical Properties

If no explicit mass or inertial properties are given, the physics engine will estimate them from the geometry mesh. To update the mass and inertial properties:

- Find the prim that contains the rigid body for the given link. You can verify this by finding `Physics > Rigid Body` under its property tab.
- If it already has a **Mass** category under its **Physics** property tab, modify them accordingly.
- If there isn't already a **Mass** category, you can add it by clicking on the **+Add** button on top of the **Property** tab, and select `Physics > Mass`.

### Joint Properties

If your robot is oscillating at the joint or moving too slow, take a look at the **stiffness** and **damping** parameters for the joints.

- **High stiffness** makes the joints snap faster and harder to the desired target.
- **Higher damping** smooths but also slows down the joint's movement to target.
- For **pure position drives**: set relatively high stiffness and low damping.
- For **velocity drives**: stiffness must be set to zero with a non-zero damping.

For this Turtlebot robot, try setting the following:

| Parameter   | Value       |
|-------------|-------------|
| Damping     | 10000000.0  |
| Stiffness   | 0.0         |

> **Note:** When URDF importing finishes, the robot that appears on stage is usually loaded as a reference. This can be confirmed by an orange or blue arrow on the robot prim on the stage tree icon. If you have problem changing the parameters and saving them, you can edit the original USD file that the reference is pointing to instead. To find the file path to the original USD file, navigate to the **Property** tab and go to `References > Asset Path`.

---

## Summary

This tutorial covered the following topics:

- URDF import
- Tuning the robot parameters

---

# Driving TurtleBot using ROS 2 Messages

The ROS 2 bridge comes with a few popular rostopics that are packaged for ease of use. Here the focus is on the procedures for using them.

The steps to connect NVIDIA Isaac Sim to ROS can be done:

- using the **UI**
- **scripting** inside the extension workflow
- **scripting** inside the standalone Python workflow

> Refer to **Workflows** for details of different workflows. The UI method using existing Omnigraph nodes is demonstrated. Introductions to other methods are listed in the **Further Learning** section.

---

## Learning Objectives

In this example, you enable a Turtlebot3 to drive around and subscribe to a twist message through the ROS network. You learn to:

- Add controllers to Turtlebot3
- Introduce the ROS 2 bridge and ROS OmniGraph (OG) nodes
- Setup the robot to be driven by a ROS2 Twist message

---

## Getting Started

### Prerequisite

- Having a rigged Turtlebot, or completed **URDF Import: Turtlebot**.
- Completed **ROS 2 Installation**, so that the necessary environment variables are set and sourced before launching NVIDIA Isaac Sim and the ROS2 extension is enabled.

---

## Main Concepts

### Driving the Robot

At the end of **URDF Import: Turtlebot**, the robot has drivable joints, and when given a target position or velocity, it can move the joints to match the targets. Typically, you want to control the vehicle speed and not the individual wheel speed. Therefore, add the appropriate controllers. For Turtlebot3, a wheeled-robot with two wheels, the nodes needed are **Differential Controller** and **Articulation Controller**. The **Differential Controller** node converts vehicle speed to wheel speed, and the **Articulation Controller** node sends the commands to the joint drives.

> For more instructions on how to connect nodes, refer to **Isaac Sim Omnigraph Tutorial**.

### Connecting to ROS2

As part of our ROS2 bridge, there are nodes that are subscribers and publishers of specific messages, some utility nodes such as keeping track of simulation time and context ID. You will also find **"Helper Nodes"**, which are gateways to more complex OmniGraphs that we abstract away from users.

To establish a ROS2 bridge for a specific topic, the steps can be generalized to the following:

1. Open an action graph
2. Add the OG nodes relevant to the desired ROS 2 topics
3. Modify any properties as needed
4. Connect the data pipeline

The **ROS2 publisher nodes** are where NVIDIA Isaac Sim data gets packaged into ROS messages and sent out to the ROS network, and **subscriber nodes** are where ROS2 messages are received and allocated to the corresponding NVIDIA Isaac Sim parameters. So to use them, you must pipe in and out the necessary data, as directed by the properties of each node.

> If you need to publish or subscribe to messages beyond the ones that are provided, review **Custom Python Nodes**, or **Custom C++ Nodes** for ways to integrate custom OmniGraph nodes.

---

## Putting It Together

### Building the Graph

1. Open **Visual Scripting**: `Window > Graph Editors > Action Graph`. An Action Graph window will appear on the bottom; you can dock it wherever convenient.
2. Click on the **New Action Graph** icon in the middle of the Action Graph window.
3. Inside the Action Graph window, there is a panel on the left-hand side with all the OmniGraph Nodes (or OG nodes). All ROS2 related OG nodes are listed under **Isaac Ros2**. You can also search for nodes by name. To place a node into the graph, drag it from the node list into the graph window.
4. Build a graph that matches the structure described below.

#### Graph Explained

| Node | Description |
|------|-------------|
| **On Playback Tick Node** | Producing a tick when simulation is "Playing". Nodes that receive ticks from this node will execute their compute functions every simulation step. |
| **ROS2 Context Node** | ROS2 uses DDS for its middleware communication. DDS uses Domain ID to allow for different logical networks to operate independently even though they share a physical network. ROS 2 nodes on the same domain can freely discover and send messages to each other, while ROS 2 nodes on different domains cannot. The ROS2 context node creates a context with a given Domain ID. It is set to `0` by default. If **Use Domain ID Env Var** is checked, it will import the `ROS_DOMAIN_ID` from the environment in which you launched the current instance of Isaac Sim. |
| **ROS2 Subscribe Twist Node** | Subscribing to a Twist message. Specify the ROS 2 topic's name `/cmd_vel` in the `topicName` field in its **Property Tab**. The subscriber nodes often have an `Exec Out` field. This acts similar to a tick and will send a signal when a message is received by the subscriber. In this case, the differential controller must be ticked each frame regardless of when a new command arrives. Therefore, for this situation, the **Differential Node's Exec In** is ticked by the output of the **On Playback Tick** node rather than the subscriber node. |
| **Scale To/From Stage Unit Node** | Convert assets or inputs to stage unit. |
| **Break 3-Vector Node** | The output of the Twist subscriber node is linear and angular velocities, both 3-dimensional vectors. But the input of the differential controller node only takes a forward velocity and rotation velocity in the z-axis, therefore you must decompose the array and extract the corresponding elements before feeding them into the differential controller node. |
| **Differential Controller Node** | This node receives desired vehicle speed and calculates the wheel speed of the robot. It needs the wheel radius and distance between the wheels to make that calculation. It can also receive optional speed limit parameters to cap off wheel speed. Type in the property tab the wheel radius, the distance between the wheels, and the maximum linear speed for the vehicle as seen in the table below to match the Turtlebot. |
| **Articulation Controller Node** | This node is assigned to a target robot, then takes in the names or the indices of the joints that need to be moved, and moves them by the commands given in **Position Commands**, **Velocity Commands**, or **Effort Commands**. The Articulation Controller node is ticked by **On Playback Tick** so that if no new Twist message arrives, it will continue to execute whatever command it had received before. |

##### Differential Controller Parameters

| Field | Value |
|-------|-------|
| Max Angular Speed | 1.0 |
| Max Linear Speed | 0.22 |
| Wheel Distance | 0.16 |
| Wheel Radius | 0.025 |

##### Assigning the Articulation Controller Target

To assign the Articulation Controller node's target to be the Turtlebot:

1. In the property tab, click on **Add Target** and search for the Turtlebot prim in the popup box.
2. Make sure the robot prim you select is also where the **Articulation Root API** is applied. Sometimes it is the robot's parent prim, but often for mobile robots, it is the chassis prim instead.
3. If you imported the URDF following the previous tutorial, the Articulation Root API can be found on `/World/turtlebot3_burger/base_footprint`.
4. If the articulation root is set on the `base_footprint` prim, remove the articulation root property from `/World/turtlebot3_burger/base_footprint` and add the articulation root property on the main robot prim of `/World/turtlebot3_burger`.

##### Joint Name Arrays

To put the names of the wheel joints in an array format, type in the names of the wheel joints inside each of the **Constant Token** nodes, and feed the array of the names into the **Make Array Node**. The names of the joints for the Turtlebot are `wheel_left_joint` and `wheel_right_joint`.

> **Important:** Do not put the names in **Constant String** node, because OmniGraph does not have a string-array data type. If strings are needed in an array format to be used by a node, it must be **token** type.

---

## Verifying ROS Connections

1. Press **Play** to start ticking the graph and the physics simulation.
2. In a separate ROS-sourced terminal, check that the associated ROS 2 topics exist with `ros2 topic list`. Verify that `/cmd_vel` is listed along with `/rosout` and `/parameter_events`.
3. Now a twist message can be published to the `/cmd_vel` topic to control the robot.

   Drive it forward with the command:

   ```bash
   ros2 topic pub /cmd_vel geometry_msgs/Twist "{'linear': {'x': 0.2, 'y': 0.0, 'z': 0.0}, 'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}}"
   ```

   To stop the robot from moving, publish a zero velocity command:

   ```bash
   ros2 topic pub /cmd_vel geometry_msgs/Twist "{'linear': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}}"
   ```

4. To make it easier to move the Turtlebot around, install the `teleop_twist_keyboard`:

   ```bash
   sudo apt-get install ros-$ROS_DISTRO-teleop-twist-keyboard
   ```

5. Enable driving using the keyboard by running:

   ```bash
   ros2 run teleop_twist_keyboard teleop_twist_keyboard
   ```

---

## Troubleshooting

Make sure your robot is on the ground. The table has a different property therefore making it hard for the robot to move on it. To change properties of either the ground or the wheels, go to **Tutorial 3: Articulate a Basic Robot**.

---

## Summary

This tutorial covered the following topics:

- Drive the robot using the **Differential Controller** and the **Articulation Controller**
- Introduction to **ROS 2 Bridge OmniGraph nodes**
- Subscribing to a **ROS2 Twist message**

---

# ROS 2 Clock

## Learning Objectives

In this example, we will:

- Have a brief discussion on the ROS 2 Clock publisher and subscriber
- Publish simulation time to ROS 2 as a Clock message
- Subscribe to a ROS 2 Clock message
- Add a Clock Action Graph using the menu shortcut

---

## Getting Started

### Prerequisite

- Complete **ROS 2 Installation**.
- If using multiple systems, set the `FASTRTPS_DEFAULT_PROFILES_FILE` environment variable as per instructions in **ROS 2 Installation** before launching Isaac Sim, as well as any terminal where ROS messages will be sent or received, and **ROS 2 Extension** is enabled.

> **Note:** In Windows 10 or 11, depending on your machine's configuration, RViz2 might not open properly.

---

## Simulation Time and Clock

For external ROS 2 nodes to synchronize with simulation time, a `/clock` topic is usually used. Many ROS 2 nodes such as RViz2 use the parameter `use_sim_time`, which if set to `True` will indicate to the node to begin subscribing to the `/clock` topic and synchronizing to the published simulation time.

You can either set this parameter in a ROS 2 launch file or set the parameter using the following command in a new ROS 2-sourced terminal:

```bash
ros2 param set /node_name use_sim_time true
```

> Make sure to replace `/node_name` with whatever node you are currently running. If setting using the terminal, the node must already be running first before setting the parameter.

---

## Running ROS 2 Clock Publisher

1. Go to **Window > Graph Editors > Action Graph** to create an Action graph.
2. Add the following OmniGraph nodes into the Action graph:

   | Node | Description |
   |------|-------------|
   | **On Playback Tick** | Execute other graph nodes every simulation frame. |
   | **ROS 2 Context** | Create a context using either the given Domain ID or the `ROS_DOMAIN_ID` environment variable. |
   | **Isaac Read Simulation Time** | Retrieve current simulation time. Note: By default the simulation time increases monotonically, meaning regardless of whether simulation is stopped and re-played, the time will continue incrementing. This is mainly to prevent issues that can arise with the time jumping back when simulation resets. You can set `resetOnStop` to `True` if you would like the clock to start from 0 every time simulation is reset. |
   | **ROS 2 Publish Clock** | Publish simulation time to the `/clock` topic. |

3. Start RViz in a new ROS 2-sourced terminal:

   ```bash
   ros2 run rviz2 rviz2
   ```

4. Take note of the **ROS Time** and **ROS Elapsed** times listed in the bottom of the RViz window. These are currently displaying the wall time and, typically, match the **Wall Time** and **Wall Elapsed** fields.

5. In a new ROS 2-sourced terminal, set the `use_sim_time` parameter to `true` for the RViz node. Ensure that simulation is **stopped** in Isaac Sim.

   ```bash
   ros2 param set /rviz use_sim_time true
   ```

6. Notice in RViz that **ROS Time** and **ROS Elapsed** are now both `0`.

7. In Isaac Sim, click **Play**.

8. In RViz, the **ROS Time** is now identical to the simulation time published from Isaac Sim over the `/clock` topic.

---

## Publishing System Time

While publishing the simulation time is the most common workflow, there can be certain workflows that require certain messages to contain system time. To publish system time over the clock topic, follow these steps:

1. Go to **Window > Graph Editors > Action Graph** to create an Action graph.
2. Add the following OmniGraph nodes into the Action graph:

   | Node | Description |
   |------|-------------|
   | **On Playback Tick** | Execute other graph nodes every simulation frame. |
   | **ROS2 Context** | Create a context using either the given Domain ID or the `ROS_DOMAIN_ID` environment variable. |
   | **Isaac Read System Time** | Retrieve current system time. |
   | **ROS2 Publish Clock** | Publish simulation time to the `/clock` topic. |

3. In Isaac Sim, click **Play**. To observe the system timestamp published from Isaac Sim over the `/clock` topic, run the following command in a ROS-sourced terminal:

   ```bash
   ros2 topic echo /clock
   ```

### Camera Helper and RTX Lidar nodes

In upcoming tutorials you will observe the **ROS 2 Camera Helper** node and the **ROS2 RTX Lidar Helper** node. As both of these nodes automatically generate a sensor publishing pipeline, to use system timestamps for their publishers, ensure that their `useSystemTime` input field is set to `True`.

---

## Running ROS 2 Clock Subscriber

1. Open a new stage. Go to **Window > Graph Editors > Action Graph** to create an Action graph.
2. Add the following OmniGraph nodes into the Action graph:

   | Node | Description |
   |------|-------------|
   | **On Playback Tick** | Execute other graph nodes every simulation frame. |
   | **ROS2 Context** | Create a context using either the given Domain ID or the `ROS_DOMAIN_ID` environment variable. |
   | **ROS2 Subscribe Clock** | Subscribe to external timestamp data. |

3. Start simulation by clicking **Play**. Select the **ROS2 Subscribe Clock** node inside the action graph to view its `timeStamp` output in the **Property** window. Verify that the timestamp is `0`.
4. In a new ROS2-sourced terminal, run the following command to manually publish a clock message once:

   ```bash
   ros2 topic pub -t 1 /clock rosgraph_msgs/Clock "clock: { sec: 1, nanosec: 200000000 }"
   ```

5. Verify that the `timeStamp` value in the **ROS2 Subscribe Clock** OmniGraph node changes to `1.2`.
6. Change the previous command with different `sec` and `nanosec` values to observe those values being reflected in the `timeStamp` field of the **ROS2 Subscribe Clock** OmniGraph node.

---

## Graph Shortcut

We provide a menu shortcut to build a clock graph within just a few clicks. Go to **Tools > Robotics > ROS 2 OmniGraphs > Clock**.

> If you don't observe any ROS2 graphs listed, you need to enable the ROS2 bridge.

A popup box will appear asking for the parameters needed to populate the graphs. Provide the graph path and click **OK**. Verify that a graph publishing the simulated clock appears on the stage.

---

## Summary

This tutorial covered:

- Explanation for using the `/clock` topic and the `use_sim_time` ROS parameter for time synchronization.
- Creating and using **ROS2 Clock Publisher** and **Subscriber** nodes.

---

# ROS 2 Publish Real Time Factor (RTF)

## Learning Objectives

This tutorial will demonstrate publishing the **Real Time Factor (RTF)** of Isaac Sim as a ROS2 `Float32` message.

---

## Getting Started

Enable the `isaacsim.ros2.bridge` Extension in the **Extension Manager** window by navigating to `Window > Extensions`.

---

## Publish RTF

The **RTF** indicates how fast or slow simulation is running with respect to real-time. It is calculated per frame as:

```
RTF = simulated_elapsed_time / real_elapsed_time
```

- If **RTF > 1.0**: the simulation time is running faster than wall clock time.
- If **RTF < 1.0**: the simulation is running slower than real-time.

1. Go to **Tools > Robotics > ROS 2 OmniGraphs > Generic Publisher**. The parameter pop-up window will appear.
2. Select **Publish RTF as Float32** and click **OK**.
3. A new Action Graph will be created with the **Isaac Real Time Factor** node connected to a generic **ROS2 Publisher** node, which is set up to publish `std_msgs/msg/Float32` ROS messages.
4. Select the Action Graph prim found at `/Graph/ROS_GenericPub`. Right-click on it and choose **Open Graph**. The autogenerated graph should contain the RTF publisher.
5. Click **Play** to start simulation.
6. In a ROS2-sourced terminal, run the following command to view the RTF value published from Isaac Sim:

   ```bash
   ros2 topic echo /topic
   ```

For an unloaded system, RTF should be close to **1.0**.

---

## Summary

This tutorial covered using an OmniGraph shortcut to automatically generate a ROS2 RTF publisher graph.

---

# ROS 2 Cameras

## Learning Objectives

In this example, you learn how to:

- Add additional cameras to the scene and onto the robot
- Add camera publishers in Omnigraph
- Add camera publishers using the menu shortcut
- Send ground truth synthetic perception data through rostopics

---

## Getting Started

### Prerequisite

- Completed **ROS 2 Installation**: installed ROS 2, enabled the ROS 2 extension, built the provided Isaac Sim ROS 2 workspace, and set up the necessary environment variables.
- Basic understanding of ROS topics and how publisher and subscriber works.
- Completed tutorial on **Isaac Sim Omnigraph Tutorial** and **Tutorial 4: Add Camera and Sensors to a Robot**.
- Completed **URDF Import: Turtlebot** so that there is a Turtlebot ready on stage.

> **Note:** In Windows 10 or 11, depending on your machine's configuration, RViz2 might not open properly.

---

## Camera Publisher

### Setting Up Cameras

The default camera displayed in the Viewport is the **Perspective** camera. You can verify that by the **Camera** button on the top left-hand corner inside the Viewport display. Click on the **Camera** button and you will observe that there are a few other preset camera positions:

- Top
- Front
- Right side views

For this tutorial, you will add two stationary cameras, naming them `Camera_1` and `Camera_2`, viewing the room from two different perspectives. The procedures for adding cameras to the stage can be found in **Tutorial 4: Add Camera and Sensors to a Robot**.

Open additional Viewports to observe multiple camera views at the same time:

1. `Window > Viewports > Viewport 2` to open the viewport
2. Select the desired camera view from the **Cameras** button on the upper left corner in the viewport.

### Building the Graph for an RGB Publisher

1. Open the Graph Editors: `Window > Graph Editors > Action Graph`.
2. Click on the **New Action Graph** icon in the middle of the Action Graph window, or **Edit Action Graph** if you want to append the camera publisher to an existing action graph.
3. Build an Action Graph with the nodes and connections as described below.

#### Parameters

| Node | Input Field | Value |
|------|-------------|-------|
| **Isaac Create Render Product** | cameraPrim | `/World/Camera_1` |
| | enabled | `True` |
| **ROS 2 Camera Helper** | type | `rgb` |
| | topicName | `rgb` |
| | frameId | `turtle` |

Ticking this graph will automatically create a new render product assigned to `Camera_1`.

### Graph Explained

| Node | Description |
|------|-------------|
| **On Playback Tick Node** | Producing a tick when simulation is "Playing". Nodes that receive ticks from this node will execute their compute functions every simulation step. |
| **ROS 2 Context Node** | ROS2 uses DDS for its middleware communication. DDS uses Domain ID to allow for different logical networks to operate independently even though they share a physical network. ROS2 nodes on the same domain can freely discover and send messages to each other, while ROS2 nodes on different domains cannot. The ROS2 context node creates a context with a given Domain ID. It is set to `0` by default. If **Use Domain ID Env Var** is checked, it will import the `ROS_DOMAIN_ID` from the environment. |
| **Isaac Create Render Product** | Creating a render product prim, which acquires the rendered data from the given camera prim and outputs the path to the render product prim. Rendering can be enabled and disabled on command by checking or unchecking the `enabled` field. |
| **Isaac Run One Simulation Frame** | This node will make sure the pipeline is only ran once on start. |
| **ROS 2 Camera Helper** | Indicating the type of data to publish, and the rostopic to publish it on. |

### Camera Helper Node

The **Camera Helper Node** is abstracting a complex postprocessing network from the users.

After you press **Play** with a Camera Helper Node connected, when you click the icon on the upper left corner of the Action Graph window, you might observe that in the list of Action Graphs, a new one appears: `/Render/PostProcessing/SDGPipeline`.

> This graph is automatically created by the Camera Helper Node. The pipeline retrieves relevant data from the renderer, processes it, and sends them to the corresponding ROS publisher. This graph is only created in the session you are running. It will not be saved as part of your asset and will not appear in the Stage tree.

### Depth and Other Perception Ground Truth Data

In addition to RGB images, the following synthetic sensor and perceptual information are also available for any camera:

- Depth
- Point Cloud

> To observe the units used for each synthetic data annotator, refer to `omni.replicator`.

Before publishing the following bounding box and labels, review the **Isaac Sim Replicator Tutorials** to learn about semantically annotating scenes.

> **Note:** If you would like to use the BoundingBox publisher nodes, which are dependent on `vision_msgs`, ensure it is installed on the system or try **Configuring Options and Enabling Internal ROS Libraries**.

- BoundingBox 2D Tight
- BoundingBox 2D Loose
- BoundingBox 3D
- Semantic labels
- Instance Labels

Each **Camera Helper** node can only retrieve **one** type of data. You can indicate what type you want to assign to the node in the dropdown menu for the field `type` in the Camera Helper Node's **Property** tab.

> **Note:** After you specify a type for a Camera Helper node and activate it (i.e., started simulation and the underlying SDGPipeline has been generated), you **cannot** change the type and reuse the node. You can use a new node or reload your stage and regenerate the SDGPipeline with the modified type.

An example of publishing multiple Rostopics for multiple cameras can be found by going to the **Isaac Sim Content Browser**: `Isaac Sim > Samples > ROS2 > Scenario > turtlebot_tutorial.usd`.

### Camera Info Helper Node

The **Camera Info Helper** publisher node uses the following equations to calculate the **K**, **P**, and **R** camera intrinsic matrices.

| Matrix | Description |
|--------|-------------|
| **K Matrix** (Intrinsic Parameters) | The K matrix is a 3x3 matrix. |
| **P Matrix** (Projection Matrix) | For stereo cameras, the stereo offset of the second camera with respect to the first camera in x and y are denoted as Tx and Ty. These values are computed automatically if two render products are attached to the node. For monocular cameras, offset values are 0. The P matrix is a 3x4 row-major matrix. |
| **R Matrix** (Rectification Matrix) | The R matrix is a rotation matrix applied to align the camera coordinate system with the ideal stereo image plane, ensuring that epipolar lines in both stereo images become parallel. The R matrix is only used for stereo cameras and is set as a 3x3 matrix. |

---

## Graph Shortcut

There is a menu shortcut to build multiple camera sensor graphs. Go to **Tools > Robotics > ROS 2 OmniGraphs > Camera**.

> If you don't observe any ROS 2 graphs listed, you need to enable the ROS 2 bridge.

A popup box will appear asking for the parameters needed to populate the graphs. You must provide:

- **Graph Path**
- **Camera Prim**
- **frameId**
- Any **Node Namespaces** if you have one
- Check the boxes for the data you want to publish

If you want to add the graphs to an existing graph, check the **Add to an existing graph?** box. This will append the nodes to the existing graph, and use the existing tick node, context node, and simulation time node if they exist.

---

## Verifying ROS Connection

- Use `ros2 topic echo /<topic>` to observe the raw information being passed along.
- Visualize depth using `rqt_image_view`:

  ```bash
  ros2 run rqt_image_view rqt_image_view /depth
  ```

- To verify the images in RViz2:

  1. In a ROS 2-sourced terminal, run `rviz2` to open RViz.
  2. Add an **Image** display type and set the topic to `rgb`.

---

## Troubleshooting

If your depth image only shows black and white sections, it is likely that the field of view has "infinite" depth and has skewed the contrast. Adjust your field of view so that the depth range in the image is limited.

---

## Additional Publishing Options

To publish images **on demand** or **periodically at a specified rate**, you will need to use Python scripting. Go to **ROS 2 Camera** for examples.

---

## Summary

This tutorial introduces how to publish camera and perception data in ROS 2.

---

# Add Noise to Camera

## Learning Objectives

In this example, we will:

- Have a brief introduction regarding adding an augmentation to sensor images
- Publish image data with noise added

---

## Getting Started

### Prerequisites

- Completed the **ROS 2 Cameras** tutorial.
- ROS 2 bridge is enabled.
- Familiarity with `omni.replicator` concepts.
- Set the environment variables needed to enable ROS2 messaging in standalone workflow by completing the steps in **Using Terminal**.

---

## Running the Example

1. In one terminal, source your ROS 2 workspace.
2. In another terminal with your ROS 2 environment sourced, run the sample script:

   ```bash
   ./python.sh standalone_examples/api/isaacsim.ros2.bridge/camera_noise.py
   ```

3. After the scene finishes loading, verify that you observe the viewport scanning a warehouse scene counterclockwise.
4. In a new terminal with your ROS environment sourced, open an empty RViz window:

   ```bash
   rviz2
   ```

5. Add an **Image** window by clicking on **"Add"** on the bottom left. In the pop-up window, under the **"By display type"** tab, select **"Image"** and click **"OK"**.
6. A new image window will appear. Dock it somewhere convenient.
7. Expand the **Image** in the Display menu and change the **"Image Topic"** to `/rgb_augmented`. Verify that a slightly noisy version of the image in Isaac Sim is now showing in the RViz image window.

---

## Code Explained

### Setting the Camera

The first step is to set the camera on the render product we want to use for capturing data. There are APIs to set the camera on the viewport, but there are also lower-level APIs that use the render product prim directly. Both achieve the same. Because we are already working with the render product path, we use `set_camera_prim_path` for illustrative purposes.

```python
# grab our render product and directly set the camera prim
render_product_path = get_active_viewport().get_render_product_path()
set_camera_prim_path(render_product_path, CAMERA_STAGE_PATH)
```

### Defining Augmentations

There are several methods for defining an augmentation within a sensor pipeline:

- C++ OmniGraph node
- Python OmniGraph node
- `omni.warp` kernel
- numpy kernel

The **numpy** and **omni.warp** kernel options are demonstrated below to define a basic noise function. For brevity there are no out-of-bounds checks for the color values.

#### GPU Noise Kernel (warp)

```python
@wp.kernel
def image_gaussian_noise_warp(
    data_in: wp.array3d(dtype=wp.uint8), data_out: wp.array3d(dtype=wp.uint8), seed: int, sigma: float = 0.5
):
    i, j = wp.tid()
    dim_i = data_out.shape[0]
    dim_j = data_out.shape[1]
    pixel_id = i * dim_i + j
    state_r = wp.rand_init(seed, pixel_id + (dim_i * dim_j * 0))
    state_g = wp.rand_init(seed, pixel_id + (dim_i * dim_j * 1))
    state_b = wp.rand_init(seed, pixel_id + (dim_i * dim_j * 2))

    data_out[i, j, 0] = wp.uint8(float(data_in[i, j, 0]) + (255.0 * sigma * wp.randn(state_r)))
    data_out[i, j, 1] = wp.uint8(float(data_in[i, j, 1]) + (255.0 * sigma * wp.randn(state_g)))
    data_out[i, j, 2] = wp.uint8(float(data_in[i, j, 2]) + (255.0 * sigma * wp.randn(state_b)))
```

#### CPU Noise Kernel (numpy)

```python
def image_gaussian_noise_np(data_in: np.ndarray, seed: int, sigma: float = 25.0):
    np.random.seed(seed)
    return data_in + sigma * np.random.randn(*data_in.shape)
```

### Registering the Augmentation

Either of the two functions can be used with `rep.Augmentation.from_function()` to define an augmentation.

```python
# register new augmented annotator that adds noise to rgba and then outputs to rgb
# the image_gaussian_noise_warp variable can be replaced with image_gaussian_noise_np to use the cpu version.
# Ensure to update device to "cpu" if using the cpu version.
rep.annotators.register(
    name="rgb_gaussian_noise",
    annotator=rep.annotators.augment_compose(
        source_annotator=rep.annotators.get("rgb", device="cuda"),
        augmentations=[
            rep.annotators.Augmentation.from_function(
                image_gaussian_noise_warp, sigma=0.1, seed=1234, data_out_shape=(-1, -1, 3)
            ),
        ],
    ),
)
```

> **Note:** `seed` is an optional predefined Replicator Augmentation argument that can be used with both Python and warp functions. If set to `None` or `< 0`, it will use Replicator's global seed together with the node identifier to produce a repeatable unique seed. When used with warp kernels, the seed is used to initialize a random number generator that produces a new integer seed value for each warp kernel call.

### Creating a Custom ROS2 Writer

Next, a new writer is created with the new `rgb_gaussian_noise` annotator and registered.

```python
# Create a new writer with the augmented image
rep.writers.register_node_writer(
    name=f"CustomROS2PublishImage",
    node_type_id="isaacsim.ros2.bridge.ROS2PublishImage",
    annotators=[
        "rgb_gaussian_noise",
        omni.syntheticdata.SyntheticData.NodeConnectionTemplate(
            "IsaacReadSimulationTime", attributes_mapping={"outputs:simulationTime": "inputs:timeStamp"}
        ),
    ],
    category="custom",
)

# Register writer for Replicator telemetry tracking
(
    rep.WriterRegistry._default_writers.append("CustomROS2PublishImage")
    if "CustomROS2PublishImage" not in rep.WriterRegistry._default_writers
    else None
)
```

### Attaching the Writer

The `CustomROS2PublishImage` writer, which uses our new augmented `rgb_gaussian_noise` annotator, is registered. We can attach the render product to our replicator writer after initializing. This will begin capturing and publishing data to ROS.

```python
# Create the new writer and attach to our render product
writer = rep.writers.get(f"CustomROS2PublishImage")
writer.initialize(topicName="rgb_augmented", frameId="sim_camera")
writer.attach([render_product_path])
```

---

## Summary

This tutorial covered the basics of adding an augmentation to the ROS sensor pipeline and adding noise to the RGB sensor output.

---

# Publishing Camera's Data

## Learning Objectives

In this tutorial, you learn how to programmatically set up publishers for Isaac Sim Cameras at an approximate frequency.

---

## Getting Started

### Prerequisite

- Completed the **ROS 2 Cameras** tutorial.
- Completed **ROS 2 Installation** so that the necessary environment variables are set and sourced before launching NVIDIA Isaac Sim.
- Read through the **Sensor Axes Representation (LiDAR, Cameras)**.
- Read through how to programmatically create a Camera sensor object in the scene.
- **ROS 2 Bridge** is enabled.

> **Note:** In Windows 10 or 11, depending on your machine's configuration, RViz2 might not open properly.

---

## Setup a Camera in a Scene

To begin this tutorial, set up an environment with an `isaacsim.sensors.camera` Camera object. Running the following code results in a basic warehouse environment loaded with a camera in the scene.

```python
import carb
from isaacsim import SimulationApp
import sys

BACKGROUND_STAGE_PATH = "/background"
BACKGROUND_USD_PATH = "/Isaac/Environments/Simple_Warehouse/warehouse_with_forklifts.usd"

CONFIG = {"renderer": "RayTracedLighting", "headless": False}

simulation_app = SimulationApp(CONFIG)
import omni
import numpy as np
from isaacsim.core.api import SimulationContext
from isaacsim.core.utils import stage, extensions, nucleus
import omni.graph.core as og
import omni.replicator.core as rep
import omni.syntheticdata._syntheticdata as sd

from isaacsim.core.utils.prims import set_targets
from isaacsim.sensors.camera import Camera
import isaacsim.core.utils.numpy.rotations as rot_utils
from isaacsim.core.utils.prims import is_prim_path_valid
from isaacsim.core.nodes.scripts.utils import set_target_prims

# Enable ROS 2 bridge extension
extensions.enable_extension("isaacsim.ros2.bridge")

simulation_app.update()

simulation_context = SimulationContext(stage_units_in_meters=1.0)

# Locate Isaac Sim assets folder to load environment and robot stages
assets_root_path = nucleus.get_assets_root_path()
if assets_root_path is None:
    carb.log_error("Could not find Isaac Sim assets folder")
    simulation_app.close()
    sys.exit()

# Loading the environment
stage.add_reference_to_stage(assets_root_path + BACKGROUND_USD_PATH, BACKGROUND_STAGE_PATH)


###### Camera helper functions for setting up publishers. ########

# Paste functions from the tutorial here
# def publish_camera_tf(camera: Camera): ...
# def publish_camera_info(camera: Camera, freq): ...
# def publish_pointcloud_from_depth(camera: Camera, freq): ...
# def publish_depth(camera: Camera, freq): ...
# def publish_rgb(camera: Camera, freq): ...

###################################################################

# Create a Camera prim
camera = Camera(
    prim_path="/World/floating_camera",
    position=np.array([-3.11, -1.87, 1.0]),
    frequency=20,
    resolution=(256, 256),
    orientation=rot_utils.euler_angles_to_quats(np.array([0, 0, 0]), degrees=True),
)
camera.initialize()

simulation_app.update()
camera.initialize()

############### Calling Camera publishing functions ###############

approx_freq = 30
#publish_camera_tf(camera)
#publish_camera_info(camera, approx_freq)
#publish_rgb(camera, approx_freq)
#publish_depth(camera, approx_freq)
#publish_pointcloud_from_depth(camera, approx_freq)

####################################################################

# Initialize physics
simulation_context.initialize_physics()
simulation_context.play()

while simulation_app.is_running():
    simulation_context.step(render=True)

simulation_context.stop()
simulation_app.close()
```

---

## Publish Camera Intrinsics to CameraInfo Topic

The following snippet will publish camera intrinsics associated with an `isaacsim.sensors.camera` Camera to a `sensor_msgs/CameraInfo` topic.

```python
def publish_camera_info(camera: Camera, freq):
    from isaacsim.ros2.bridge import read_camera_info
    render_product = camera._render_product_path
    step_size = int(60/freq)
    topic_name = camera.name+"_camera_info"
    queue_size = 1
    node_namespace = ""
    frame_id = camera.prim_path.split("/")[-1]

    writer = rep.writers.get("ROS2PublishCameraInfo")
    camera_info, _ = read_camera_info(render_product_path=render_product)
    writer.initialize(
        frameId=frame_id,
        nodeNamespace=node_namespace,
        queueSize=queue_size,
        topicName=topic_name,
        width=camera_info.width,
        height=camera_info.height,
        projectionType=camera_info.distortion_model,
        k=camera_info.k.reshape([1, 9]),
        r=camera_info.r.reshape([1, 9]),
        p=camera_info.p.reshape([1, 12]),
        physicalDistortionModel=camera_info.distortion_model,
        physicalDistortionCoefficients=camera_info.d,
    )
    writer.attach([render_product])

    gate_path = omni.syntheticdata.SyntheticData._get_node_path(
        "PostProcessDispatch" + "IsaacSimulationGate", render_product
    )

    # Set step input to control execution rate
    og.Controller.attribute(gate_path + ".inputs:step").set(step_size)
    return
```

---

## Publish Pointcloud from Depth Images

In the following snippet, a pointcloud is published to a `sensor_msgs/PointCloud2` message. This pointcloud is reconstructed from the depth image using the intrinsics of the camera.

```python
def publish_pointcloud_from_depth(camera: Camera, freq):
    render_product = camera._render_product_path
    step_size = int(60/freq)
    topic_name = camera.name+"_pointcloud"
    queue_size = 1
    node_namespace = ""
    frame_id = camera.prim_path.split("/")[-1]

    rv = omni.syntheticdata.SyntheticData.convert_sensor_type_to_rendervar(
        sd.SensorType.DistanceToImagePlane.name
    )

    writer = rep.writers.get(rv + "ROS2PublishPointCloud")
    writer.initialize(
        frameId=frame_id,
        nodeNamespace=node_namespace,
        queueSize=queue_size,
        topicName=topic_name
    )
    writer.attach([render_product])

    gate_path = omni.syntheticdata.SyntheticData._get_node_path(
        rv + "IsaacSimulationGate", render_product
    )
    og.Controller.attribute(gate_path + ".inputs:step").set(step_size)
    return
```

---

## Publish RGB Images

```python
def publish_rgb(camera: Camera, freq):
    render_product = camera._render_product_path
    step_size = int(60/freq)
    topic_name = camera.name+"_rgb"
    queue_size = 1
    node_namespace = ""
    frame_id = camera.prim_path.split("/")[-1]

    rv = omni.syntheticdata.SyntheticData.convert_sensor_type_to_rendervar(sd.SensorType.Rgb.name)
    writer = rep.writers.get(rv + "ROS2PublishImage")
    writer.initialize(
        frameId=frame_id,
        nodeNamespace=node_namespace,
        queueSize=queue_size,
        topicName=topic_name
    )
    writer.attach([render_product])

    gate_path = omni.syntheticdata.SyntheticData._get_node_path(
        rv + "IsaacSimulationGate", render_product
    )
    og.Controller.attribute(gate_path + ".inputs:step").set(step_size)
    return
```

---

## Publish Depth Images

```python
def publish_depth(camera: Camera, freq):
    render_product = camera._render_product_path
    step_size = int(60/freq)
    topic_name = camera.name+"_depth"
    queue_size = 1
    node_namespace = ""
    frame_id = camera.prim_path.split("/")[-1]

    rv = omni.syntheticdata.SyntheticData.convert_sensor_type_to_rendervar(
        sd.SensorType.DistanceToImagePlane.name
    )
    writer = rep.writers.get(rv + "ROS2PublishImage")
    writer.initialize(
        frameId=frame_id,
        nodeNamespace=node_namespace,
        queueSize=queue_size,
        topicName=topic_name
    )
    writer.attach([render_product])

    gate_path = omni.syntheticdata.SyntheticData._get_node_path(
        rv + "IsaacSimulationGate", render_product
    )
    og.Controller.attribute(gate_path + ".inputs:step").set(step_size)
    return
```

---

## Publish a TF Tree for the Camera Pose

The pointcloud, published using the above function, will publish the pointcloud in the **ROS camera axes convention** (-Y up, +Z forward). To make visualizing this pointcloud easy in ROS using RViz, the following snippet will publish a TF Tree to `/tf`, containing two frames.

### Frames Published

| Frame | Description |
|-------|-------------|
| `{camera_frame_id}` | Camera's pose in the **ROS camera convention** (-Y up, +Z forward). Pointclouds are published in this frame. |
| `{camera_frame_id}_world` | Camera's pose in the **World axes convention** (+Z up, +X forward). This reflects the true pose of the camera. |

### TF Tree Structure

```
world -> {camera_frame_id}           (dynamic transform)
{camera_frame_id} -> {camera_frame_id}_world   (static transform, rotation only)
```

The static transform can be represented by the quaternion `[0.5, -0.5, 0.5, 0.5]` in `[w, x, y, z]` convention.

Because the pointcloud is published in `{camera_frame_id}`, it is encouraged to set the `frame_id` of the pointcloud topic to `{camera_frame_id}`. The resulting visualization of the pointclouds can be viewed in the **world** frame in RViz.

```python
def publish_camera_tf(camera: Camera):
    camera_prim = camera.prim_path

    if not is_prim_path_valid(camera_prim):
        raise ValueError(f"Camera path '{camera_prim}' is invalid.")

    try:
        camera_frame_id = camera_prim.split("/")[-1]

        ros_camera_graph_path = "/CameraTFActionGraph"

        if not is_prim_path_valid(ros_camera_graph_path):
            (ros_camera_graph, _, _, _) = og.Controller.edit(
                {
                    "graph_path": ros_camera_graph_path,
                    "evaluator_name": "execution",
                    "pipeline_stage": og.GraphPipelineStage.GRAPH_PIPELINE_STAGE_SIMULATION,
                },
                {
                    og.Controller.Keys.CREATE_NODES: [
                        ("OnTick", "omni.graph.action.OnTick"),
                        ("IsaacClock", "isaacsim.core.nodes.IsaacReadSimulationTime"),
                        ("RosPublisher", "isaacsim.ros2.bridge.ROS2PublishClock"),
                    ],
                    og.Controller.Keys.CONNECT: [
                        ("OnTick.outputs:tick", "RosPublisher.inputs:execIn"),
                        ("IsaacClock.outputs:simulationTime", "RosPublisher.inputs:timeStamp"),
                    ]
                }
            )

        og.Controller.edit(
            ros_camera_graph_path,
            {
                og.Controller.Keys.CREATE_NODES: [
                    ("PublishTF_"+camera_frame_id, "isaacsim.ros2.bridge.ROS2PublishTransformTree"),
                    ("PublishRawTF_"+camera_frame_id+"_world", "isaacsim.ros2.bridge.ROS2PublishRawTransformTree"),
                ],
                og.Controller.Keys.SET_VALUES: [
                    ("PublishTF_"+camera_frame_id+".inputs:topicName", "/tf"),
                    ("PublishRawTF_"+camera_frame_id+"_world.inputs:topicName", "/tf"),
                    ("PublishRawTF_"+camera_frame_id+"_world.inputs:parentFrameId", camera_frame_id),
                    ("PublishRawTF_"+camera_frame_id+"_world.inputs:childFrameId", camera_frame_id+"_world"),
                    ("PublishRawTF_"+camera_frame_id+"_world.inputs:rotation", [0.5, -0.5, 0.5, 0.5]),
                ],
                og.Controller.Keys.CONNECT: [
                    (ros_camera_graph_path+"/OnTick.outputs:tick",
                        "PublishTF_"+camera_frame_id+".inputs:execIn"),
                    (ros_camera_graph_path+"/OnTick.outputs:tick",
                        "PublishRawTF_"+camera_frame_id+"_world.inputs:execIn"),
                    (ros_camera_graph_path+"/IsaacClock.outputs:simulationTime",
                        "PublishTF_"+camera_frame_id+".inputs:timeStamp"),
                    (ros_camera_graph_path+"/IsaacClock.outputs:simulationTime",
                        "PublishRawTF_"+camera_frame_id+"_world.inputs:timeStamp"),
                ],
            },
        )
    except Exception as e:
        print(e)

    set_target_prims(
        primPath=ros_camera_graph_path+"/PublishTF_"+camera_frame_id,
        inputName="inputs:targetPrims",
        targetPrimPaths=[camera_prim],
    )
    return
```

---

## Running the Example

1. Enable `isaacsim.ros2.bridge` extension and set up ROS 2 environment variables.
2. Save the script and run it using `python.sh` in the Isaac Sim folder.
3. In our example, `{camera_frame_id}` is the prim name of the camera, which is `floating_camera`.
4. Verify that you observe a floating camera with prim path `/World/floating_camera` in the scene.
5. In a terminal, run `ros2 topic list` and verify the following topics appear:

   ```
   /camera_camera_info
   /camera_depth
   /camera_pointcloud
   /camera_rgb
   /clock
   /parameter_events
   /rosout
   /tf
   ```

### Visualizing in RViz2

1. Open RViz2 and set the **Fixed Frame** field to `world`.
2. Enable viewing of `/camera_depth`, `/camera_rgb`, `/camera_pointcloud`, and `/tf` topics.
3. Verify that the depth and RGB images display correctly.
4. Verify that the camera frames published by the TF publisher show the two frames (`{camera_frame_id}` and `{camera_frame_id}_world`).

---

## Summary

This tutorial demonstrated how to programmatically set up ROS 2 publishers for Isaac Sim Cameras at an approximate frequency.

---

# RTX Lidar Sensors

Isaac Sim **RTX or Raytraced Lidar** supports both **Solid State** and **Rotating Lidar** configuration using a JSON config file. Each RTX Sensor must be attached to its own viewport to simulate properly.

> **Warning:** Docking windows in the isaac-sim UI when an RTX Lidars simulation is running will likely lead to a crash. Pause the simulation before re-docking the window.

---

## Learning Objectives

In this example, you:

- Briefly introduce how to use RTX Lidar sensors.
- Create an RTX Lidar sensor.
- Publish sensor data to ROS2 as **LaserScan** and **PointCloud2** messages.
- Use the menu shortcut to create RTX Lidar sensor publishers.
- Put it all together and visualize multiple sensors in RViz2.

---

## Getting Started

> **Important:** Make sure to source ROS 2 appropriately from the terminal before running Isaac Sim.

### Prerequisites

- Completed the **ROS 2 Cameras** tutorial.
- `FASTRTPS_DEFAULT_PROFILES_FILE` environmental variable is set prior to launching sim, and **ROS2 bridge** is enabled.
- OPTIONAL: Explore the inner workings of RTX Lidar sensors by learning **Overview** and how to get **RTX Sensor Annotators**.
- Completed the **URDF Import: Turtlebot** tutorial so that Turtlebot is loaded and moving around.

> **Note:** In Windows 10 or 11, depending on your machine's configuration, RViz2 might not open properly. Some bandwidth-heavy topics might not be available to visualize in RViz2 in WSL.

---

## Adding a RTX Lidar ROS 2 Bridge

### Adding a 2D Lidar Sensor

1. Go to **Create > Sensors > RTX Lidar > NVIDIA > Example Rotary 2D**.
2. To place the synthetic Lidar sensor at the same place as the robot's Lidar unit, drag the Lidar prim under `/World/turtlebot3_burger/base_scan`.
3. Zero out any displacement in the **Transform** fields inside the **Property** tab. The Lidar prim should now be overlapping with the scanning unit of the robot.

### Adding a 3D Lidar Sensor

1. Go to **Create > Sensors > RTX Lidar > NVIDIA > Example Rotary**.
2. Drag the Lidar prim under `/World/turtlebot3_burger/base_scan`.
3. Zero out any displacement in the **Transform** fields. The Lidar prim should now be overlapping with the scanning unit of the robot.

### Connecting the ROS2 Bridge with OmniGraph Nodes

Open the visual scripting editor: `Window > Graph Editors > Action Graph`. (Optionally: move the graph under `/World/turtlebot3_burger/base_scan` — the placement is important for **Automatic ROS 2 Namespace Generation**.)

Add the following nodes:

| Node | Description |
|------|-------------|
| **On Playback Tick** | Triggers all the other nodes after Play is pressed. |
| **ROS2 Context Node** | Creates a context with a given Domain ID (default `0`). If **Use Domain ID Env Var** is checked, it imports `ROS_DOMAIN_ID` from the environment. |
| **Isaac Run One Simulation Frame** | Runs the create render product pipeline once at the start to improve performance. |
| **Isaac Create Render Product** (1st) | For the `cameraPrim` input, select the **2D RTX Lidar** created earlier. |
| **Isaac Create Render Product** (2nd) | For the `cameraPrim` input, select the **3D RTX Lidar** created earlier. |
| **ROS2 RTX Lidar Helper** (1st) | Publishes the **laser scan** message. Set `type` to `laser_scan`, `topicName` to `scan`, `frameId` to `base_scan`. Input render product from the 2D Lidar's Create Render Product. |
| **ROS2 RTX Lidar Helper** (2nd) | Publishes the **point cloud** message. Set `type` to `point_cloud`, `topicName` to `point_cloud`, `frameId` to `base_scan`. Input render product from the 3D Lidar's Create Render Product. |

> **Note on LaserScan timing:** When `type` is set to `laser_scan`, the LaserScan message will only be published when the RTX Lidar generates a **full scan**. For a rotary Lidar this is a full 360-degree rotation; for a solid state Lidar this is the full azimuth. Depending on Lidar rotation rate and time step size, it can take multiple frames to complete the full rotary scan. PointCloud messages are published either every frame or after the full scan has been accumulated, based on the **Publish Full Scan** setting.

---

## Visualizing in RViz

1. Run RViz2 in a sourced terminal: `rviz2`
2. Update the **Fixed Frame** to `base_scan`.
3. Add **LaserScan** visualization and set topic to `/scan`.
4. Add **PointCloud2** visualization and set topic to `/point_cloud`.

---

## Graph Shortcut

There is a menu shortcut to build multiple Lidar sensor graphs. Go to **Tools > Robotics > ROS 2 OmniGraphs > RTX Lidar**.

> If you don't observe any ROS2 graphs listed, you need to enable the ROS2 bridge.

A popup will appear asking for the parameters needed to populate the graphs. You must provide:

- **Graph Path**
- **Lidar Prim**
- **frameId**
- Any **Node Namespaces** if you have one
- Check the boxes for the data you want to publish

If you want to add the graphs to an existing graph, check the **Add to an existing graph?** box.

---

## Running the Example

In a new terminal with your ROS2 environment sourced, run the following command to start RViz with the Lidar point cloud configuration:

```bash
rviz2 -d <ros2_ws>/src/isaac_tutorials/rviz2/rtx_lidar.rviz
```

Then run the sample script:

```bash
./python.sh standalone_examples/api/isaacsim.ros2.bridge/rtx_lidar.py
```

After the scene finishes loading, verify that you observe the point cloud for the rotating Lidar sensor being simulated.

---

### RTX Lidar Script Sample

While most of the sample code is fairly generic, there are a few specific pieces needed to create and simulate the sensor.

#### Create the 3D RTX Lidar Sensor

```python
_, sensor = omni.kit.commands.execute(
    "IsaacSensorCreateRtxLidar",
    path="/sensor",
    parent=None,
    config="Example_Rotary",
    translation=(0, 0, 1.0),
    orientation=Gf.Quatd(1.0, 0.0, 0.0, 0.0),
)
```

`Example_Rotary` defines the configuration for the 3D Lidar sensor. Two generic configuration files are provided in `exts/build/omni.sensors.nv.common/data/lidar/`: `Example_Rotary.json` and `Example_Solid_State.json`. To switch to solid state, replace `config="Example_Rotary"` with `config="Example_Solid_State"`.

Create a render product and attach this sensor:

```python
hydra_texture = rep.create.render_product(sensor.GetPath(), [1, 1], name="Isaac")
```

Create the post process pipeline that publishes to ROS:

```python
writer = rep.writers.get("RtxLidar" + "ROS2PublishPointCloud")
writer.initialize(topicName="point_cloud", frameId="base_scan")
writer.attach([hydra_texture])
```

#### Create the 2D RTX Lidar Sensor

```python
_, sensor_2D = omni.kit.commands.execute(
    "IsaacSensorCreateRtxLidar",
    path="/sensor_2D",
    parent=None,
    config="Example_Rotary_2D",
    translation=(0, 0, 1.0),
    orientation=Gf.Quatd(1.0, 0.0, 0.0, 0.0),
)
```

Create a render product and the post process pipeline that publishes LaserScan data to ROS:

```python
hydra_texture_2D = rep.create.render_product(sensor_2D.GetPath(), [1, 1], name="Isaac")

writer = rep.writers.get("RtxLidar" + "ROS2PublishLaserScan")
writer.initialize(topicName="scan", frameId="base_scan")
writer.attach([hydra_texture_2D])
```

> **Note:** You can specify an optional `attributes={...}` dictionary when calling `activate_node_template` to set node specific parameters.

---

## Multiple Sensors in RViz2

> **Note:** In Windows 10 or 11, depending on your machine's configuration, some bandwidth-heavy topics might not be available to visualize in RViz2 in WSL.

To display multiple sensors in RViz2, there are a few important aspects to ensure all messages are synced and timestamped correctly.

### Simulation Timestamp

Use **Isaac Read Simulation Time** as the node that feeds the timestamp into all publishing nodes' timestamps.

### ROS 2 Clock

To publish the simulation time to the ROS 2 clock topic, setup the graph as shown in the **Running ROS 2 Clock Publisher** tutorial.

### frameId and topicName Conventions

To visualize all sensors as well as the tf tree inside RViz, the `frameId` and `topicName` must follow certain conventions:

| Source | frameId | nodeNamespace | topicName | type |
|--------|---------|---------------|-----------|------|
| Camera RGB | `(device_name)_(data_type)` | `(device_name)/(data_type)` | `image_raw` | rgb |
| Camera Depth | `(device_name)_(data_type)` | `(device_name)/(data_type)` | `image_rect_raw` | depth |
| Lidar | `base_scan` | | `scan` | laser scan |
| Lidar | `base_scan` | | `point_cloud` | point_cloud |
| TF | | | `tf` | tf |

To observe the multi-sensor RViz configuration, find the USD asset in **Isaac Sim Content Browser**: `Isaac Sim > Samples > ROS2 > Scenario > turtlebot_tutorial.usd`.

Open with the configuration:

```bash
rviz2 -d <ros2_ws>/src/isaac_tutorials/rviz2/camera_lidar.rviz
```

> **Important:** Ensure that the `use_sim_time` ROS2 param is set to `true` after running the RViz2 node. This ensures synchronization with simulation data especially when RViz2 interpolates position of Lidar data points.
>
> ```bash
> ros2 param set /rviz use_sim_time true
> ```

---

## Summary

This tutorial covered creating and using the RTX Lidar Sensor with ROS2:

- Adding an RTX Lidar sensor.
- Adding RTX Lidar and PointCloud ROS2 nodes.
- Displaying multiple sensors in RViz2.

---

# ROS2 Transform Trees and Odometry

## Learning Objectives

In this example, you:

- Add a transform publisher to publish the camera positions as part of the transform tree.
- Publish relative poses of objects.
- Publish the odometry of a robot.
- Use the menu shortcut to create transform and Odometry publishers.
- View the transform tree in Isaac Sim.

---

## Getting Started

### Prerequisite

- Completed the **URDF Import: Turtlebot**, **ROS 2 Cameras**, and **RTX Lidar Sensors** tutorials.
- Completed **ROS 2 Installation** so that the necessary environment variables are set and sourced before launching NVIDIA Isaac Sim, and ROS2 extension is enabled.

---

## Transform Tree Publisher

Assuming you've already gone through the ROS 2 camera tutorial and have two cameras on stage already, let's add those cameras to a transform tree so that you can track the camera's position in the global frame.

### Transform Publisher

1. In a new or existing Action Graph window, add a **ROS 2 Publish Transform Tree** node, and connect it with **On Playback Tick** and **Isaac Read Simulation Time**.
2. In the Property tab for the **ROS 2 Publish Transform Tree** node, add both `Camera_1` and `Camera_2` to the `targetPrims` field.
3. Examine the transform tree in a ROS 2-enabled terminal:
   ```bash
   ros2 topic echo /tf
   ```
   Verify that both cameras are on the transform tree. Move the camera around inside the viewport and observe how the camera's pose changes.

---

### Articulation Transforms

To get the transforms of each linkage on an articulated robot, you can add the robot's articulation root to the `targetPrims` field in a **ROS2 Publish Transform Tree** node. All the linkages subsequent to the articulation root will be published automatically.

> **Important:** If you find that the generated transform tree for an articulated robot chose the wrong link as the root link, use the following steps to manually select the articulation root link:
>
> 1. Select the robot's root prim on the **Stage Tree**. In its **Raw USD Properties** tab, find the **Articulation Root** section. Delete it by clicking the **X** on the upper right corner inside the section.
> 2. Select the desired link on the **Stage Tree**. Inside its **Raw USD Properties** tab, click **+ADD** and add `Physics > Articulation Root`.
> 3. After you change the articulation root, save the file and reload.

---

### Publish Relative Transforms

By default, the transforms are in reference to the world frame. You can check that the `/base_link` transform of the Turtlebot is published relative to `/World`. If you want to get the transforms relative to something else, such as a camera, indicate that in the `parentPrim` field. Add `Camera_1` in the `parentPrim` field, stop and play the simulation between property changes, and you can observe that the `/base_link` transform is now relative to `Camera_1`.

---

## Setting Up Odometry

To setup odometry for a robot, publish the odometry ROS message and its corresponding transforms.

1. Ensure the articulation root for your imported Turtlebot3 robot is `/World/turtlebot3_burger`. Otherwise, remove the articulation root from `/World/turtlebot3_burger/base_footprint` and add it for `/World/turtlebot3_burger`. Follow the steps in **Articulation Transforms** section to change the articulation root.

2. (Optional) Add `/World/turtlebot3_burger` to the `targetPrims` field in any **ROS2 Publish Transform Tree** node, and observe that the transforms of all links of the robot, fixed or articulated, will be published on the `/tf` topic.

3. Compose an Action Graph with the following nodes:

   - **Isaac Compute Odometry Node**: Add the Turtlebot prim (e.g., `/World/turtlebot3_burger`) to its **Chassis Prim** input field. This node calculates the position of the robot relative to its start location. Its output will be fed into both a publisher for the `/odom` ROS 2 topic, and a TF publisher that publishes the transform from `/odom` frame to `/base_link` frame.

   - **ROS2 Publish Raw Transform Tree Node**:
     - `childFrameId`: `base_link`
     - `parentFrameId`: `odom`

   - **ROS2 Publish Odometry Node**:
     - `chassisFrameId`: `base_link`
     - `odomFrameId`: `odom`

     > **Note:** The ROS2 Publish Odometry node publishes **full 3D velocity information**. Both linear velocity and angular velocity are published with all three dimensions (x, y, and z), allowing for a more complete representation of the robot's motion state.

4. Add a **ROS2 Publish Transform Tree** node to also publish the relevant robot prims under `base_link`:

   - `parentPrim`: `/World/turtlebot3_burger/base_link`
   - `targetPrims`:
     - `/World/turtlebot3_burger/base_footprint`
     - `/World/turtlebot3_burger/base_scan`
     - `/World/turtlebot3_burger/caster_back_link`
     - `/World/turtlebot3_burger/base_link/imu_link`
     - `/World/turtlebot3_burger/wheel_left_link`
     - `/World/turtlebot3_burger/wheel_right_link`

   This publishes a transform tree of `odom -> base_link -> <other robot links>`.

5. (Ground truth localization) Add another **ROS2 Publish Raw Transform Tree** node:

   - `childFrameId`: `odom`
   - `parentFrameId`: `world`
   - Leave **Translation** and **Rotation** fields detached (defaults: `(0,0,0)` translation, `(1,0,0,0)` rotation quaternion).

6. Press **Play** and in a new ROS-sourced terminal run:

   ```bash
   ros2 run tf2_tools view_frames
   ```

   Open the generated PDF file to observe the transform tree. Verify it shows `world -> odom -> base_link -> <robot links>`.

---

### Final Transform Tree Structure

```
world -> odom -> base_link -> base_footprint
                           -> base_scan
                           -> caster_back_link
                           -> imu_link
                           -> wheel_left_link
                           -> wheel_right_link
```

---

## Graph Shortcuts

### TF Publisher

Go to **Tools > Robotics > ROS 2 OmniGraphs > TF Publisher**.

> If you don't observe any ROS2 graphs listed, you need to enable the ROS2 bridge.

A popup box will appear asking for parameters:

- **Graph Path** and **Node Namespaces** if you have one.
- **Target Prim** that contains the articulation root API (for full articulation chain) or individual prims.
- **Parent Prim** used as the reference frame for the transforms (defaults to `/World`).

If you already have a transform publisher and want to add more prims, check both **"Add to an existing graph"** and **"Add to an existing node"** boxes.

### Odometry Publisher

Go to **Tools > Robotics > ROS 2 OmniGraphs > Odometry Publisher**. Provide:

- **Graph Path** and **Node Namespaces** if you have one.
- The prim that contains the **Articulation Root API**, and the **chassis prim** whose origin is used to calculate odometry.

---

## Viewing the Transform Tree in Isaac Sim

Isaac Sim's transform viewer allows you to draw on the simulated scene itself in the viewport window and on the transform tree published (under `/tf` and `/tf_static` topics) by Isaac Sim and/or external ROS 2 nodes.

### Enabling the TF Viewer

1. Enable the transform viewer extension using the **Extension Manager** by searching for `isaacsim.ros2.tf_viewer`.
2. After the extension is enabled, go to **Window > TF Viewer** to open the transform viewer control window.

### Window Components

| Component | Description |
|-----------|-------------|
| **Root Frame** | Frame on which to compute the transformations. |
| **Show Frames** | Whether the frames (markers) are displayed. Configure marker color and size. |
| **Show Names** | Whether the frames' names are displayed. Configure text color and size. |
| **Show Axes** | Whether the frames' axes are displayed (RGB → XYZ). Configure axis length and thickness. |
| **Show Connections** | Whether to show connections between child and parent frames. Configure line color and thickness. |
| **Update Frequency** | Frame transformation update frequency (Hz). Higher frequency might reduce simulation performance. |
| **Reset** | Reset transformation tree (clear transformation buffers). Useful to clean `TF_OLD_DATA` warnings. |

> **Note:** Closing the transform viewer window stops the display and clears the viewport drawings.

To start visualization, choose the appropriate root frame (e.g., `World` or `world`) according to the published transform tree specification.

> **Troubleshooting:** If the visualization does not show even though there are publications under `/tf` and/or `/tf_static` topics:
>
> - Make sure the simulation is running before opening the **TF Viewer** window.
> - Close and reopen the **TF Viewer** window to update the transform subscriptions.
> - Press the **Reset** button on the **TF Viewer** window to reset the transformation tree.

---

## Summary

This tutorial covered:

- Transform publisher to publish sensors and full articulation trees.
- Raw transform publisher to publish individual transforms.
- Odometry publisher and transform publishers setup for Turtlebot.
- Show the transform viewer in the Isaac Sim's viewport.
- Full 3D velocity (x, y, z) publishing for both linear and angular velocity in the odometry message.

---

# ROS2 Setting Publish Rates

## Learning Objectives

In this example, you learn to:

- Set the simulation frame rate in Isaac Sim.
- Set different publish rates for various ROS2 publishers simultaneously.

---

## Getting Started

### Prerequisite

- Completed the **URDF Import: Turtlebot**, **ROS 2 Cameras**, **RTX Lidar Sensors**, and **ROS2 Transform Trees and Odometry** tutorials.
- Completed **ROS 2 Installation** so that the necessary environment variables are set and sourced before launching NVIDIA Isaac Sim, and ROS2 extension is enabled.

---

## Setting Publish Rates with OmniGraph

Action Graphs are ticked every simulation frame and therefore OmniGraph nodes are bound to the factors of the simulation rate. This tutorial explains how to configure publishing ROS2 nodes at these factors of simulation.

### Isaac Simulation Gate Node

This section demonstrates the **Isaac Simulation Gate** node, which can be used to tick OmniGraph every certain number of frames. An IMU publisher is set up with this OmniGraph node.

1. Open the turtlebot simple room scene: **Isaac Sim Content browser** > `Isaac Sim > Samples > ROS2 > Scenario > turtlebot_tutorial.usd`.
2. Select the prim at `/World/turtlebot3_burger/base_link/imu_link` and create an IMU sensor: `Create > Sensors > Imu Sensor`. Verify the IMU sensor is created under the `imu_link` prim.
3. Create a new Action Graph inside `/World/turtlebot3_burger/base_link/imu_link` prim and name it `ROS_IMU` (placement is important for **Automatic ROS 2 Namespace Generation**). Select the prim, then go to `Window > Graph Editors > Action Graph`.
4. Build the IMU graph including the **Isaac Simulation Gate** node.

#### Node Configuration

| Node | Property | Value |
|------|----------|-------|
| **Isaac Simulation Gate** | `step` | `2` (downstream nodes ticked every other frame) |
| **Isaac Read IMU Node** | `imuPrim` | `/World/turtlebot3_burger/base_link/imu_link/Imu_Sensor` |
| **ROS2 Publish Imu** | `frameId` | `imu_link` |

---

## Setting Publish Rates for Nodes Within SDG Pipeline

In the previous section, we added the **Isaac Simulation Gate Node** in an OmniGraph ROS2 publishing pipeline. For **Camera** and **RTX Lidar** sensors, this is configured automatically within the **SDG pipeline**.

To modify the publish rates for each individual publisher, the `frameSkipCount` parameter inside each **ROS2 Helper** node can be modified.

### Lidar Configuration

1. Open the Lidar Action Graph: `/World/turtlebot3_burger/base_scan/ROS_LidarRTX`.
2. Select the `Ros2RTXLidarHelper` node (`/World/turtlebot3_burger/base_scan/ROS_LidarRTX/LaserScanPublish`) and set `frameSkipCount` to `11`.

   > Skipping 11 frames = publishing every 12 frames.

3. Disable the PointCloud publisher: uncheck `enabled` on `/World/turtlebot3_burger/base_scan/ROS_LidarRTX/PointCloudPublish`.

### Camera Configuration

1. Open the camera Action Graph: `/World/ActionGraph_camera`.
2. Disable the second camera render product: uncheck `enabled` on `/World/ActionGraph_camera/isaac_create_render_product_01`.
3. Select the Camera Helper node for RGB (`/World/ActionGraph_camera/ros2_camera_helper`) and set `frameSkipCount` to `3`.

   > Skipping 3 frames = publishing every 4 frames.

4. Disable the depth image publisher: uncheck `enabled` on `/World/ActionGraph_camera/ros2_camera_helper_02`.
5. Select the Camera Info Helper node (`/World/ActionGraph_camera/ros2_camera_info_helper`) and set `frameSkipCount` to `5`.

   > Skipping 5 frames = publishing every 6 frames.

---

## Setting Simulation Frame Rates

You configured the ActionGraphs to tick certain nodes at various rates. Because all Action Graphs are capped to the maximum frame rate defined for simulation rate, you can modify this simulation frame rate using the **Python interface**.

Open the Script Editor: `Window > Script Editor`.

### Method 1: Changing the carb setting

Run this script **after** playing the scene. This method sets the simulation timeline run rate and affects time from the **OnPlayBackTick** node.

```python
import carb
physics_rate = 60  # fps
carb_settings = carb.settings.get_settings()
carb.settings.get_settings().set_bool("/app/runLoops/main/rateLimitEnabled", True)
carb.settings.get_settings().set_int("/app/runLoops/main/rateLimitFrequency", int(physics_rate))
carb.settings.get_settings().set_int("/persistent/simulation/minFrameRate", int(physics_rate))
```

### Method 2: Changing SetTimeCodesPerSecond and set_target_framerate

This method sets the physics run rate and affects time from the **IsaacReadSimulationTime** node.

> **Note:** The Time Codes Per Second can only be set once before a scene is played. Reload the scene first if you want to change this value.

```python
import omni
physics_rate = 60  # fps

timeline = omni.timeline.get_timeline_interface()
stage = omni.usd.get_context().get_stage()
timeline.stop()

stage.SetTimeCodesPerSecond(physics_rate)
timeline.set_target_framerate(physics_rate)

timeline.play()
```

Run the snippets in the script editor and notice the effect on the simulation rate. You can enable the FPS display: viewport show/hide menu (eye icon) > **Heads Up Display > FPS**.

> **Important:** Both methods set the **target** frame rate of simulation. The actual frame rate depends on your machine's performance.

---

## Checking ROS 2 Publish Rate

Press **Play** to start the simulation. Check the publish rate for each ROS topic:

```bash
ros2 topic hz /topic_name
```

The publish rates are estimated. On a high-performance machine the maximum FPS would be closer to the `physics_rate` that was set (default 60 Hz).

| Topic | Effective Rate | Calculation |
|-------|---------------|-------------|
| `/clock` | ~60 Hz | Same as sim FPS |
| `/imu` | ~30 Hz | sim_fps / 2 |
| `/scan` | ~5 Hz | sim_fps / 12 |
| `/camera_1/rgb/image_raw` | ~15 Hz | sim_fps / 4 |
| `/camera_1/rgb/camera_info` | ~10 Hz | sim_fps / 6 |

The complete scene can be found at: **Isaac Sim Content browser** > `Isaac Sim > Samples > ROS2 > Scenario > turtlebot_tutorial_multi_sensor_publish_rates.usd`.

> **Note:** If `/camera_1/rgb/image_raw` publishes slower than anticipated, the large image message size may cause bottlenecks in network traffic or DDS queue management. Try reducing the render product resolution dimensions on `/World/ActionGraph_camera/isaac_create_render_product`.

---

## Troubleshooting

If you observe much different publish rates from the target simulation frame rate, try the following:

- Run Isaac Sim with factory settings to clear any persistent simulation frame rate settings:
  ```bash
  ./isaac-sim.sh --reset-user
  ```

- Check your computer's CPU usage to identify bottlenecks. If Isaac Sim exhibits incredibly high usage, try running with **Fabric** enabled:
  ```bash
  ./isaac-sim.fabric.sh --reset-user
  ```

> **Important:** The Fabric command above is experimental and not all functionality of Isaac Sim is supported. You only need to use the `--reset-user` flag the first time running with Fabric.

---

## Summary

This tutorial covered:

- Two ways to set the simulation frame rate in Isaac Sim using the Python interface.
- Setting different publish rates for various ROS2 publishers in OmniGraph and within the SDG Pipeline.

---

# ROS 2 Quality of Service (QoS)

## Learning Objectives

In this tutorial, you:

- Set Quality of Service (QoS) for all ROS2 OmniGraph nodes.
- Create a preset generic ROS2 publisher Action Graph.
- Set a static ROS2 publisher by setting a QoS Profile.

---

## Getting Started

### Prerequisite

- Completed **ROS 2 Installation** so that the necessary environment variables are set and sourced before launching NVIDIA Isaac Sim, and ROS2 extension is enabled.
- Read about **Quality of Service** settings.

> **Note:** The ROS2 QoS Profile OmniGraph node has a known issue: it is unable to save custom profiles in USD unless you first set the `createProfile` input to **"Custom"** before modifying any other fields.

---

## Setting QoS Profile for ROS 2 OmniGraph Nodes

1. Open a new stage.
2. Go to **Tools > Robotics > ROS 2 OmniGraphs > Generic Publisher**. For **Generic Publisher Graph**, select **Publish String**. Click **OK**.
3. Expand the newly created Graph prim. Select `ROS_GenericPub`, right-click and choose **Open Graph**.
4. All ROS 2 OmniGraph nodes such as the **ROS2 Publisher** include a `qosProfile` string input, formatted as a **JSON string**.

   Example JSON for default QoS settings:

   ```json
   {
       "history": "keepLast",
       "depth": 10,
       "reliability": "reliable",
       "durability": "volatile",
       "deadline": 0.0,
       "lifespan": 0.0,
       "liveliness": "systemDefault",
       "leaseDuration": 0.0
   }
   ```

   > `depth` must be a positive integer; `deadline`, `lifespan`, and `leaseDuration` must be floats.

5. While you can directly set the `qosProfile` input of any ROS 2 OmniGraph node with a valid JSON string, you can also use the **ROS2 QoS Profile** node to automatically generate this string and connect its output to multiple ROS 2 publisher or subscriber nodes.

6. In the Action Graph window, add the **ROS2 QoS Profile** node and connect it appropriately. The `createProfile` input contains multiple preset QoS profiles. The other inputs are QoS policies, which can be individually set to create a custom QoS profile.

7. Set `createProfile` to **Sensor Data** and then click **Play** to start simulation.

   > **Note:** If the UI doesn't update with new values, try clicking outside of the node and then clicking on it again.

8. In a ROS2-sourced terminal, run the following command to retrieve the QoS settings for the topic:

   ```bash
   ros2 topic info /topic -v
   ```

   The output for QoS Profile should match the ones defined from Isaac Sim.

   > **Note:** By default Fast DDS does not store depth, so the depth policy may appear as `UNKNOWN`. Try running Isaac Sim and ROS2 nodes using **Cyclone DDS** to retrieve depth info.

---

## Creating Static Publishers

> This section assumes you have already completed the above section.

Static publishers can be useful when you publish a message exactly once but need the same message to be available regardless of how many subscribers connect to the topic.

1. Modify the Action Graph from earlier by adding the **On Stage Event** and **Countdown** OmniGraph nodes.
2. For the **On Stage Event** node, set `eventName` to `Simulation Start Play`.
3. For the **Countdown** node, set `duration` to `3` and `period` to `1`. This will tick the ROS2 Publisher node 3 times after simulation is played. The first 2 frames are used for setup and the 3rd frame publishes a message.
4. Select the **ROS2 QoS Profile** node and set `createProfile` to **Default for publisher/subscribers**.
5. Set `depth` policy to `1` and `durability` policy to `transientLocal`.
6. Hit **Play** to start simulation.
7. In a new ROS2-sourced terminal, run the command to view the static message:

   ```bash
   ros2 topic echo /topic
   ```

8. In another ROS2-sourced terminal, repeat step 7 and notice the static message appears again for this second subscriber.

---

## Summary

This tutorial covered:

- QoS Profile Node.
- Setting Quality of Service (QoS) for all ROS2 OmniGraph nodes.
- Setting a static ROS2 publisher using a custom QoS Profile.

---

# ROS2 Joint Control: Extension Python Scripting

## Learning Objectives

In this tutorial, you interact with a manipulator, the **Franka Emika Panda Robot**. You:

- Add a ROS2 Joint State publisher and subscriber in Omnigraph
- Add a ROS2 Joint State publisher and subscriber using menu shortcut
- Add a ROS2 Joint State publisher and subscriber using the OmniGraph Python API via the script editor
- Learn about the `isaac:nameOverride` prim attribute

---

## Getting Started

### Prerequisite

- Completed **Workflows** to understand the Extension Workflow.
- Appropriate `ros2_ws` is sourced in the terminal that will be running Python scripts.
- `FASTRTPS_DEFAULT_PROFILES_FILE` environmental variable is set prior to launching Isaac Sim and the ROS2 bridge is enabled.

---

## Add Joint States in UI

1. Open the asset: **Isaac Sim Content browser** > `Isaac Sim > Robots > FrankaRobotics > FrankaPanda > franka.usd`.
2. Go to **Window > Graph Editors > Action Graph** to create an Action graph.
3. Add the following OmniGraph nodes:

   | Node | Description |
   |------|-------------|
   | **On Playback Tick** | Execute other graph nodes every simulation frame. |
   | **Isaac Read Simulation Time** | Retrieve current simulation time. |
   | **ROS2 Publish Joint State** | Publish ROS2 Joint States to `/joint_states`. |
   | **ROS2 Subscribe Joint State** | Subscribe to ROS2 Joint States from `/joint_command`. |
   | **Articulation Controller** | Move the robot articulation according to commands from the subscriber. |

4. Select **ROS2 Publish Joint State** node and add the `/panda` robot articulation to `targetPrim`.
5. Select **Articulation Controller** node and add `/panda` to `targetPrim` or type `/panda` in the `robotPath` field.
6. Connect the nodes:
   - `OnPlaybackTick.outputs:tick` → `ROS2PublishJointState.inputs:execIn`
   - `OnPlaybackTick.outputs:tick` → `ROS2SubscribeJointState.inputs:execIn`
   - `OnPlaybackTick.outputs:tick` → `ArticulationController.inputs:execIn`
   - `IsaacReadSimulationTime.outputs:simulationTime` → `ROS2PublishJointState.inputs:timeStamp`
7. Press **Play** to start publishing joint states and subscribing commands.
8. In a ROS2-sourced terminal, test with the provided script:

   ```bash
   ros2 run isaac_tutorials ros2_publisher.py
   ```

9. Check the joint state topic:

   ```bash
   ros2 topic echo /joint_states
   ```

> **Note:** **Articulation Root** describes the beginning of an articulation tree. For fixed base robots like the Franka, the articulation root is specified at its root joint to world. For movable objects, it is specified at the rigid body with the deepest tree, typically the torso or `chassis_link`.

---

## Graph Shortcut

Go to **Tools > Robotics > ROS 2 OmniGraphs > JointStates**.

> If you don't observe any ROS2 graphs listed, you need to enable the ROS2 bridge.

A popup box will appear asking for:

- **Graph Path**
- **Node Namespace** if needed
- The prim that contains the **Articulation Root API**
- (For subscriber) Option to add the **Articulation Controller** node

---

## Add Joint States in Extension

The same action can be done using a Python script via the **Script Editor**.

1. Open the Franka asset: **Isaac Sim Content browser** > `Isaac Sim > Robots > FrankaRobotics > FrankaPanda > franka.usd`.
2. Open **Script Editor**: `Window > Script Editor`.
3. Paste the following code:

   ```python
   import omni.graph.core as og

   og.Controller.edit(
       {"graph_path": "/ActionGraph", "evaluator_name": "execution"},
       {
           og.Controller.Keys.CREATE_NODES: [
               ("OnPlaybackTick", "omni.graph.action.OnPlaybackTick"),
               ("PublishJointState", "isaacsim.ros2.bridge.ROS2PublishJointState"),
               ("SubscribeJointState", "isaacsim.ros2.bridge.ROS2SubscribeJointState"),
               ("ArticulationController", "isaacsim.core.nodes.IsaacArticulationController"),
               ("ReadSimTime", "isaacsim.core.nodes.IsaacReadSimulationTime"),
           ],
           og.Controller.Keys.CONNECT: [
               ("OnPlaybackTick.outputs:tick", "PublishJointState.inputs:execIn"),
               ("OnPlaybackTick.outputs:tick", "SubscribeJointState.inputs:execIn"),
               ("OnPlaybackTick.outputs:tick", "ArticulationController.inputs:execIn"),
               ("ReadSimTime.outputs:simulationTime", "PublishJointState.inputs:timeStamp"),
               ("SubscribeJointState.outputs:jointNames", "ArticulationController.inputs:jointNames"),
               ("SubscribeJointState.outputs:positionCommand", "ArticulationController.inputs:positionCommand"),
               ("SubscribeJointState.outputs:velocityCommand", "ArticulationController.inputs:velocityCommand"),
               ("SubscribeJointState.outputs:effortCommand", "ArticulationController.inputs:effortCommand"),
           ],
           og.Controller.Keys.SET_VALUES: [
               ("ArticulationController.inputs:robotPath", "/panda"),
               ("PublishJointState.inputs:targetPrim", "/panda")
           ],
       },
   )
   ```

4. Press **Run** in the Script Editor. The Action Graph with all required nodes is added.
5. Test with the ROS 2 Python node:

   ```bash
   ros2 run isaac_tutorials ros2_publisher.py
   ```

6. Verify joint states:

   ```bash
   ros2 topic echo /joint_states
   ```

> **Note:** This script must only be run once. It assumes no ActionGraph already exists on stage. Start a new stage to run it again.

---

## Position and Velocity Control Modes

The joint state subscriber supports **position** and **velocity** control. Each joint can only be controlled by a single mode at a time, but different joints on the same articulation tree can be controlled by different modes.

> Make sure each joint's stiffness and damping parameters are set appropriately: **position control** requires stiffness >> damping; **velocity control** requires stiffness = 0.

### Separate Messages per Mode

```python
import threading
import rclpy
from sensor_msgs.msg import JointState

rclpy.init()
node = rclpy.create_node('position_velocity_publisher')
pub = node.create_publisher(JointState, 'joint_command', 10)

thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
thread.start()

joint_state_position = JointState()
joint_state_velocity = JointState()

joint_state_position.name = ["joint1", "joint2", "joint3"]
joint_state_velocity.name = ["wheel_left_joint", "wheel_right_joint"]
joint_state_position.position = [0.2, 0.2, 0.2]
joint_state_velocity.velocity = [20.0, -20.0]

rate = node.create_rate(10)
try:
    while rclpy.ok():
        pub.publish(joint_state_position)
        pub.publish(joint_state_velocity)
        rate.sleep()
except KeyboardInterrupt:
    pass
rclpy.shutdown()
thread.join()
```

### Combined Single Message (using `nan` for unused modes)

```python
joint_state = JointState()
joint_state.name = ["joint1", "joint2", "joint3", "wheel_left_joint", "wheel_right_joint"]
joint_state.position = [0.2, 0.2, 0.2, float('nan'), float('nan')]
joint_state.velocity = [float('nan'), float('nan'), float('nan'), 20.0, -20.0]
```

---

## Summary

This tutorial covered adding a ROS2 Joint State publisher and subscriber using both the UI and Extension scripting.

---

# NameOverride Attribute

## Learning Objectives

In this tutorial, you learn more about the `isaac:nameOverride` prim attribute and how it can be used for publishing joint names and TF.

---

## Getting Started

### Prerequisite

- Completed **Workflows** to understand the Extension Workflow.
- Completed **ROS2 Joint Control: Extension Python Scripting** to understand how to setup Joint Publishers and Subscribers.
- Completed **ROS2 Transform Trees and Odometry** to understand how to setup TF Publishers.
- Appropriate `ros2_ws` is sourced in the terminal that will be running Python scripts.
- If running multiple machines, ensure `FASTRTPS_DEFAULT_PROFILES_FILE` environmental variable is set prior to launching sim, and ROS2 bridge is enabled.

---

## Setting up the NameOverride Attribute

When setting up the Joint State or TF publishers, the **prim name** is used to publish the ROS link name. In some cases the prim names might not match the convention expected by the ROS stack. In this case, the `isaac:nameOverride` prim attribute allows you to internally override any prim name when it is used to publish using ROS.

Before proceeding, setup the scene by following the **Add Joint States in Extension** section.

### Adding the isaac:nameOverride Prim Attribute

1. Click on any joint prim.
2. Look for the **Name Override** field in the **raw USD properties** in the property panel.
   - If this field is already present, skip the next step.
   - If not present, proceed to step 3.
3. In the property panel, click **Add**. In the popup menu, go to **Isaac > NameOverride**. This will apply this attribute to the prim.
4. In the property panel, add your custom prim name in the **Name Override** field.
5. Click **Play** and notice the joint names have updated with the custom names you added when you echo the `/joint_states` topic.

### ROS Publishers

The **ROS 2 Publish Transform Tree** and the **ROS 2 Publish Joint State** OmniGraph node will automatically publish the name provided by the `isaac:nameOverride` attribute if it is defined for a given prim.

### ROS Subscribers

For the **ROS 2 Joint State Subscriber** pipeline, you can drag in the **Isaac Joint Name Resolver** OmniGraph node and connect it within the pipeline.

For the **Isaac Joint Name Resolver** node, set the **Target Prim** or the **Robot Path** to `/panda`.

If you publish joint commands to Isaac Sim from an external ROS 2 node using your custom prim names, the **Isaac Joint Name Resolver** node will provide the actual prim paths to the **Articulation Controller**, which will then be able to manipulate the prims as commanded.

---

## Summary

This tutorial covered adding the `isaac:nameOverride` attribute to prims to enable custom names for each prim to be published and manipulated using ROS.

---

# ROS 2 Ackermann Controller

## Learning Objectives

In this example, you learn to drive a **Leatherback car** by subscribing to an `AckermannDriveStamped` message through the ROS network. You will learn to:

- Setup Articulation and Ackermann Controllers to a Leatherback
- Setup the robot to be driven by a ROS 2 `AckermannDriveStamped` message
- Control an Ackermann base robot with a Twist message

---

## Getting Started

### Prerequisite

- The `ackermann_msgs` ROS 2 package is required. To install:

  ```bash
  sudo apt install ros-$ROS_DISTRO-ackermann-msgs
  ```

- Enable the `isaacsim.ros2.bridge` Extension in the **Extension Manager**: `Window > Extensions`.
- This tutorial requires `isaac_tutorials` and `cmdvel_to_ackermann` ROS 2 packages, provided in the [IsaacSim-ros_workspaces](https://github.com/isaacsim/IsaacSim-ros_workspaces) repo. Complete **ROS 2 Installation** to ensure the workspace is set up correctly.

---

## Ackermann Controller and Drive Setup

1. In a new stage, create the **Flat Grid** environment: `Create > Environments > Flat Grid`.
2. Add the Leatherback robot: **Content Browser** > `Isaac Sim > ROBOTS > NVIDIA > Leatherback`.
3. Drag and drop the `leatherback.usd` asset onto the stage. Zero out all **Translate** components in the **Transform** Property.
4. Create a new action graph: `Window > Graph Editors > Action Graph`. Click **New Action Graph**.
5. Add the following nodes and connect them:

   | Node | Description |
   |------|-------------|
   | **On Playback Tick** | Execute other graph nodes every simulation frame. |
   | **ROS 2 Context Node** | Create a context using the given Domain ID or `ROS_DOMAIN_ID`. |
   | **Ackermann Controller** | Compute individual wheel steering angles and wheel speed. |
   | **ROS 2 Subscribe AckermannDrive** | Subscribe to Ackermann drive commands. Topics: `ackermann_cmd`. |
   | **ROS 2 QoS Profile** | Create a QoS profile. |
   | **Articulation Controller** | Manipulate the steering joints of the Leatherback. |
   | **Articulation Controller_01** | Manipulate the wheels of the Leatherback. |

6. **Articulation Controller** (steering) — Property tab:
   - `targetPrim`: `/Leatherback`
   - `jointNames`:
     - `Knuckle__Upright__Front_Left`
     - `Knuckle__Upright__Front_Right`

7. **Articulation Controller_01** (wheels) — Property tab:
   - `targetPrim`: `/Leatherback`
   - `jointNames`:
     - `Wheel__Upright__Rear_Left`
     - `Wheel__Upright__Rear_Right`
     - `Wheel__Knuckle__Front_Left`
     - `Wheel__Knuckle__Front_Right`

8. **ROS 2 Subscribe AckermannDrive** — Property tab: set `topicName` to `ackermann_cmd`.

9. **Ackermann Controller** — Property tab:

   | Input Field | Value |
   |-------------|-------|
   | `backWheelRadius` | 0.052 |
   | `frontWheelRadius` | 0.052 |
   | `maxWheelRotation` | 0.7854 |
   | `maxWheelVelocity` | 20.0 |
   | `trackWidth` | 0.24 |
   | `wheelBase` | 0.32 |
   | `maxAcceleration` | 1.0 |
   | `maxSteeringAngleVelocity` | 1.0 |

10. Hit **Play** to start simulation.
11. In a new terminal, source your Isaac Sim ROS workspace and run:

    ```bash
    ros2 run isaac_tutorials ros2_ackermann_publisher.py
    ```

12. Verify that the Leatherback car moves correctly.

> **Note:** Preconfigured Leatherback assets are available in the **Content Browser**:
> - `Isaac Sim > Sample > ROS2 > Robots > Leatherback_ROS` (with action graph)
> - `Isaac Sim > Sample > ROS2 > Scenario > leatherback_ackermann` (warehouse race track)

---

## Converting Twist Messages to AckermannDriveStamped Messages

To control the Leatherback robot using your keyboard by translating command velocity to Ackermann drive stamped messages:

1. Open the Leatherback warehouse race track scene: **Content Browser** > `Isaac Sim > Sample > ROS2 > Scenario > leatherback_ackermann`.
2. Press **PLAY** to start simulation.
3. Stop the previous publisher.
4. In a new terminal, source ROS and launch the conversion node:

   ```bash
   ros2 launch cmdvel_to_ackermann cmdvel_to_ackermann.launch.py acceleration:=0.5 steering_velocity:=0.5
   ```

   > Launch parameters:
   > - `publish_period_ms` (default: 20): publishing dt (ms)
   > - `track_width` (default: 0.2): wheel separation distance (m)
   > - `acceleration` (default: 0.0): acceleration (ms⁻²), 0 = instant speed change
   > - `steering_velocity` (default: 0.0): delta steering angle (rad/s), 0 = instant angle change

5. In a separate terminal, launch `teleop_twist_keyboard`:

   ```bash
   ros2 run teleop_twist_keyboard teleop_twist_keyboard
   ```

6. Keyboard controls:

   | Action | Key |
   |--------|-----|
   | Forward | `i` |
   | Backward | `,` |
   | Forward Left | `u` |
   | Forward Right | `o` |
   | Backward Left | `m` |
   | Backward Right | `.` |
   | Stop | `k` |

---

## Summary

This tutorial covered:

- Creating and setting up an **Ackermann Controller** node with articulation controller nodes.
- Adding a **ROS 2 AckermannDriveStamped** subscriber node, which feeds commands into the Ackermann Controller node.
- Translating the command velocity to AckermannDriveStamped message and controlling an Ackermann-based robot with keyboard.

---

# Automatic ROS 2 Namespace Generation

## Learning Objectives

In this tutorial we will:

- Learn how to configure your Isaac Sim assets to automatically generate ROS 2 namespaces for each ROS 2 OmniGraph node.

---

## Getting Started

### Prerequisite

- Completed **ROS 2 Installation** so that the necessary environment variables are set and sourced before launching NVIDIA Isaac Sim, and ROS 2 extension is enabled.
- Read about **ROS 2 Namespaces**.

---

## ROS 2 Namespaces

Managing namespaces in ROS 2 is crucial for multi-robot simulations to ensure that each robot's topics are uniquely identifiable.

There are currently two main ways within OmniGraph to set a namespace for ROS publishers, subscribers and services:

1. **Manually** set namespaces in the `nodeNamespace` field.
2. **(Recommended)** Configure assets to **automatically generate namespaces** for all Isaac Sim ROS OmniGraph nodes using the `isaac:namespace` prim attribute.

This tutorial focuses on the second approach.

---

## Configuring the Asset

### Setting Up the Base Asset

1. Open a new stage and open the **Script Editor** (`Window > Script Editor`).
2. Run the following snippet to create a set of XForms that mimic a robot articulation:

   ```python
   from pxr import UsdGeom
   import omni.usd

   stage = omni.usd.get_context().get_stage()

   if not stage:
       print("No stage is currently loaded.")
   else:
       mock_robot = UsdGeom.Xform.Define(stage, "/mock_robot")
       base_link = UsdGeom.Xform.Define(stage, "/mock_robot/base_link")
       lidar_link = UsdGeom.Xform.Define(stage, "/mock_robot/base_link/lidar_link")
       lidar_link.AddTranslateOp().Set(value=(0, 0, 0.4))
       camera_link = UsdGeom.Xform.Define(stage, "/mock_robot/base_link/camera_link")
       camera_link.AddTranslateOp().Set(value=(0, 0, 0.2))
       wheel_left = UsdGeom.Xform.Define(stage, "/mock_robot/base_link/wheel_left")
       wheel_left.AddTranslateOp().Set(value=(-0.2, 0, 0))
       wheel_right = UsdGeom.Xform.Define(stage, "/mock_robot/base_link/wheel_right")
       wheel_right.AddTranslateOp().Set(value=(0.2, 0, 0))
   ```

3. Add a 2D RTX Lidar sensor: `Create > Sensors > RTX Lidar > NVIDIA > Example Rotary 2D`. Drag it under `/mock_robot/base_link/lidar_link`.

4. Add a Hawk stereo camera: `Create > Sensors > Camera and Depth Sensors > LeopardImaging > Hawk`. Drag it under `/mock_robot/base_link/camera_link`.

5. Create a **Generic Publisher**: `Tools > Robotics > ROS 2 OmniGraphs > Generic Publisher`. Set **Publish String**, Graph Path to `/mock_robot/base_link/wheel_left/String_graph`.

6. Create a **TF Publisher**: `Tools > Robotics > ROS 2 OmniGraphs > TF Publisher`. Set Target Prim to `/mock_robot`, Graph Path to `/mock_robot/base_link/wheel_left/TF_graph`.

7. Create **Camera Publisher** (left): `Tools > Robotics > ROS 2 OmniGraphs > Camera`. Set Camera Prim to `/mock_robot/base_link/camera_link/Hawk/left/camera_left`, Graph Path to `/mock_robot/base_link/camera_link/Hawk/Camera_Left_Graph`. Uncheck **Depth**.

8. Create **Camera Publisher** (right): Same as above but Camera Prim to `/mock_robot/base_link/camera_link/Hawk/right/camera_right`, Graph Path to `/mock_robot/base_link/camera_link/Hawk/Camera_Right_Graph`. Uncheck **Depth**.

9. Create a **2D RTX Lidar Publisher**: `Tools > Robotics > ROS 2 OmniGraphs > RTX Lidar`. Set Lidar Prim to `/mock_robot/base_link/lidar_link/Example_Rotary_2D`, Graph Path to `/mock_robot/base_link/lidar_link/Lidar_Graph`. Enable only **Laser Scan**.

---

## Configuring Namespace Attributes

Now that the base asset is set up, an `isaac:namespace` attribute must be added for each prim where a namespace value is desired. The namespace will be generated by appending each `isaac:namespace` attribute value from the top of the prim hierarchy down to each ROS publisher.

The namespace generation behavior depends on the type of ROS publisher:

| Publisher Type | Namespace Behavior |
|----------------|-------------------|
| **ROS 2 TF OmniGraph Nodes** | Only includes the namespace value from the **top-level prim** with a namespace attribute set (e.g., `robot1/tf`). |
| **ROS 2 Camera & Lidar Helper Nodes** | The **render product path** of the Camera/Lidar sensor is used to identify the namespace path. The location of the sensor prim (not the helper node) is relevant. |
| **All other OmniGraph nodes** | The **path to the OmniGraph node** is used to identify the namespace path. The location of the OmniGraph node is relevant. |

### Adding the isaac:namespace Prim Attribute

1. Select the prim. In the property window, click **Add**.
2. In the popup menu, go to **Isaac > Namespace**.
3. In the property panel, enter your namespace value in the **Namespace** field.

---

## Testing the isaac:namespace Prim Attribute

### Single Robot

Apply `isaac:namespace` to the following prims (set each value to the prim name):

- `/mock_robot/base_link/lidar_link`
- `/mock_robot/base_link/camera_link`
- `/mock_robot/base_link/camera_link/Hawk`
- `/mock_robot/base_link/camera_link/Hawk/left`
- `/mock_robot/base_link/camera_link/Hawk/right`
- `/mock_robot/base_link/wheel_left`

Click **Play**. In a ROS-sourced terminal, run `ros2 topic list`. Verify you observe:

```
/camera_link/Hawk/left/camera_info
/camera_link/Hawk/left/rgb
/camera_link/Hawk/right/camera_info
/camera_link/Hawk/right/rgb
/lidar_link/laser_scan
/wheel_left/tf
/wheel_left/topic
```

### Multi-Robot (Duplication)

1. Stop simulation. Select `/mock_robot` prim and add `isaac:namespace` attribute. Set it to `mock_robot`.
2. Duplicate `/mock_robot` (right-click > **Duplicate**). For `/mock_robot_01`, change `isaac:namespace` to `mock_robot_01`.
3. Click **Play**.

Verify topics are now namespaced per robot:

**`mock_robot` topics:**
```
/mock_robot/camera_link/Hawk/left/camera_info
/mock_robot/camera_link/Hawk/left/rgb
/mock_robot/camera_link/Hawk/right/camera_info
/mock_robot/camera_link/Hawk/right/rgb
/mock_robot/lidar_link/laser_scan
/mock_robot/tf
/mock_robot/wheel_left/topic
```

**`mock_robot_01` topics:**
```
/mock_robot_01/camera_link/Hawk/left/camera_info
/mock_robot_01/camera_link/Hawk/left/rgb
/mock_robot_01/camera_link/Hawk/right/camera_info
/mock_robot_01/camera_link/Hawk/right/rgb
/mock_robot_01/lidar_link/laser_scan
/mock_robot_01/tf
/mock_robot_01/wheel_left/topic
```

> **Important:** Topics are generated automatically. If your namespace needs a custom naming scheme, you can manually fill in the `nodeNamespace` input field for each ROS OmniGraph node.

---

## Summary

This tutorial covered:

- Demonstrating how the `isaac:namespace` attribute can be set to prims on a robot to automatically generate namespaces for multi-robot simulations.

---

# ROS 2 Bridge in Standalone Workflow

## Learning Objectives

- Run standalone ROS2 Python examples
- Manually step ROS2 components

---

## Getting Started

### Prerequisite

- Completed **Workflows** and **Hello World** to understand the two workflows (Standalone and Extension).
- Set the environment variables needed to enable ROS2 messaging in standalone workflow by completing the steps in **Using Terminal**.

> **Note:** In Windows 10 or 11, depending on your machine's configuration, RViz2 might not open properly.

---

## Manually Stepping ROS2 Components

Standalone scripting is typically ideal for manual control of the simulation steps. An **OnImpulseEvent** OmniGraph node can be connected to any ROS2 OmniGraph node so that the frequency of the publishers and subscribers can be carefully controlled.

Example: creating an action graph with a **ROS2 Publish Clock** node precisely controlled with a ROS2 Domain ID of 1:

```python
import omni.graph.core as og

og.Controller.edit(
    {"graph_path": "/ActionGraph", "evaluator_name": "execution"},
    {
        og.Controller.Keys.CREATE_NODES: [
            ("ReadSimTime", "isaacsim.core.nodes.IsaacReadSimulationTime"),
            ("Context", "isaacsim.ros2.bridge.ROS2Context"),
            ("PublishClock", "isaacsim.ros2.bridge.ROS2PublishClock"),
            ("OnImpulseEvent", "omni.graph.action.OnImpulseEvent"),
        ],
        og.Controller.Keys.CONNECT: [
            ("OnImpulseEvent.outputs:execOut", "PublishClock.inputs:execIn"),
            ("ReadSimTime.outputs:simulationTime", "PublishClock.inputs:timeStamp"),
            ("Context.outputs:context", "PublishClock.inputs:context"),
        ],
        og.Controller.Keys.SET_VALUES: [
            ("PublishClock.inputs:topicName", "/clock"),
            ("Context.inputs:domain_id", 1),
            ("Context.inputs:useDomainIDEnvVar", False),
        ],
    },
)
```

On any frame, run the following to set an impulse event, which will tick the clock publisher once:

```python
og.Controller.set(og.Controller.attribute("/ActionGraph/OnImpulseEvent.state:enableImpulse"), True)
```

> **Note:** Due to the explicit control of rendering and physics simulation steps in standalone scripting, the time it takes to complete each step will depend on the computation load and will likely not match real time. Use the simulation clock as reference.

---

## Examples

### ROS 2 Clock

This sample demonstrates how to create an action graph with ROS 2 component nodes and tick them at different rates.

```bash
./python.sh standalone_examples/api/isaacsim.ros2.bridge/clock.py
```

Echo the topics to observe messages:

```bash
ros2 topic echo /sim_time
ros2 topic echo /manual_time
```

> For the UI-based approach, refer to the **ROS 2 Clock** tutorial.

---

### ROS 2 Camera

Two samples that create an action graph with ROS 2 **Camera Helper** and **Camera Info Helper** OmniGraph nodes to set up RGB, depth, and camera info publishers.

**Publishing schedule:**
- Every frame: Camera Info
- Every 5 frames: RGB image
- Every 60 frames: Depth image

#### Periodic Image Publishing

Execution rate is set via **Isaac Simulation Gate** OmniGraph nodes in the SDGPipeline graph.

```bash
./python.sh standalone_examples/api/isaacsim.ros2.bridge/camera_periodic.py
```

#### Manual Image Publishing

Uses **Branch** OmniGraph nodes as custom gates that can be enabled/disabled at any time.

```bash
./python.sh standalone_examples/api/isaacsim.ros2.bridge/camera_manual.py
```

#### Visualizing Results

```bash
rviz2 -d <ros2_ws>/src/isaac_tutorials/rviz2/camera_manual.rviz
```

> **Note:** Black frames might appear for depth image displays in RViz2. To verify, use `ros2 run rqt_image_view rqt_image_view` and set topic to `/depth`.

---

### Carter Stereo

Demonstrates taking an existing USD stage with an action graph containing ROS 2 component nodes and modifying default settings. The stereo camera pair is automatically enabled.

**Publishing schedule (every frame):**
- ROS 2 clock, PointCloud2 (RTX Lidar), Odometry, Twist subscriber, TF messages, Left/Right cameras
- Every 2 frames: Twist command message

```bash
./python.sh standalone_examples/api/isaacsim.ros2.bridge/carter_stereo.py
```

Visualize in RViz2:

```bash
rviz2 -d <ros2_ws>/src/isaac_tutorials/rviz2/carter_stereo.rviz
```

> **Note:** If images don't show up in RViz2, press **Stop** and **Play** in the simulator.

---

### Multiple Robot ROS 2 Navigation

Demonstrates running an existing USD stage with multiple robots. Can be run with hospital or office environments.

**Hospital Environment:**
```bash
./python.sh standalone_examples/api/isaacsim.ros2.bridge/carter_multiple_robot_navigation.py --environment hospital
```

**Office Environment:**
```bash
./python.sh standalone_examples/api/isaacsim.ros2.bridge/carter_multiple_robot_navigation.py --environment office
```

**Per frame:**
- ROS 2 clock, PointCloud2 (RTX Lidars), Odometry, Twist subscriber, TF messages

---

### MoveIt2

Demonstrates adding multiple USD stages and manually creating/ticking an action graph with ROS 2 component nodes.

**Per frame:**
- ROS 2 clock, Joint State messages (published), Joint State subscriber, TF messages

```bash
./python.sh standalone_examples/api/isaacsim.ros2.bridge/moveit.py
```

---

### Receiving ROS 2 Messages

A basic subscriber example where upon receiving an empty ROS2 message, a cube in the scene teleports to a random location.

```bash
./python.sh standalone_examples/api/isaacsim.ros2.bridge/subscriber.py
```

From another terminal, publish the empty message (1 Hz):

```bash
ros2 topic pub -r 1 /move_cube std_msgs/msg/Empty
```

---

## Summary

In this tutorial you learned how to manually step ROS 2 components and run standalone ROS 2 Python examples.

---

# ROS 2 Navigation

> **Support Limitations:** ROS 2 Navigation with Isaac Sim is fully supported on **Linux**. On **Windows**, ROS 2 Navigation with Isaac Sim is **partially supported** and could potentially produce errors.

## Learning Objectives

This ROS2 sample demonstrates NVIDIA Isaac Sim integrated with ROS2 Nav2.

---

## Getting Started

### Prerequisite

- You must source your ROS 2 installation from the terminal before running Isaac Sim.
- The **Nav2** project is required. Refer to the [Nav2 installation page](https://navigation.ros.org/getting_started/index.html).
- Enable the `isaacsim.ros2.bridge` Extension: `Window > Extensions`.
- This tutorial requires `carter_navigation`, `iw_hub_navigation`, and `isaac_ros_navigation_goal` ROS2 packages, provided as part of your NVIDIA Isaac Sim download. Complete **ROS 2 Installation** and set up the ROS 2 workspace.

> **Note:** In Windows 10 or 11, depending on your machine's configuration, RViz2 might not open properly.

---

## Nav2 Setup

The following block diagram shows the ROS2 messages required for Nav2:

| ROS2 Topic | ROS2 Message Type |
|------------|-------------------|
| `/tf` | `tf2_msgs/TFMessage` |
| `/odom` | `nav_msgs/Odometry` |
| `/map` | `nav_msgs/OccupancyGrid` |
| `/point_cloud` | `sensor_msgs/PointCloud` |
| `/scan` | `sensor_msgs/LaserScan` (published by an external `pointcloud_to_laserscan` node) |

### Occupancy Map

1. Go to **Window > Examples > Robotics Examples**. Expand sections and open: `ROS2 > Navigation > Nova Carter` to load the warehouse scenario with the Nova Carter robot.
2. Click **Camera** in the viewport and select **Top**.
3. Go to **Tools > Robotics > Occupancy Map**.
4. Set **Origin** to `X: 0.0, Y: 0.0, Z: 0.0`. Lower bound `Z: 0.1`. Upper bound `Z: 0.62`.
5. Select the `warehouse_with_forklifts` prim and click **BOUND SELECTION**.
6. Delete the `Nova_Carter_ROS` prim from the stage.
7. Click **CALCULATE** followed by **VISUALIZE IMAGE**.
8. For **Rotate Image**, select `180 degrees`. For **Coordinate Type**, select **ROS Occupancy Map Parameters File (YAML)**. Click **RE-GENERATE IMAGE**.
9. Copy the full YAML text and create a file at `<ros2_ws>/src/navigation/carter_navigation/maps/carter_warehouse_navigation.yaml`.
10. Click **Save Image**, name it `carter_warehouse_navigation.png`, and save it in the same directory.

---

## Running Nav2

### Nav2 with Nova Carter in a Small Warehouse

1. Open the example: **Window > Examples > Robotics Examples** > `ROS2 > Navigation > Nova Carter`.
2. Click **Play** to begin simulation.
3. In a new terminal, launch Nav2:

   ```bash
   ros2 launch carter_navigation carter_navigation.launch.py
   ```

4. RViz2 opens and loads the occupancy map. Verify the robot is properly localized.
5. Click the **Navigation2 Goal** button, then click and drag at the desired location in the map.

> **Notes:**
> - The Carter robot uses **RTX Lidar** by default. You can add people assets into the scene.
> - Some Hawk camera pipelines are disabled by default. To enable, open the `_hawk` action graphs and enable `_camera_render_product` nodes.
> - All sensors publish with **Sensor Data QoS**. In RViz, set Topic > Reliability Policy to **Best Effort** if needed.
> - If you see `[Warning] [omni.graph.core.plugin] ... invalid dt 0.000000`, these are harmless.

### Nav2 with Robot Description

1. Install the `nova_carter_description` package (see section below).
2. Launch the robot description:

   ```bash
   ros2 launch carter_navigation nova_carter_description_isaac_sim.launch.py
   ```

3. Open the navigation scene in Isaac Sim: `ROS2 > Navigation > Nova Carter`.
4. Click **Play**, then launch Nav2:

   ```bash
   ros2 launch carter_navigation carter_navigation.launch.py
   ```

5. Verify the robot model is automatically loaded in RViz.

### Nav2 with robot_state_publisher

A new asset `Nova_Carter_Joint_States_ROS.usd` is used. Differences from the original:

- `transform_tree_odometry` action graph removed; an odometry action graph added.
- New `joint_states` action graph publishes movable joint states for `robot_state_publisher`.
- Hawk camera graphs include static TF publishers for left/right camera frames.

1. Install `nova_carter_description` (see below).
2. Open the example: `ROS2 > Navigation > Nova Carter Joint States`.
3. Click **Play**, then in a terminal:

   ```bash
   ros2 launch carter_navigation nova_carter_description_isaac_sim.launch.py
   ```

4. In another terminal:

   ```bash
   ros2 launch carter_navigation carter_navigation.launch.py
   ```

### Installing the Nova Carter Description Package

> **Note:** This section is only supported on **Linux** for ROS 2 Humble.

```bash
# Set up locale
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# Install dependencies
sudo apt update && sudo apt install gnupg wget
sudo apt install software-properties-common
sudo add-apt-repository universe

# Register NVIDIA's GPG Key and Repository
wget -qO - https://isaac.download.nvidia.com/isaac-ros/repos.key | sudo apt-key add -
grep -qxF "deb https://isaac.download.nvidia.com/isaac-ros/release-3 $(lsb_release -cs) release-3.0" /etc/apt/sources.list || \
echo "deb https://isaac.download.nvidia.com/isaac-ros/release-3 $(lsb_release -cs) release-3.0" | sudo tee -a /etc/apt/sources.list
sudo apt-get update

# Install the nova_carter_description package
sudo apt install ros-humble-nova-carter-description
```

### Nav2 with iw.hub in Warehouse

1. Open the example: `ROS2 > Navigation > iw_hub`.
2. Click **Play**, then:

   ```bash
   ros2 launch iw_hub_navigation iw_hub_navigation.launch.py
   ```

3. Set a goal using the **Navigation2 Goal** button. Verify the robot avoids dynamic obstacles.

---

## Sending Goals Programmatically

> **Note:** The `isaac_ros_navigation_goal` package is fully supported on **Linux**. On **Windows**, it might produce errors.

The `isaac_ros_navigation_goal` ROS2 package can set goal poses for the robot using a Python node.

### Parameters

| Parameter | Description |
|-----------|-------------|
| `goal_generator_type` | `RandomGoalGenerator` or `GoalReader` |
| `map_yaml_path` | Path to occupancy map YAML |
| `iteration_count` | Number of goals to set |
| `action_server_name` | Name of the action server |
| `obstacle_search_distance_in_meters` | Clearance distance for generated poses |
| `goal_text_file_path` | Path to text file with user-defined goals |
| `initial_pose` | Initial pose `[x, y, z, ox, oy, oz, ow]` |

### Running

1. Open `ROS2 > Navigation > Nova Carter`. Click **Play**.
2. Start Nav2:

   ```bash
   ros2 launch carter_navigation carter_navigation.launch.py
   ```

3. Start sending goals:

   ```bash
   ros2 launch isaac_ros_navigation_goal isaac_ros_navigation_goal.launch.py
   ```

The package stops when: iteration count reached, all goals published, a goal is rejected, or too many invalid poses generated.

---

## Sending Goals Using ActionGraph

> **Important:** Make sure Nav2 is installed. This section will not work with internal libraries.

1. Open **Robotics Examples** > `ROS2 > Navigation > Nova Carter`. Click **Load Sample Scene**.
2. Go to `ROS2 > Navigation > Add Waypoint Follower` to open the waypoint follower parameter window.

### Parameters

| Parameter | Description |
|-----------|-------------|
| **Graph Path** | Path within the stage |
| **Frame ID** | Reference frame for navigation |
| **Navigation Modes** | `Waypoint Mode` (single goal) or `Patrolling Mode` (2~50 waypoints) |
| **Waypoint Count** | Number of waypoints for Patrolling |

3. Click **Load Waypoint Follower ActionGraph**.
4. Click **Play**.
5. Launch Nav2:

   ```bash
   ros2 launch carter_navigation carter_navigation.launch.py
   ```

6. **Waypoint Mode**: Adjust `/World/Waypoints/waypoint_1`, open `ROS_Nav2_Waypoint_Follower` graph, click **Send Impulse** on `OnImpulseEvent`.
7. **Patrolling Mode**: Adjust waypoints, then click **Send Impulse**.

> **Note:** This tutorial uses the **AMCL** localizer. Harmless warnings may appear when deleting the graph.

---

## Summary

In this tutorial, you covered:

- Occupancy map generation.
- Running Isaac Sim with Nav2.
- Running the **Isaac ROS2 Navigation Goal** package to send navigation goals programmatically.
- Running **Waypoint Follower ActionGraph** to send navigation goals.

---

# Multiple Robot ROS2 Navigation

> **Support Limitations:** Multiple Robot ROS2 Navigation with Isaac Sim is fully supported on **Linux**. On **Windows**, it could potentially produce errors.

## Learning Objectives

In this ROS2 sample, we demonstrate NVIDIA Isaac Sim integrated with the ROS2 Nav2 stack to perform **simultaneous multiple robot navigation**.

---

## Getting Started

### Prerequisite

- Completed **ROS 2 Navigation** for ROS2 Nav2 with a single robot.
- ROS2 and Nav2 are installed.
- ROS2 bridge is enabled.
- `ros2_ws` is sourced so that `carter_navigation` and `isaac_ros_navigation_goal` are inside your workspace.

> **Note:** In Windows 10 or 11, depending on your machine's configuration, RViz2 might not open properly.

---

## Occupancy Map

We generate the map of both the **Hospital** and **Office** environments using the **Occupancy Map Generator** extension within NVIDIA Isaac Sim.

### Hospital Environment

1. Go to **Isaac Sim Content browser** > `Isaac Sim > Environments > Hospital`. Drag `hospital.usd` onto the stage. Zero out all **Translate** components.
2. In the viewport, switch **Perspective → Top**. Select the `/Hospital` prim and press **F** to zoom.
3. Go to **Tools > Robotics > Occupancy Map**.
4. Set **Origin** to `X: 0.0, Y: 0.0, Z: 0.0`. Lower bound `Z: 0.1`. Upper bound `Z: 0.62`.
5. Select the **Hospital** prim and click **BOUND SELECTION**.

### Office Environment

Follow the same steps using the office environment asset.

### Finalize Map

1. Click **CALCULATE** followed by **VISUALIZE IMAGE**.
2. Set **Rotate Image** to `180 degrees`, **Coordinate Type** to **ROS Occupancy Map Parameters File (YAML)**. Click **RE-GENERATE IMAGE**.
3. Copy the YAML text. Create `carter_hospital_navigation.yaml` (or `carter_office_navigation.yaml`) in `carter_navigation/maps/`.
4. Click **Save Image** with the same name and directory.

---

## Multiple Robot ROS2 Navigation Setup

1. Open the scene: **Window > Examples > Robotics Examples** > `ROS2 > Navigation > Multiple Robots > Hospital Scene` (or `Office Scene`).
2. Namespaces are utilized for multiple robots. The `node_namespace` OmniGraph node in each `Nova_Carter_ROS_X` action graph has been set to the corresponding robot name.
3. The launch files `multiple_robot_carter_navigation_hospital.launch.py` and `multiple_robot_carter_navigation_office.launch.py` are configured with the same namespaces.

---

## Running Multiple Robot ROS2 Navigation

1. Load the scenario (Hospital or Office scene).
2. Click **Play** to begin simulation.
3. In a new terminal, run:

   **Hospital:**
   ```bash
   ros2 launch carter_navigation multiple_robot_carter_navigation_hospital.launch.py
   ```

   **Office:**
   ```bash
   ros2 launch carter_navigation multiple_robot_carter_navigation_office.launch.py
   ```

4. Three RViz2 windows will launch (may take a moment).
5. In each RViz2 window, observe the **Topic** name and robot namespace.
6. In the `/carter1` namespaced RViz2 window, click **2D Nav Goal** and drag to set a destination.
7. Repeat for `/carter2` and `/carter3`.

> **Note:** Image publisher pipelines are disabled by default. To enable, open the `_hawk` action graphs under each `Nova_Carter_ROS` prim and enable `_camera_render_product` nodes. Set **Reliability Policy** to **Best Effort** in RViz if needed.

---

## Troubleshooting

This tutorial exhibits high CPU usage. If robots collide or have localization issues:

- Enable **Publish Full Scan** checkbox on the `publish_front_3d_lidar_scan` OmniGraph node under each robot's `ros_lidars` action graph.
- If issues persist, run Isaac Sim with Fabric:
  ```bash
  ./isaac-sim.fabric.sh --reset-user
  ```
  > **Important:** The above command is experimental.

---

## Sending Goals Programmatically for Multiple Robots

> **Note:** The `isaac_ros_navigation_goal` package is fully supported on **Linux**.

To send navigation goals to multiple robots simultaneously, setup node namespaces in the Python launch file:

```python
navigation_goal_node = Node(
    name="set_navigation_goal",
    package="isaac_ros_navigation_goal",
    executable="SetNavigationGoal",
    namespace="carter1",
    parameters=[{
        "map_yaml_path": map_yaml_file,
        "iteration_count": 3,
        "goal_generator_type": "RandomGoalGenerator",
        "action_server_name": "navigate_to_pose",
        "obstacle_search_distance_in_meters": 0.2,
        "initial_pose": [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
    }],
    output="screen",
)
```

Copy and paste the node declaration for `carter2` and `carter3` with updated namespaces and initial poses. Then add all nodes to the launch description:

```python
return LaunchDescription([
    navigation_goal_node,
    navigation_goal_node_2,
    navigation_goal_node_3
])
```

Run the modified launch file:

```bash
ros2 launch isaac_ros_navigation_goal isaac_ros_navigation_goal.launch.py
```

> **Note:** Ensure steps 1–4 from **Multiple Robot ROS2 Navigation Setup** have been run first.

---

## Summary

In this tutorial, we covered running multiple robots with the ROS2 navigation stack.

---

# ROS 2 Navigation with Block World Generator

## Learning Objectives

In this example, you learn how to:

- Generate a 3D world using a 2D occupancy map
- Perform navigation with a robot in the generated 3D world with Nav2

---

## Getting Started

### Prerequisite

- Completed **ROS 2 Navigation** for ROS 2 Nav2 with a single robot.
- ROS 2 and Nav2 are installed, and ROS2 bridge is enabled.
- Appropriate `ros2_ws` is sourced so that `carter_navigation` and `isaac_ros_navigation_goal` are inside your workspace.

> **Note:** In Windows 10 or 11, depending on your machine's configuration, RViz2 might not open properly.

---

## Setting Up Environment and Robot

### Generate 3D World

1. Go to **Tools > Robotics > Block World Generator**.
2. Press **Load Image** and open the occupancy map image located at `carter_navigation/maps/carter_warehouse_navigation.png`. A **Visualization** window will appear.
3. Press the **Generate** button to create geometry corresponding to the input occupancy map in the Stage.

> The generated 3D world automatically has a collision mesh applied for all occupied pixels.

### Add Robot in Scene

1. Go to **Isaac Sim Content browser** > `Isaac Sim > Samples > ROS2 > Robots`.
2. Drag and drop the `Nova_Carter_ROS.usd` asset into the scene (anywhere within the walls, on the ground).

### Add Clock in Scene

To ensure all external ROS 2 nodes reference simulation time, a **ROS_Clock** graph needs to be added. Follow the steps in **Graph Shortcut** to add a clock publisher for the `/clock` topic.

---

## Running Navigation

1. Click **Play** in Isaac Sim to begin simulation.
2. Open a new terminal and source the `<ros2_ws>` that contains the `carter_navigation` package.
3. Launch Nav2:

   ```bash
   ros2 launch carter_navigation carter_navigation.launch.py
   ```

4. RViz2 will open and begin loading the occupancy map. If a map does not appear, repeat the previous step.
5. Use the **2D Pose Estimate** button to set the robot's position approximately.
6. Click the **Navigation2 Goal** button, then click and drag at the desired location in the map. Nav2 will generate a trajectory and the robot will start moving.

---

## Summary

In this tutorial, you:

- Generated a 3D world using a 2D occupancy map with **Block World Generator**.
- Added a robot into this world and ran Nav2 with it.

---

# MoveIt 2

## Learning Objectives

Run a manipulation scene in Isaac Sim with **MoveIt 2**.

---

## Getting Started

### Prerequisite

- This tutorial requires `isaac_moveit` ROS 2 packages, provided as part of your NVIDIA Isaac Sim download. These are located inside the appropriate `humble_ws` or `jazzy_ws`. Complete **ROS 2 Installation** to ensure the workspace is set up correctly.
- If using multiple systems, set the `FASTRTPS_DEFAULT_PROFILES_FILE` environment variable before launching Isaac Sim and in any terminal where ROS messages will be sent or received. ROS2 Extension must be enabled.
- Completed **ROS2 Joint Control: Extension Python Scripting**.

---

## Running MoveIt 2

1. Load the environment: **Window > Examples > Robotics Examples** > `ROS2 > MoveIt > Franka MoveIt`.
2. Click **Play** to start simulation.
3. Run the launch file to start MoveIt 2:

   ```bash
   ros2 launch isaac_moveit isaac_moveit.launch.py
   ```

4. After RViz is launched, under **Planning Group**, select `hand`. Under **Goal State**, select `open`.

   > **Note:** On certain machines, selecting `close` under Goal State for the hand planning group may cause execution to fail/abort and execute later with a delay.

5. Under **Commands**, click **Plan**. The planned movement of the hand will be visualized.
6. Click **Execute**. The hand will start moving as planned.
7. To plan movement for the arm, under **Planning Group**, select `panda_arm`. Use the displayed arrows and rotation disks to set a goal position, or select `<random_valid>` under **Goal State**.
8. Click **Plan** followed by **Execute** to visualize and move the arm.

---

## Troubleshooting

If your RViz window shows a black screen where the robot should be, update your mesa driver:

```bash
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:kisak/kisak-mesa
sudo apt install -y mesa-utils
sudo apt -y upgrade
```

---

## Summary

Tips for running MoveIt2's Isaac Sim tutorial.

---

# ROS 2 Generic Publisher and Subscriber

## Learning Objectives

In this tutorial, we will:

- Have a brief discussion on ROS 2 message types
- Publish a message of **any type** to a ROS 2 topic
- Subscribe to a ROS 2 topic of **any message type**

---

## Getting Started

### Prerequisite

- Complete **ROS 2 Installation**.
- If using multiple systems, set the `FASTRTPS_DEFAULT_PROFILES_FILE` environment variable.
- ROS 2 Extension is enabled.

---

## ROS 2 Message Types

One of the main styles of communication interfaces of ROS 2 is the **topic**. It is used to send/receive continuous data streams like robot state (`nav_msgs/msg/Odometry`), sensors (`sensor_msgs/msg/Imu`), among others.

List available message types for the current sourced ROS 2 distro:

```bash
ros2 interface list --only-msgs
```

---

## Generic Publisher

### Basic Methodology

1. Go to **Window > Graph Editors > Action Graph** to create an Action Graph.
2. Add and connect the following OmniGraph nodes:

   | Node | Description |
   |------|-------------|
   | **On Playback Tick** | Execute other graph nodes every simulation frame. |
   | **ROS2 Context** | Create a context using the given Domain ID or `ROS_DOMAIN_ID`. |
   | **ROS2 Publisher** | Publish a message of any type to a ROS 2 topic. |

3. In the node **Property** panel, define the message type following the pattern: `messagePackage/messageSubfolder/messageName`. When a valid message type is defined, the node will reconfigure its input attributes.
4. Connect outputs from other nodes or set values in the Property panel.
5. Play the simulation to start publishing.

> **Note on attribute reconfiguration:**
> - Fields of ROS 2 embedded messages (e.g., `std_msgs/Header header`) are un-rolled into new attributes.
> - Fields of ROS 2 array of embedded messages (e.g., `geometry_msgs/Point32[] points`) are treated as a token array, each encoded as JSON.
>
> It is **not necessary** to play the simulation to (re)configure the node's input attributes.

---

### Example: Publish Joint States

Publish to `/joint_states` using `sensor_msgs/msg/JointState` with the Franka robot.

1. Load the Franka robot: **Window > Examples > Robotics Examples** > `Import Robots > Franka URDF` > **LOAD AND CONFIGURE**.
2. Create an Action Graph and add the following nodes:

   | Node | Input Field | Value |
   |------|-------------|-------|
   | **ROS2 Publisher** | `messagePackage` | `sensor_msgs` |
   | | `messageName` | `JointState` |
   | | `topicName` | `joint_states` |
   | **Articulation State** | `targetPrim` | `/panda` |

3. Additional nodes: **On Playback Tick**, **Isaac Read Simulation Time**, **Isaac Time Splitter**, **ROS2 Context**.
4. Play the simulation and click **MOVE** in the Import Franka window.
5. In a ROS2-sourced terminal:

   ```bash
   ros2 topic echo /joint_states
   ```

---

### Example: Publish Object Pose

Publish to `/object_pose` using `geometry_msgs/msg/Pose` for a falling cube.

1. Create a Cube: `Create > Shape > Cube`. Add `Physics > Rigid Body with Colliders Preset`.
2. Create an Action Graph with the following nodes:

   | Node | Input Field | Value |
   |------|-------------|-------|
   | **ROS2 Publisher** | `messagePackage` | `geometry_msgs` |
   | | `messageName` | `Pose` |
   | | `topicName` | `object_pose` |
   | **Read Prim Attribute** (upper) | `Prim` | `/World/Cube` |
   | | `Attribute Name` | `xformOp:translate` |
   | **Read Prim Attribute** (lower) | `Prim` | `/World/Cube` |
   | | `Attribute Name` | `xformOp:orient` |

3. Additional nodes: **On Playback Tick**, **Break 3-Vector**, **ROS2 Context**.
4. Play the simulation. Observe messages:

   ```bash
   ros2 topic echo /object_pose
   ```

---

## Generic Subscriber

### Basic Methodology

1. Go to **Window > Graph Editors > Action Graph** to create an Action Graph.
2. Add and connect the following OmniGraph nodes:

   | Node | Description |
   |------|-------------|
   | **On Playback Tick** | Execute other graph nodes every simulation frame. |
   | **ROS2 Context** | Create a context using the given Domain ID or `ROS_DOMAIN_ID`. |
   | **ROS2 Subscriber** | Subscribe to a ROS 2 topic of any message type. |

3. In the node **Property** panel, define the message type following the pattern: `messagePackage/messageSubfolder/messageName`. The node will reconfigure its output attributes.
4. Connect the node outputs to other nodes to consume the received data.
5. Play the simulation to get subscriptions.

> **Note:** Attribute reconfiguration follows the same rules as the Generic Publisher (embedded messages un-rolled, arrays as JSON token arrays).

---

### Example: Subscribe to Object Pose

Teleport a cube to a received pose.

1. Create a Cube: `Create > Shape > Cube`.
2. Create an Action Graph with the following nodes:

   | Node | Input Field | Value |
   |------|-------------|-------|
   | **ROS2 Subscriber** | `messagePackage` | `geometry_msgs` |
   | | `messageName` | `Pose` |
   | | `topicName` | `object_pose` |
   | **Write Prim Attribute** (upper) | `Prim` | `/World/Cube` |
   | | `Attribute Name` | `xformOp:translate` |
   | **Write Prim Attribute** (lower) | `Prim` | `/World/Cube` |
   | | `Attribute Name` | `xformOp:orient` |

3. Additional nodes: **On Playback Tick**, **Make 3-Vector**, **ROS2 Context**.
4. Play the simulation. In another terminal, teleport the cube:

   ```bash
   ros2 topic pub -1 /object_pose geometry_msgs/msg/Pose "{position: {x: 1, y: 2, z: 3}, orientation: {x: 0.4619398, y: 0.1913417, z: 0.4619398, w: 0.7325378}}"
   ```

---

## Summary

In this tutorial we learned how to publish any available message type to a ROS 2 topic as well as how to subscribe to a ROS 2 topic of any available message type.

---

# ROS 2 Generic Server and Client

## Learning Objectives

In this example, you learn how to use Isaac Sim to:

- Receive a ROS2 message of any type and respond using **generic server** nodes
- Send a ROS2 message of any type and receive the response using **generic client** nodes

---

## Getting Started

### Prerequisite

- Complete **ROS 2 Installation**.
- If using multiple systems, set the `FASTRTPS_DEFAULT_PROFILES_FILE` environment variable.
- ROS 2 Extension is enabled.

---

## ROS 2 Message Types

See **ROS 2 Generic Publisher and Subscriber** for background on ROS2 topics and message types. Generic services (server and client) build on a similar communication style.

List all available services in your environment:

```bash
ros2 interface list --only-srvs
```

A service configuration file is comprised of two sections:

1. **Request** — the message sent by a client and received by the server.
2. **Response** — the message sent by the server and received by the client.

---

## Generic Server

### Basic Methodology

1. Go to **Window > Graph Editors > Action Graph** to create an Action Graph.
2. Add and connect the following OmniGraph nodes:

   | Node | Description |
   |------|-------------|
   | **On Playback Tick** | Execute other graph nodes every simulation frame. |
   | **ROS2 Context** | Create a context using the given Domain ID or `ROS_DOMAIN_ID`. |
   | **ROS2 Service Server Request** | Receive a ROS2 service request message of any type. |
   | **ROS2 Service Server Response** | Respond to a ROS2 service request message of any type. |

3. Make the following connections:
   - **Server Handle** output of **Request** → **Server Handle** input of **Response** (shares the same server)
   - **On received** output of **Request** → **On received** input of **Response** (sends response only on request)
   - Playback tick → Request node; Context → both Request and Response nodes

4. In the node **Property** panel, define the message type using the pattern: `messagePackage/messageSubfolder/messageName`.

   > **Note:** You must enter the same message fields for both Request and Response nodes. For example, for `std_srvs/srv/SetBool`: `messagePackage = std_srvs`, `messageSubfolder = srv`, `messageName = SetBool`.

5. The outputs of the **Request** node include the service request fields; the inputs of the **Response** node include the service response fields.

   > It is **not necessary** to play the simulation to (re)configure the node's attributes.

6. Modify the **Service Name** property of the Request node as needed.
7. Play the simulation. The server is now ready to receive requests.

### Testing the Server

In a separate terminal, send a request:

```bash
ros2 service call /service_name std_srvs/srv/SetBool "{data: true}"
```

Validate the response matches the values you set in the **ROS2 Service Server Response** node.

---

## Generic Client

### Basic Methodology

1. Go to **Window > Graph Editors > Action Graph** to create an Action Graph.
2. Add and connect the following OmniGraph nodes:

   | Node | Description |
   |------|-------------|
   | **On Playback Tick** | Execute other graph nodes every simulation frame. |
   | **ROS2 Context** | Create a context using the given Domain ID or `ROS_DOMAIN_ID`. |
   | **ROS2 Service Client** | Send a ROS2 request message of any type and receive the response. |

3. In the node **Property** panel, define the message type following the pattern: `messagePackage/messageSubfolder/messageName`. The node inputs/outputs reconfigure to include the Request/Response fields.
4. Play the simulation. The client starts making requests according to its input data.

### Example: Server + Client in the Same Graph

Configure both server and client nodes in the same graph. The client sends requests and the server responds. Verify the client node receives the response you provided in the server node.

---

## Summary

In this tutorial you learned how to reconfigure the generic server and client nodes to send and receive any ROS2 messages in Isaac Sim.

---

# ROS 2 Service for Manipulating Prims Attributes

## Learning Objectives

In this tutorial, you:

- Have a brief discussion on the Isaac Sim ROS 2 service message types for manipulating prims attributes.
- Create ROS 2 services to list prims and their attributes, as well as to read and write a specific prim attribute.

---

## Getting Started

### Prerequisite

- Complete **ROS 2 Installation**.
- If using multiple systems, set the `FASTRTPS_DEFAULT_PROFILES_FILE` environment variable.
- ROS 2 Extension is enabled.
- The **Isaac Sim ROS 2 Workspace** (with the `isaac_ros2_messages` ROS 2 package) built and sourced in the terminal where the service will be called.

> **Note:** Isaac Sim already has this service included as part of the internal ROS 2 bridge libraries.

---

## Service Message Types

The **ROS2 Service Prim** node provides four services:

### Get all prim paths (and types) under a specific path

`isaac_ros2_messages/srv/GetPrims`

```
string path
---
string[] paths
string[] types
bool success
string message
```

### Get all attribute names and types for a specific prim

`isaac_ros2_messages/srv/GetPrimAttributes`

```
string path
---
string[] names
string[] displays
string[] types
bool success
string message
```

### Get a prim attribute type and value

`isaac_ros2_messages/srv/GetPrimAttribute`

```
string path
string attribute
---
string value
string type
bool success
string message
```

### Set a prim attribute value

`isaac_ros2_messages/srv/SetPrimAttribute`

```
string path
string attribute
string value
---
bool success
string message
```

> **Note:** Prim attributes are read and written as JSON (applied directly to the data, without keys). Arrays, vectors, matrices and other numeric containers (e.g., `pxr.Gf.Vec3f`, `pxr.Gf.Matrix4d`, `pxr.Gf.Quatd`) are interpreted as a list of numbers (row first).

---

## Manipulating Prims Attributes

Example: list prims and attributes, read and write the pose of a Cube.

1. Create a Cube: `Create > Shape > Cube`.
2. Go to **Window > Graph Editors > Action Graph**. Create an Action Graph and add the **ROS2 Service Prim** node.
3. Connect it with **On Playback Tick** and **ROS2 Context**.
4. Play the simulation to start the services.

### List available services

```bash
ros2 service list
```

### Get all child prim paths and types under `/World`

```bash
ros2 service call /get_prims isaac_ros2_messages/srv/GetPrims "{path: /World}"
```

### Get all attribute names and types for Cube

```bash
ros2 service call /get_prim_attributes isaac_ros2_messages/srv/GetPrimAttributes "{path: /World/Cube}"
```

### Get the pose (position and orientation) of Cube

```bash
# get position
ros2 service call /get_prim_attribute isaac_ros2_messages/srv/GetPrimAttribute "{path: /World/Cube, attribute: xformOp:translate}"
# get orientation (quaternion: wxyz)
ros2 service call /get_prim_attribute isaac_ros2_messages/srv/GetPrimAttribute "{path: /World/Cube, attribute: xformOp:orient}"
```

### Set the pose of Cube

```bash
# set position
ros2 service call /set_prim_attribute isaac_ros2_messages/srv/SetPrimAttribute "{path: /World/Cube, attribute: xformOp:translate, value: [1, 2, 3]}"
# set orientation (quaternion: wxyz)
ros2 service call /set_prim_attribute isaac_ros2_messages/srv/SetPrimAttribute "{path: /World/Cube, attribute: xformOp:orient, value: [0.7325378, 0.4619398, 0.1913417, 0.4619398]}"
```

---

## Summary

In this tutorial you learned how to create ROS 2 services to list prims and their attributes, as well as to read and write a specific prim attribute.

---

# ROS 2 Python Custom Messages

> **Note:** ROS 2 Python Custom Messages with Isaac Sim is fully supported on **Linux**. On **Windows (WSL)**, this workflow is not supported.

## Learning Objectives

In this example, you learn how to use ROS 2 `rclpy` Python interface with Isaac Sim for a custom message.

---

## Getting Started

### Prerequisite

- Basic understanding of building ROS 2 packages.

---

## Using Custom Messages with Python

For using `rclpy` with Isaac Sim, the packages must be built with **Python 3.11** (Isaac Sim's Python version). Packages built with Python 3.11 can be used directly with `rclpy` in Isaac Sim.

This tutorial uses the `custom_message` package, part of the **Isaac Sim ROS Workspace** repository. It contains a custom message under `custom_message/msg/SampleMsg.msg`:

```
std_msgs/String my_string
int64 my_num
```

### Building Your Own Custom Message Package

1. Place your package under `<ros_ws>/src/` (e.g., `humble_ws/src` or `jazzy_ws/src`).
2. Run `./build_ros.sh` to build.
3. Source your workspace before running Isaac Sim.

### Using the custom_message Package

Launch Isaac Sim from the sourced terminal containing the `custom_message` package.

#### Script Editor

Open the **Script Editor** and run:

```python
import rclpy
from custom_message.msg import SampleMsg

# Create message
sample_msg = SampleMsg()

# Assign data
sample_msg.my_string.data = "hello from Isaac Sim!"
sample_msg.my_num = 23

print("Message assignment completed!")
```

Verify that `Message assignment completed` is logged on the console.

#### Standalone Python Scripts

The same import and usage pattern works in standalone Python scripts run from the sourced terminal.

---

## Summary

This tutorial covered the following topics:

- Building a ROS 2 custom message package with Python 3.11.
- Using the custom message with `rclpy` in Isaac Sim.
- Overview of steps to build and use your own custom message package with `rclpy` and Isaac Sim.

---

# ROS 2 Python Custom OmniGraph Node

> This is an **optional, advanced** tutorial.

## Learning Objectives

You will learn how to:

- Use ROS 2 `rclpy` Python interface with Isaac Sim
- Create a basic custom OmniGraph Python node (using the **Isaac Sim VS Code Edition**) that can subscribe to a topic (`std_msgs/msg/Int32`) and output the Fibonacci computation of the published number.

---

## Getting Started

### Prerequisite

- Completed **ROS 2 Installation**: ROS2 installed, ROS2 extension enabled, Isaac Sim ROS 2 workspace built.
- Completed the tutorial for writing custom Python nodes: **Custom Python Nodes**.

---

## Creating the ROS 2 Custom OmniGraph Python Node

### Step 1: Generate Template

Go to **Template > Extension** in the Isaac Sim VS Code Edition (VS Code extension) to open the wizard.

| Field | Value |
|-------|-------|
| Ext. name | `custom.python.ros2_node` |
| Ext. path | (your target path) |
| Ext. title | ROS 2 Python Custom OmniGraph Node |
| Ready-to-use extension | ✅ Checked |
| Omnigraph node | ✅ Checked |

### Step 2: Edit Extension Configuration

Edit `custom.python.ros2_node/config/extension.toml` to add the ROS 2 Bridge dependency:

```toml
[dependencies]
"isaacsim.ros2.bridge" = {}
```

### Step 3: Edit OmniGraph Definition (.ogn)

Edit `OgnCustomPythonRos2NodePy.ogn`:

```json
{
    "CustomPythonRos2NodePy": {
        "version": 1,
        "language": "python",
        "uiName": "Custom Python ROS 2 Node",
        "description": [
            "Subscribes to std_msgs/msg/Int32 topic and outputs the Fibonacci number"
        ],
        "inputs": {
            "execIn": {
                "type": "execution",
                "description": "Input execution trigger"
            },
            "topic": {
                "type": "string",
                "default": "/number",
                "description": "Topic to subscribe to"
            }
        },
        "outputs": {
            "execOut": {
                "type": "execution",
                "description": "Output execution trigger"
            },
            "fibonacci": {
                "type": "uint64",
                "description": "Computed Fibonacci number"
            }
        }
    }
}
```

### Step 4: Edit OmniGraph Python Source

Edit `OgnCustomPythonRos2NodePy.py`:

```python
import rclpy
import std_msgs.msg
import omni.graph.core
from isaacsim.core.nodes import BaseResetNode
from custom.python.ros2_node.ogn.OgnCustomPythonRos2NodePyDatabase import OgnCustomPythonRos2NodePyDatabase


class OgnCustomPythonRos2NodePyInternalState(BaseResetNode):
    """Per-node state: ROS 2 node, subscription, received data."""

    def __init__(self):
        self._data = None
        self._ros2_node = None
        self._subscription = None
        super().__init__(initialize=False)

    @property
    def data(self):
        tmp = self._data
        self._data = None
        return tmp

    def _callback(self, msg):
        self._data = msg.data

    def initialize(self, node_name, topic_name):
        try:
            rclpy.init()
        except:
            pass
        if not self._ros2_node:
            self._ros2_node = rclpy.create_node(node_name=node_name)
        if not self._subscription:
            self._subscription = self._ros2_node.create_subscription(
                msg_type=std_msgs.msg.Int32, topic=topic_name, callback=self._callback, qos_profile=10
            )
        self.initialized = True

    def spin_once(self, timeout_sec=0.01):
        rclpy.spin_once(self._ros2_node, timeout_sec=timeout_sec)

    def custom_reset(self):
        if self._ros2_node:
            self._ros2_node.destroy_subscription(self._subscription)
            self._ros2_node.destroy_node()
        self._data = None
        self._ros2_node = None
        self._subscription = None
        self.initialized = False
        rclpy.try_shutdown()


class OgnCustomPythonRos2NodePy:
    """The OmniGraph node class"""

    @staticmethod
    def fibonacci(n):
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

    @staticmethod
    def internal_state():
        return OgnCustomPythonRos2NodePyInternalState()

    @staticmethod
    def compute(db) -> bool:
        state = db.per_instance_state
        try:
            if not state.initialized:
                state.initialize(node_name="custom_python_ros2_node", topic_name=db.inputs.topic)
            state.spin_once()
            number = state.data
            if number is not None:
                value = OgnCustomPythonRos2NodePy.fibonacci(number)
                if value > 2**64:
                    db.log_warn(f"Fibonacci number {number} exceeds uint64 capacity")
                    return False
                db.outputs.fibonacci = value
                db.outputs.execOut = omni.graph.core.ExecutionAttributeState.ENABLED
        except Exception as e:
            db.log_error(f"Computation error: {e}")
            return False
        return True

    @staticmethod
    def release(node):
        try:
            state = OgnCustomPythonRos2NodePyDatabase.per_instance_internal_state(node)
        except Exception:
            return
        state.reset()
        state.initialized = False
```

---

## Running the Custom OmniGraph Node

> **Warning:** The custom extension must first be **activated** for the OmniGraph node to be available.

1. Enable the extension: **Window > Extensions**, search for `custom.python.ros2_node`.
2. Create a new Action Graph: **Window > Graph Editors > Action Graph**.
3. Add and connect the following nodes:

   | Node | Role |
   |------|------|
   | **On Playback Tick** | Execute every simulation frame |
   | **Custom Python ROS 2 Node** | Subscribe to topic, compute Fibonacci |
   | **To String** | Convert uint64 output to string |
   | **Print Text** | Display output in viewport (check **To Screen**) |

4. Play the simulation.
5. In a ROS2-sourced terminal, publish a number:

   ```bash
   ros2 topic pub -1 /number std_msgs/msg/Int32 "{data: 10}"
   ```

   The Fibonacci number (55 for input 10) will appear in the top-left corner of the viewport.

> **Note:** To view values in the console instead, uncheck **To Screen** and set **Log Level** to **Warning** in the Print Text node properties.

---

## Summary

This tutorial covered:

- Creating a custom OmniGraph Python node in an extension.
- Using `rclpy` to create a ROS 2 node within a custom OmniGraph node to subscribe to a topic, perform Fibonacci computation, and trigger downstream nodes.

---

# ROS 2 Custom C++ OmniGraph Node

> **Note:** This tutorial is supported only on **Linux** with **ROS 2 Humble**.

## Learning Objectives

In this example, you learn how to:

- Write a custom **C++ OmniGraph node** to use with Isaac Sim.

---

## Getting Started

### Prerequisite

- Basic understanding of building ROS 2 packages.

---

## Building a Custom Message Package

To use a custom message with Isaac Sim, build it with ROS 2. Follow the [ROS 2 Humble Documentation for Creating custom msg and srv files](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html).

Message definition (`SphereMsg.msg`):

```
geometry_msgs/Point center
float64 radius
```

> **Important:** Follow the package and message naming conventions in the official tutorials — they are required when building C++ OmniGraph nodes.

---

## Setting Up Kit Extension C++ Template

1. Clone **Omniverse Kit Extension Template C++** and switch to the `release/107.3.0` branch:

   ```bash
   git checkout release/107.3.0
   ```

2. Run `./build.sh` to build the sample extensions.
3. Verify `./_build/linux-x86_64/release/omni.app.kit.dev.sh` works.

4. Download the sample custom extension for this tutorial: **Custom ROS 2 OmniGraph Node Extension (Humble)**. Extract `omni.example.cpp.omnigraph_node_ros` into `source/extensions/`.

5. Edit `deps/kit-sdk-deps.packman.xml` and add before `</project>`:

   ```xml
   <dependency name="system_ros" linkPath="../_build/target-deps/system_ros" tags="${config}">
       <source path="/opt/ros/humble" />
   </dependency>
   <dependency name="additional_ros_workspace" linkPath="../_build/target-deps/additional_ros" tags="${config}">
       <source path="/home/user/ros2_ws/install/tutorial_interfaces" />
   </dependency>
   ```

6. Run `./build.sh` to build the extension with ROS 2 OmniGraph nodes.

> **Important:** Provide **complete absolute paths** for `source_path` in both dependencies.

---

## Adding the Extension to Isaac Sim

1. Source the `install/local_setup.bash` of the workspace containing `tutorial_interfaces`:

   ```bash
   source install/local_setup.bash
   ```

   > Do **not** source the ROS 2 installation directly — it can cause Python version conflicts.

2. Run Isaac Sim from this terminal.
3. Go to **Window > Extensions**. Click the hamburger menu → **Settings**. Click **+** under **Extension Search Paths** and add the path to your built extension (`kit-extension-template-cpp/_build/linux-x86_64/release/exts`).
4. Verify the extension appears under the **Third Party** tab.
5. Enable **Custom ROS2 OGN Example Extension**.

> **Error:** If you see `libtutorial_interfaces__rosidl_typesupport_c.so: cannot open shared object file`, your custom package is not sourced correctly.

---

## Building the Action Graph and Running the Nodes

With the extension enabled:

1. Go to **Window > Graph Editors > Action Graph**.
2. Search for **ROS 2** and drag both nodes: **ROS 2 Publish Custom Message** and **ROS 2 Publish String**.
3. Add **On Playback Tick** and connect **Tick** → **Exec In** of both ROS 2 nodes.
4. Click **Play**.

Verify topics in a ROS2-sourced terminal:

```bash
ros2 topic list
```

Expected output:

```
/custom_node/my_string
/custom_node/sphere_msg
```

---

## Deeper Dive: premake5.lua

The `premake5.lua` handles building the extension:

- Compiles and links against specified ROS install paths
- Includes minimal ROS 2 C API libraries: `rosidl_runtime_c`, `rcutils`, `rcl`, `rmw`
- Links message-specific libraries: `std_msgs__rosidl_typesupport_c`, `tutorial_interfaces__rosidl_typesupport_c`, etc.
- Uses **C++17**

The OmniGraph C++ nodes are located under `plugins/nodes/`. The `compute()` function is called when `Exec In` is triggered — this is where the node, publisher, and message publishing are handled.

---

## Summary

This tutorial covered:

- Building your own extension containing ROS 2 C++ OmniGraph nodes.
- Using these nodes with Isaac Sim.

---

# ROS 2 Launch

> **Note:** ROS 2 Launch with Isaac Sim is only supported in **Linux**. The `isaacsim` package is not supported in WSL2.

## Learning Objectives

In this tutorial, we demonstrate running NVIDIA Isaac Sim from a **ROS 2 launch file**.

---

## Getting Started

### Prerequisite

- ROS 2 Launch for Isaac Sim is only supported on **Linux**.
- Completed **ROS 2 Navigation** for ROS 2 Nav2 with a single robot.
- ROS 2 and Nav2 are installed. ROS 2 bridge is enabled.
- This tutorial requires `carter_navigation`, `isaac_ros_navigation_goal`, and `isaacsim` ROS 2 packages, provided as part of your NVIDIA Isaac Sim download. Complete **ROS 2 Installation**.

---

## Launching Isaac Sim with ROS 2

The `isaacsim` package contains scripts and a ROS 2 launch file (`run_isaacsim.launch.py`).

### Launch Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `version` | Isaac Sim version to use. Empty = latest. | `5.1.0` |
| `install_path` | Non-default install path. Overrides `version`. | `""` |
| `use_internal_libs` | Use internal ROS libraries (Python 3.11). | `true` |
| `dds_type` | DDS implementation: `fastdds` or `cyclonedds`. | `fastdds` |
| `gui` | USD file path to open in GUI mode. | `""` |
| `standalone` | Python file path for standalone workflow. | `""` |
| `play_sim_on_start` | Auto-play simulation after loading. | `false` |
| `ros_distro` | ROS distribution (only Humble). | `humble` |
| `ros_installation_path` | Comma-separated paths to custom ROS install + workspace `setup.bash` / `local_setup.bash`. | `""` |
| `headless` | Set to `webrtc` for headless mode. | `""` |
| `custom_args` | Custom Isaac Sim args forwarded to `isaac-sim.sh`. | `""` |
| `exclude_install_path` | Comma-separated paths to exclude from `LD_LIBRARY_PATH`, `PYTHONPATH`, `PATH`. | `""` |

### Launch Examples

**Default configuration:**

```bash
ros2 launch isaacsim run_isaacsim.launch.py
```

**With custom ROS packages (Python 3.11 build):**

```bash
ros2 launch isaacsim run_isaacsim.launch.py \
  exclude_install_path:=/home/user/IsaacSim-ros_workspaces/humble_ws/install \
  ros_installation_path:=/home/user/IsaacSim-ros_workspaces/build_ws/humble/humble_ws/install/local_setup.bash
```

**With a USD file opened and auto-play:**

```bash
ros2 launch isaacsim run_isaacsim.launch.py \
  gui:=https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/5.1/Isaac/Samples/ROS2/Robots/Nova_Carter_ROS.usd \
  play_sim_on_start:=true
```

**Standalone workflow:**

```bash
ros2 launch isaacsim run_isaacsim.launch.py \
  standalone:=$HOME/isaacsim/standalone_examples/api/isaacsim.ros2.bridge/moveit.py
```

---

## Launch Isaac Sim with Nav2

The Isaac Sim launch file can be included in other launch files. The example is in `carter_navigation/launch/carter_navigation_isaacsim.launch.py`.

The launch file waits for the console output: `"Stage loaded and simulation is playing."` — printed from `open_isaacsim_stage.py` in the `isaacsim` package.

```bash
ros2 launch carter_navigation carter_navigation_isaacsim.launch.py
```

Wait for the scene to load. RViz2 will automatically display the robot's sensor data and automatic goals will be generated.

> **Note:** If automatic goals fail, Nav2 may not have initialized yet. Add a manual delay in `carter_navigation_isaacsim.launch.py` (see comments in the file).

Same workflow with `iw_hub`:

```bash
ros2 launch iw_hub_navigation iw_hub_navigation_isaacsim.launch.py
```

---

## Summary

In this tutorial, we covered:

- Launching Isaac Sim from a ROS 2 launch file.
- Running an integrated launch file with Isaac Sim, Nav2 stack, and the `isaac_ros_navigation_goal` package.

---

# ROS2 Simulation Control

## Learning Objectives

In this page, you will learn how to:

- Understand the ROS 2 Simulation Control extension for Isaac Sim
- Control Isaac Sim simulations using ROS 2 services and actions
- Manipulate simulation entities and worlds using ROS 2 interfaces
- Step through simulations programmatically

---

## Getting Started

### Prerequisite

Complete **ROS 2 Installation**.

If using multiple systems, set the `FASTRTPS_DEFAULT_PROFILES_FILE` environment variable as per instructions in ROS 2 Installation before launching Isaac Sim, as well as any terminal where ROS messages will be sent or received, and ROS2 Extension is enabled.

Isaac Sim 5.0 or later

ROS 2 (Humble or later)

Install Simulation Interfaces package using:

**Humble**
```bash
sudo apt install ros-humble-simulation-interfaces
```

**Jazzy**
> For reference, see the source code for the Simulation Interfaces package [here](https://github.com/ros-simulation/simulation_interfaces/).

---

## Overview

The ROS 2 Simulation Control extension uses the ROS 2 Simulation Interfaces to control Isaac Sim functions. This extension is designed to be scalable, allowing multiple services and actions to run simultaneously with little performance overhead.

The extension provides comprehensive control over Isaac Sim through ROS 2 services and actions, including:

- **Simulation State Control**: Play, pause, stop, and step through simulations
- **Entity Management**: Spawn, delete, and manipulate simulation entities (prims)
- **World Management**: Load, unload, and query simulation worlds (USD files)
- **State Querying**: Get information about entities, simulation state, and available resources

This allows you to control Isaac Sim programmatically or through the ROS 2 command line interface using the Simulation Interfaces package to enable workflows like automated testing. This page lists and provides example commands for all of the services and actions from Simulation Interfaces supported by Isaac Sim.

---

## Enabling the Extension

### Enable Automatically

Open Isaac Sim from the terminal with the following command:

```bash
./isaac-sim.sh --/isaac/startup/ros_sim_control_extension=True
```

### Enable Manually

1. Open Isaac Sim
2. Enable the extension from the Extension Manager: `isaacsim.ros2.sim_control`

---

## Available Services and Actions

The extension provides the following ROS 2 services:

- `/get_simulator_features`: Lists the supported features in this Isaac Sim implementation
- `/set_simulation_state`: Set simulation to specific state (stopped/playing/paused/quitting)
- `/get_simulation_state`: Get current simulation state
- `/get_entities`: Get list of all entities (prims) in the simulation
- `/get_entity_info`: Get detailed information about a specific entity (currently returns OBJECT category type)
- `/get_entity_state`: Get the pose, twist, and acceleration of a specific entity
- `/get_entities_states`: Get the states (pose, twist, acceleration) of multiple entities with filtering
- `/delete_entity`: Delete a specific entity (prim) from the simulation
- `/spawn_entity`: Spawn a new entity into the simulation at a specified location
- `/reset_simulation`: Reset the simulation environment to its initial state
- `/set_entity_state`: Sets the state (pose, twist) of a specific entity in the simulation
- `/step_simulation`: Step the simulation forward by a specific number of frames
- `/load_world`: Load a world or environment file into the simulation
- `/unload_world`: Unload the current world and create an empty stage
- `/get_current_world`: Get information about the currently loaded world
- `/get_available_worlds`: Get a list of available world files that can be loaded

And the following ROS 2 actions:

- `/simulate_steps`: Action for stepping the simulation with progress feedback

---

## Using the ROS 2 Simulation Control Services

This section describes how to use each of the available services in detail.

### GetSimulatorFeatures Service

The `GetSimulatorFeatures` service lists the subset of services and actions supported by Isaac Sim from `simulation_interfaces`.

```bash
ros2 service call /get_simulator_features simulation_interfaces/srv/GetSimulatorFeatures
```

**Notes:**
- Returns a list of supported features (for example, `SPAWNING`, `DELETING`, `ENTITY_STATE_GETTING`)
- Reports USD file format support using the `spawn_formats` field
- Provides `custom_info` with details about the implementation
- See the [full list of simulator features](https://github.com/ros-simulation/simulation_interfaces/blob/main/simulation_interfaces/srv/GetSimulatorFeatures.srv)

### SetSimulationState Service

The `SetSimulationState` service updates the global state of the simulation (stopped/playing/paused/quitting) corresponding to enums defined in `SimulationState.msg` (`STATE_STOPPED`, `STATE_PLAYING`, `STATE_PAUSED`, `STATE_QUITTING`).

To set simulation state to playing:

```bash
ros2 service call /set_simulation_state simulation_interfaces/srv/SetSimulationState "{state: {state: 1}}"  # 1=playing
```

To set simulation state to paused:

```bash
ros2 service call /set_simulation_state simulation_interfaces/srv/SetSimulationState "{state: {state: 2}}"  # 2=paused
```

To set simulation state to stopped:

```bash
ros2 service call /set_simulation_state simulation_interfaces/srv/SetSimulationState "{state: {state: 0}}"  # 0=stopped
```

To quit the simulator:

```bash
ros2 service call /set_simulation_state simulation_interfaces/srv/SetSimulationState "{state: {state: 3}}"  # 3=quit
```

**Notes:**
- State 0 (Stopped) is equivalent to pausing and resetting the simulation
- State 1 (Playing) starts the simulation timeline
- State 2 (Paused) pauses the simulation at the current time
- State 3 (Quitting) shuts down Isaac Sim

### GetSimulationState Service

The `GetSimulationState` service retrieves the current state of the entire simulation (stopped/playing/paused/quitting) corresponding to enums defined in `SimulationState.msg` (`STATE_STOPPED`, `STATE_PLAYING`, `STATE_PAUSED`, `STATE_QUITTING`).

```bash
ros2 service call /get_simulation_state simulation_interfaces/srv/GetSimulationState
```

**Notes:**
- Returns state 0 for stopped, 1 for playing, 2 for paused
- Used to query the simulation state before performing operations like stepping

### GetEntities Service

The `GetEntities` service retrieves a list of all entities present in the simulation with optional filtering (using regex pattern).

Get all entities in the simulation:

```bash
ros2 service call /get_entities simulation_interfaces/srv/GetEntities "{filters: {filter: ''}}"
```

Get entities with full paths or partial paths. In this case filter for prims containing 'camera' in the path:

```bash
ros2 service call /get_entities simulation_interfaces/srv/GetEntities "{filters: {filter: 'camera'}}"
```

Get entities with paths starting with '/World':

```bash
ros2 service call /get_entities simulation_interfaces/srv/GetEntities "{filters: {filter: '^/World'}}"
```

Get entities with paths ending with 'mesh':

```bash
ros2 service call /get_entities simulation_interfaces/srv/GetEntities "{filters: {filter: 'mesh$'}}"
```

**Notes:**
- The `filter` parameter accepts POSIX Extended regular expressions for matching entity names (prim paths)
- Isaac Sim uses the full USD prim paths as entity names

### GetEntityInfo Service

The `GetEntityInfo` service provides detailed information about a specific entity, such as its type and properties.

```bash
ros2 service call /get_entity_info simulation_interfaces/srv/GetEntityInfo "{entity: '/World/robot'}"
```

**Notes:**
- Returns `RESULT_OK` with `EntityInfo` if the entity exists
- Returns `RESULT_OPERATION_FAILED` if the entity doesn't exist
- The `EntityInfo` contains:
  - `category`: Currently always set to `OBJECT` (EntityCategory.OBJECT)
  - `description`: Empty string (reserved for future use)
  - `tags`: Empty array (reserved for future use)

### GetEntityState Service

The `GetEntityState` service gets the pose, twist, acceleration of a specific entity relative to a given reference frame. Currently only world frames are supported.

```bash
ros2 service call /get_entity_state simulation_interfaces/srv/GetEntityState "{entity: '/World/robot'}"
```

**Notes:**
- For entities with RigidBodyAPI, both pose and velocities will be returned
- For entities without RigidBodyAPI, only pose will be returned with zero velocities
- Acceleration values are always reported as zero (not provided by the current API)
- Returns `RESULT_OK` if successfully retrieved entity state
- Returns `RESULT_NOT_FOUND` if entity does not exist
- Returns `RESULT_OPERATION_FAILED` if error retrieving entity state

### GetEntitiesStates Service

The `GetEntitiesStates` service fetches the states (pose, twist, acceleration) in the world frame of multiple entities in the simulation.

Get states for all entities in the simulation:

```bash
ros2 service call /get_entities_states simulation_interfaces/srv/GetEntitiesStates "{filters: {filter: ''}}"
```

Get states for entities containing 'robot' in their path:

```bash
ros2 service call /get_entities_states simulation_interfaces/srv/GetEntitiesStates "{filters: {filter: 'robot'}}"
```

Get states for entities with paths starting with '/World':

```bash
ros2 service call /get_entities_states simulation_interfaces/srv/GetEntitiesStates "{filters: {filter: '^/World'}}"
```

**Notes:**
- Combines functionality from `GetEntities` and `GetEntityState` services
- Filters entities first using regex pattern matching
- Retrieves state for each filtered entity
- Returns list of entity paths and corresponding states
- For entities with RigidBodyAPI, both pose and velocities will be returned
- For entities without RigidBodyAPI, only pose will be returned with zero velocities
- Acceleration values are always reported as zero (not provided by the current API)
- Using this service is more efficient than making multiple `GetEntityState` calls when you need states for many entities
- Returns `RESULT_OK` if successfully retrieved entity states
- Returns `RESULT_OPERATION_FAILED` if error in filtering or retrieving states

### DeleteEntity Service

The `DeleteEntity` service deletes a specified entity in the simulation.

```bash
ros2 service call /delete_entity simulation_interfaces/srv/DeleteEntity "{entity: '/World/robot'}"
```

**Notes:**
- The service will return `RESULT_OK` if the entity was successfully deleted
- Returns `RESULT_OPERATION_FAILED` if the entity is protected and cannot be deleted
- Uses `prim_utils.is_prim_no_delete()` to check if a prim can be deleted before attempting deletion

### SpawnEntity Service

The `SpawnEntity` service spawns a new entity into the simulation at a specified location.

Basic entity spawn with default position:

```bash
ros2 service call /spawn_entity simulation_interfaces/srv/SpawnEntity "{name: 'MyEntity', allow_renaming: false, uri: '/path/to/model.usd'}"
```

Spawn with specific position and orientation:

```bash
ros2 service call /spawn_entity simulation_interfaces/srv/SpawnEntity "{name: 'PositionedEntity', allow_renaming: false, uri: '/path/to/model.usd', initial_pose: {pose: {position: {x: 1.0, y: 2.0, z: 3.0}, orientation: {w: 1.0, x: 0.0, y: 0.0, z: 0.0}}}}"
```

Empty Xform creation (no URI):

```bash
ros2 service call /spawn_entity simulation_interfaces/srv/SpawnEntity "{name: 'EmptyXform', allow_renaming: false, uri: ''}"
```

With auto-renaming enabled:

```bash
ros2 service call /spawn_entity simulation_interfaces/srv/SpawnEntity "{name: 'AutoRenamedEntity', allow_renaming: true, uri: '/path/to/model.usd'}"
```

With namespace specified:

```bash
ros2 service call /spawn_entity simulation_interfaces/srv/SpawnEntity "{name: 'NamespacedEntity', allow_renaming: false, uri: '/path/to/model.usd', entity_namespace: 'robot1'}"
```

**Notes:**
- If URI is provided, loads the USD file as a reference in the given prim path
- If URI is not provided, creates a Xform at the given prim path
- All spawned prims are marked with a `simulationInterfacesSpawned` attribute for tracking
- Returns `RESULT_OK` if the entity was successfully spawned
- Returns `NAME_NOT_UNIQUE (101)` if the entity name already exists and `allow_renaming` is false
- Returns `NAME_INVALID (102)` if the entity name is empty and `allow_renaming` is false
- Returns `RESOURCE_PARSE_ERROR (106)` if failed to parse or load USD file

### ResetSimulation Service

The `ResetSimulation` service resets the simulation environment to its initial state.

```bash
ros2 service call /reset_simulation simulation_interfaces/srv/ResetSimulation
```

**Notes:**
- Stops the simulation timeline
- Finds and removes all prims with `simulationInterfacesSpawned` attribute
- Uses multiple passes to ensure all spawned entities are removed
- Restarts the simulation timeline
- Returns `RESULT_OK` if successfully reset
- Returns `RESULT_OPERATION_FAILED` if error resetting simulation

### SetEntityState Service

The `SetEntityState` service sets the state (pose, twist) of a specific entity in the simulation. Only transforms in the world frame are currently accepted.

Set only position and orientation:

```bash
ros2 service call /set_entity_state simulation_interfaces/srv/SetEntityState "{
  entity: '/World/Cube',
  state: {
    header: {frame_id: 'world'},
    pose: {
      position: {x: 1.0, y: 2.0, z: 3.0},
      orientation: {w: 1.0, x: 0.0, y: 0.0, z: 0.0}
    },
    twist: {
      linear: {x: 0.0, y: 0.0, z: 0.0},
      angular: {x: 0.0, y: 0.0, z: 0.0}
    }
  }
}"
```

Set position, orientation and velocity (for entities with rigid body physics):

```bash
ros2 service call /set_entity_state simulation_interfaces/srv/SetEntityState "{
  entity: '/World/RigidBody',
  state: {
    header: {frame_id: 'world'},
    pose: {
      position: {x: 1.0, y: 2.0, z: 3.0},
      orientation: {w: 1.0, x: 0.0, y: 0.0, z: 0.0}
    },
    twist: {
      linear: {x: 0.5, y: 0.0, z: 0.0},
      angular: {x: 0.0, y: 0.0, z: 0.1}
    }
  }
}"
```

**Notes:**
- The position and orientation are always updated for any entity
- Velocities are only set for entities with a RigidBodyAPI
- For non-rigid bodies, only position and orientation will be set (velocity settings are ignored)
- Acceleration settings are not currently supported and will be ignored
- Returns `RESULT_OK` if successfully set entity state
- Returns `RESULT_NOT_FOUND` if entity does not exist
- Returns `RESULT_OPERATION_FAILED` if error setting entity state

### StepSimulation Service

The `StepSimulation` service simulates a finite number of steps and returns to PAUSED state.

Step the simulation by 1 frame (note: will use 2 steps internally):

```bash
ros2 service call /step_simulation simulation_interfaces/srv/StepSimulation "{steps: 1}"
```

Step the simulation by 10 frames:

```bash
ros2 service call /step_simulation simulation_interfaces/srv/StepSimulation "{steps: 10}"
```

Step the simulation by 100 frames:

```bash
ros2 service call /step_simulation simulation_interfaces/srv/StepSimulation "{steps: 100}"
```

**Notes:**
- The simulation must be in a paused state before stepping can be performed
- The service call will block until all steps are completed
- After stepping completes, the simulation will automatically return to a paused state
- Returns `RESULT_OK` if stepping completed successfully
- Returns `RESULT_INCORRECT_STATE` if the simulation is not paused when the service is called
- Returns `RESULT_OPERATION_FAILED` if any error occurs during stepping

### LoadWorld Service

The `LoadWorld` service loads a world or environment file into the simulation, clearing the current scene and setting the simulation to stopped state. Currently supports USD format worlds.

Load a world from a USD file:

```bash
ros2 service call /load_world simulation_interfaces/srv/LoadWorld "{uri: '/path/to/world.usd'}"
```

Load a sample world with Isaac Sim sample environments:

```bash
ros2 service call /load_world simulation_interfaces/srv/LoadWorld "{uri: 'https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/5.1/Isaac/Environments/Simple_Room/simple_room.usd'}"
```

Load a sample world with a ROS2 scenario:

```bash
ros2 service call /load_world simulation_interfaces/srv/LoadWorld "{uri: 'https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/5.1/Isaac/Samples/ROS2/Scenario/carter_warehouse_apriltags_worker.usd'}"
```

**Notes:**
- Only USD files (.usd, .usda, .usdc, .usdz) are supported
- The simulation must be stopped or paused before loading a world (not playing)
- Loading a world will clear the current scene and create a new stage from the USD file
- If the given path cannot be found directly, Isaac Sim will automatically try prefixing it with the default asset root path
- Returns `RESULT_OK` if the world was successfully loaded
- Returns `UNSUPPORTED_FORMAT` if the file format is not supported
- Returns `RESOURCE_PARSE_ERROR` if the USD file cannot be parsed or loaded
- Returns `RESULT_OPERATION_FAILED` if the simulation is playing when the service is called

### UnloadWorld Service

The `UnloadWorld` service unloads the current world from the simulation, clearing the current scene and creating a new empty stage. Any previously spawned entities will be removed.

```bash
ros2 service call /unload_world simulation_interfaces/srv/UnloadWorld
```

**Notes:**
- The simulation must be stopped or paused before unloading a world (not playing)
- Creates a new empty stage after unloading the current world
- Returns `RESULT_OK` if the world was successfully unloaded
- Returns `NO_WORLD_LOADED` if no world is currently loaded
- Returns `RESULT_OPERATION_FAILED` if the simulation is playing when the service is called

### GetCurrentWorld Service

The `GetCurrentWorld` service returns information about the currently loaded world, including its URI, name, and format.

```bash
ros2 service call /get_current_world simulation_interfaces/srv/GetCurrentWorld
```

**Notes:**
- Returns world information including URI and name if a world is loaded from a file
- For worlds created in memory (new stage), returns empty URI and "untitled_world" as the name
- Returns `RESULT_OK` with world information if successful
- Returns `NO_WORLD_LOADED` if no world is currently loaded

### GetAvailableWorlds Service

The `GetAvailableWorlds` service returns a list of available world files that can be loaded into the simulation. It searches default Isaac Sim paths for USD world files, with support for TagsFilter-based filtering.

Get all default available worlds:

```bash
ros2 service call /get_available_worlds simulation_interfaces/srv/GetAvailableWorlds
```

Get worlds with tag filtering (search for default worlds with specific tags in filename):

```bash
ros2 service call /get_available_worlds simulation_interfaces/srv/GetAvailableWorlds "{filter: {tags: ['warehouse', 'carter']}, continue_on_error: true}"
```

Search additional custom paths:

```bash
ros2 service call /get_available_worlds simulation_interfaces/srv/GetAvailableWorlds "{additional_sources: ['/custom/worlds/path'], continue_on_error: true}"
```

Offline-only search with additional local sources:

```bash
ros2 service call /get_available_worlds simulation_interfaces/srv/GetAvailableWorlds "{additional_sources: ['/home/user/custom_worlds', '/opt/isaac_worlds'], offline_only: true, continue_on_error: true}"
```

**Notes:**
- Searches default Isaac Sim paths: `/Isaac/Environments` and `/Isaac/Samples/ROS2/Scenario`
- Supports TagsFilter with `FILTER_MODE_ANY` (default) or `FILTER_MODE_ALL` for tag matching
- Can search additional custom paths specified in `additional_sources`
- Set `offline_only: true` to only search local filesystem paths
- Set `continue_on_error: true` to continue searching even if some paths fail
- Returns `RESULT_OK` with list of available worlds
- Returns `DEFAULT_SOURCES_FAILED` if default asset paths are not accessible and no additional sources are provided

---

## Using the ROS 2 Simulation Control Actions

### SimulateSteps Action

The `SimulateSteps` action simulates a finite number of steps and returns to PAUSED state with feedback after each step.

Basic usage - Step the simulation by 10 frames:

```bash
ros2 action send_goal /simulate_steps simulation_interfaces/action/SimulateSteps "{steps: 10}"
```

With feedback - Step the simulation by 20 frames and show feedback:

```bash
ros2 action send_goal /simulate_steps simulation_interfaces/action/SimulateSteps "{steps: 20}" --feedback
```

**Notes:**
- The simulation must be in a paused state before stepping can be performed
- After steps are completed, the simulation will return to a paused state
- You will receive feedback after each step showing completed and remaining steps
- The action can be canceled while executing

---

## Technical Details

The extension uses the `omni.timeline` interface to control the simulation state and provides a clean ROS 2 interface through standard services. The implementation includes:

- A singleton `ROS2ServiceManager` to handle all ROS 2 services through a single node
- A `SimulationControl` class that interfaces with Isaac Sim's timeline
- Thread-safe implementation for ROS 2 spinning independent of Action Graph interface

---

## Extending

To add more simulation control services, extend the `SimulationControl` class and register additional services with the `ROS2ServiceManager`.

---

## Summary

This page covered:

- The ROS 2 Simulation Control extension and its capabilities
- How to enable the extension in Isaac Sim
- Using ROS 2 services to control simulation state (play, pause, stop)
- Manipulating entities in the simulation (spawn, delete, get/set state, get info)
- Managing simulation worlds (load, unload, query available worlds)
- Using ROS 2 actions for simulation stepping with feedback
- Technical implementation details of the extension
