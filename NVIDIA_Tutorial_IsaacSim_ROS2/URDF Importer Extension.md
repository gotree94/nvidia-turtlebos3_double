# URDF Importer Extension

> **Note**
> Starting from the Isaac Sim 2023.1.0 release, the URDF importer has been open-sourced. Source code and information for contributing can be found at our [Github repository](https://github.com/NVIDIA-Omniverse/IsaacSim). As of Isaac Sim 5.0, the former dedicated repository has been deprecated, and the code has been moved to the Isaac Sim repository.

The URDF Importer Extension is used to import URDF representations of robots. Unified Robot Description Format (URDF), is an XML format for representing a robot model in ROS.

To Import URDF files, go to the top menu bar and click **File > Import**.

This extension is enabled by default. If it is ever disabled, it can be re-enabled from the Extension Manager by searching for `isaacsim.asset.importer.urdf`.

---

## Overview of URDF Importer Extension

Import results are logged in the **Output Log**, accessible from the bottom of the screen. The Output Log will display any errors or warnings that occur during the import process. For more detailed log information, open Isaac Sim's log file, change the console to Info mode, or start Isaac Sim with the parameter `--verbose` to display results in the terminal output.

> **Note**
> The Imported model follows the [Isaac Sim Asset Structure](https://docs.omniverse.nvidia.com/isaacsim/latest/reference/asset_structure.html) convention, and the meshes are already instantiable to optimize performance.

---

## Conventions

> **Note**
> To comply with USD prim name conventions, special characters in link, joint, mesh names, and all other reference asset filenames are not supported and will be replaced with an underscore. In the event that the name starts with an underscore due to the replacement, an `a` is pre-pended. It is recommended to make these name changes in the URDF directly.

Refer to the [Isaac Sim Conventions](https://docs.omniverse.nvidia.com/isaacsim/latest/reference/conventions.html) documentation for a complete list of NVIDIA Isaac Sim conventions.

---

## Import Options

### Model

Provides the Options to Import in Stage, or add as a referenced model. If **Create in Stage** is selected. Choose the options to set as the default prim, and Clear Stage on Import. By default both are left unchecked.

### Links

Choose between a **Moveable base** (for example, a wheeled robot) or a **Static base** (for example, a 6DoF robotic arm). If the robot is a moveable base, the base link will be set to moveable. If the robot is a static base, the base link will be fixed in place with a `root_joint`.

The **Default Density** is used for links that do not have a mass specified in the URDF. If the density is set to 0, the physics engine will automatically compute the density with its default value.

### Joints and Drives

Provides an interface to configure individual joints and is loaded with the default values.

**Ignore Mimic**: If checked, the Mimic tag will be ignored on import. Otherwise joints with the mimic tag will receive the PhysX Mimic API, allowing it to work in tandem with the primary joint that is defined in its setup.

**Joint Configuration**: Choose between configuring the joints directly through stiffness or with natural frequency. Saved values will always be in stiffness.

- **Stiffness**: Edit the joint drive stiffness and damping directly.

  The stiffness value is used to control the strength of the position drive. A combination of setting stiffness and damping on a drive will result in both targets being applied, this can be useful in position control to reduce vibrations.

- **Natural Frequency**: Computes the joint drive stiffness and Damping ratio based on the desired natural frequency using the formula:

  ```
  stiffness = (2 * π * natural_frequency)² * inertia
  damping = 2 * damping_ratio * √(stiffness * inertia)
  ```

  where `natural_frequency` is the natural frequency, `damping_ratio` is the damping ratio, and `inertia` is the total equivalent inertia at the joint. The damping ratio is such that `damping_ratio = 1` is a critically damped system, `damping_ratio < 1` is underdamped, and `damping_ratio > 1` is overdamped.

**Multi-Edit**: To Edit multiple joints at the same time, you can `ctrl+click` at their names, to select individual joints, or `shift+click` to select a range of joints. After selected, the values will be applied to all selected joints.

**Drive Type**: The drive type can be chosen between **Acceleration** and **Force**.
- Acceleration drives normalize the inertia before applying the effort, making it invariant to changes in robot mass (payload not included), equivalent to ideal damped actuator.
- In force drives, the effort is applied directly to the joint, equivalent to a spring-damper system.

**Target**: Can be chosen between **None**, **Position**, and **Velocity**.
- If the drive type is set to position, the target will be the position in radians for revolute joints, or distance units for prismatic.
- For velocity drives, it's the unit per second.
- When the joint is configured as Mimic you cannot change the Target Type.

### Colliders

**Collision From Visuals**: If checked, the collision objects will be created from the visual meshes when a collision object is not provided. Otherwise, no collision will be created for that link.

**Collider Type**: Select between:
- **Convex Hull** will create a single convex hull around the collision mesh.
- **Convex Decomposition** will create multiple convex hulls around the collision mesh to better match the visual asset.

**Allow self-collision**: Enables self collision between adjacent links. It may cause instability if the collision meshes are intersecting at the joint.

**Replace Cylinders with Capsules**: When selected, cylinder colliders will be replaced with capsule primitives.

> **Note**
> It is recommended that you set Self Collision to false unless you are certain that links on the robot are not self colliding.

You must have write access to the output directory used for import, it will default to the current open stage, change this as necessary.

---

## Importing URDF from a ROS 2 Node

Enable the extension `isaacsim.ros2.urdf` to enable this feature. This will open a standalone URDF importer UI that allows to define a ROS 2 Node containing a robot description.

To select the appropriate node, type in the name of the node in the Node text box. If changes were made to the import settings, or to the published node hit **Refresh**. If the node name is in

> **Note**
> This feature is only available when the ROS 2 bridge is enabled.

**Interface when Importing from a ROS 2 Node**

For more on how to use the ROS 2 URDF Importer, refer to the [Import from ROS 2 Node Tutorial](https://docs.omniverse.nvidia.com/isaacsim/latest/ros2_tutorials/tutorial_ros2_urdf_import.html).

---

## Robot Properties

There might be many properties you want to tune on your robot. These properties can be spread across many different schemas and APIs.

The general steps of getting and setting a parameter are:

1. Find which API is the parameter under. Most common ones can be found in the Pixar USD API.
2. Get the prim handle that the API is applied to. For example, articulation and drive APIs are applied to joints, and MassAPIs are applied to the rigid bodies.
3. Get the handle to the API. From there on, you can Get or Set the attributes associated with that API.

For example, if you want to set the wheel's drive velocity and the actuators' stiffness, find the DriveAPI:

```python
# get handle to the Drive API for both wheels
left_wheel_drive = UsdPhysics.DriveAPI.Get(stage.GetPrimAtPath("/carter/chassis_link/left_wheel"), "angular")
right_wheel_drive = UsdPhysics.DriveAPI.Get(stage.GetPrimAtPath("/carter/chassis_link/right_wheel"), "angular")

# Set the velocity drive target in degrees/second
left_wheel_drive.GetTargetVelocityAttr().Set(150)
right_wheel_drive.GetTargetVelocityAttr().Set(150)

# Set the drive damping, which controls the strength of the velocity drive
left_wheel_drive.GetDampingAttr().Set(15000)
right_wheel_drive.GetDampingAttr().Set(15000)

# Set the drive stiffness, which controls the strength of the position drive
# In this case because we want to do velocity control this should be set to zero
left_wheel_drive.GetStiffnessAttr().Set(0)
right_wheel_drive.GetStiffnessAttr().Set(0)
```

Alternatively you can use the **Omniverse Commands Tool** Extension to change a value in the UI and get the associated Omniverse command that changes the property.

> **Note**
> - The drive stiffness parameter should be set when using position control on a joint drive.
> - The drive damping parameter should be set when using velocity control on a joint drive.
> - A combination of setting stiffness and damping on a drive will result in both targets being applied, this can be useful in position control to reduce vibrations.

---

## Custom Isaac Sim URDF Attributes and Tags

### `sensor.isaac_sim_config`

This attribute is used in the sensor tag to provide Isaac Sim configuration for Sensors. There are two possible uses:

1. **Preconfigured Lidars** that are shipped with Isaac Sim
2. **User-defined configurations**. When it's used with a user-defined configuration, the location of the configuration JSON must be provided, otherwise provide the configuration name for a preconfigured Lidar. A sample configuration file is provided in the tests provided with the URDF Importer in `data/lidar_sensor_template`.

> **Note**
> When using a custom Lidar configuration, the importer will try to create a symlink to the configuration in the `isaacsim.sensors.rtx` folder. If you get **Error Code: 1314** on Windows try running Isaac Sim with Administrator Privileges, or manually create the Symbolic Link post-import. Alternatively, add the imported asset path into the lookup folders for `isaacsim.sensors.rtx`. If you get **Error Code: 183** on Windows, the symbolic link already exists, double check and replace manually if necessary.

**Example:**

```xml
<robot>
    <link name="root_link"/>
    <joint name="root_to_base" type="fixed">
        <parent link="root_link"/>
        <child link="link_1"/>
    </joint>
    <link name="link_1"/>

    <sensor name="custom_lidar" type="ray" update_rate="30" isaac_sim_config="../lidar_sensor_template/lidar_template.json">
        <parent link="link_1"/>
        <origin xyz="0.5 0.5 0" rpy="0 0 0"/>
    </sensor>

    <sensor name="preconfigured_lidar" type="ray" update_rate="30" isaac_sim_config="Velodyne_VLS128">
        <parent link="link_1"/>
        <origin xyz="0.5 1.5 0" rpy="0 0 0"/>
    </sensor>
</robot>
```

### `loop_joint`

Defines a joint to close kinematic chain loops. This is useful for robots with closed kinematic chains, such as a quadruped robot with a loop joint at the hip. The loop joint is defined in the URDF as follows:

```xml
<loop_joint name="loop_joint_name" type="spherical">
    <link1 link="link_1" rpy="0 0 0" xyz="0 0 0"/>
    <link1 link="link_2" rpy="0 0 0" xyz="0 0 0"/>
</loop_joint>
```

### `fixed_frame`

Fixed frames are used to define a reference point attached to a link. This is useful to define reference points (for example, sensor placements or end-effector offset) without using the link tag. The fixed frame is defined in the URDF as follows:

```xml
<fixed_frame name="frame_0">
    <parent link="link_1"/>
    <origin rpy="0.0 0.0 0.0" xyz="1.00 -0.020 0.10"/>
</fixed_frame>
```

Fixed frames must have an exclusive name and parent link pair.

---

## References

- Refer to the [Asset Structure](https://docs.omniverse.nvidia.com/isaacsim/latest/reference/asset_structure.html) for more information about the asset structure.

## Examples

- For usage examples, refer to the [Tutorial: Import URDF](https://docs.omniverse.nvidia.com/isaacsim/latest/ros2_tutorials/tutorial_ros2_urdf_import.html).
