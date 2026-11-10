# 5DOF Robotic Arm Welder (ROS2)

## Overview
As part of our senior capstone project, we were tasked with designing and developing a 5-DOF robotic manipulator capable of executing both linear and curved welding trajectories. 
This ROS 2 workspace implements the manipulator's control and motion-planning pipeline for linear welding trajectories, using MoveIt 2 for trajectory planning and execution,
specifically Cartesian and Joint Space planning.

## Features
- ROS2 control of Feetech STS3215 Motors.
- Joint Space Planning
- Cartesian Space Planning
- Gazebo Simulation

## Software Used
- ROS2
- MoveIt2
- Python
- Ubuntu

## How to Run
colcon build <br>
source install/setup.bash <br>
ros2 launch robot_arm_model_moveit demo.launch.py <br>
ros2 run forward_ki motion_planning.py 
