from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    pkg_path = get_package_share_directory('robot_arm_model')

    urdf_file = os.path.join(pkg_path, 'urdf', 'robot_arm_model.urdf')
    rviz_config = os.path.join(pkg_path, 'config', 'robot_arm_model_config.rviz')

    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_desc}]
        ),

        Node(
            package='arm_hardware',
            executable='arm_joint_publisher'
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config],
            output='screen'
        )
    ])