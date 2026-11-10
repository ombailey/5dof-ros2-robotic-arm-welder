from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
import launch_ros.actions

def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("robot_arm", package_name="robot_arm_model_moveit").to_moveit_configs()
    launch_ros.actions.SetParameter(name='use_sim_time', value=False)
    joint_space_node = Node(
        package="arm_moveit_motion_planning",
        executable="joint_space_planning",
        output="screen",
        parameters=[
            {"use_sim_time": False},
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
        ],

    )

    return LaunchDescription([joint_space_node])