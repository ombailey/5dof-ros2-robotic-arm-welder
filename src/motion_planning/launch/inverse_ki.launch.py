"""
A launch file for running the motion planning python api tutorial
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    moveit_config = (
        MoveItConfigsBuilder(
            robot_name="robot_arm", package_name="robot_arm_model_moveit"
        )
        .robot_description(file_path="config/robot_arm_model.urdf.xacro")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .moveit_cpp(
            file_path=get_package_share_directory("motion_planning")
            + "/config/inverse_config.yaml"
        )
        .to_moveit_configs()
    )

    robot_arm_file = DeclareLaunchArgument(
        "robot_arm_file",
        default_value="inverse_kinematics",
        description="Inverse Kinematics",
    )

    moveit_py_node = Node(
        name="moveit_py",
        package="motion_planning",
        executable=LaunchConfiguration("robot_arm_file"),
        output="both",
        parameters=[moveit_config.to_dict()],
    )

    rviz_config_file = os.path.join(
        get_package_share_directory("robot_arm_model"),
        "config",
        "robot_arm_model.rviz",
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
        ],
    )

    # static_tf = Node(
    #     package="tf2_ros",
    #     executable="static_transform_publisher",
    #     name="static_transform_publisher",
    #     output="log",
    #     arguments=["--frame-id", "world", "--child-frame-id", "base_link"],
    # )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="log",
        parameters=[moveit_config.robot_description],
    )

    ros2_controllers_path = os.path.join(
        get_package_share_directory("robot_arm_model_moveit"),
        "config",
        "ros2_controllers.yaml",
    )
    ros2_control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[ros2_controllers_path],
        remappings=[
            ("/controller_manager/robot_description", "/robot_description"),
        ],
        output="log",
    )

    load_controllers = []
    for controller in [
        "arm_group_controller",
        "joint_state_broadcaster",
    ]:
        load_controllers += [
            ExecuteProcess(
                cmd=["ros2 run controller_manager spawner {}".format(controller)],
                shell=True,
                output="log",
            )
        ]

    return LaunchDescription(
        [
            robot_arm_file,
            moveit_py_node,
            robot_state_publisher,
            ros2_control_node,
            rviz_node,
        ]
        + load_controllers
    )
