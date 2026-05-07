# 5DOF Robotic Arm Welder (ROS2)

## Overview
This project is a ROS2-based control system for a 5DOF robotic arm designed for welding applications.

## Features
- ROS2-based motion control
- Joint Angle Control
- Motor control

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
