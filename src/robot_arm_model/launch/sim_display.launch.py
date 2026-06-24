from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import Command
from launch.actions import ExecuteProcess, SetEnvironmentVariable, IncludeLaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
import os


def generate_launch_description():

    pkg_path = get_package_share_directory('robot_arm_model')

    urdf_file = os.path.join(pkg_path, 'urdf', 'robot_arm_model.urdf.xacro')
    rviz_config = os.path.join(pkg_path, 'config', 'robot_arm_model_config.rviz')

    workspace_path = os.environ.get('COLCON_PREFIX_PATH') or os.environ.get('AMENT_PREFIX_PATH')
    robot_arm_model_descrip = workspace_path + "/robot_arm_model/share"

    return LaunchDescription([

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description': Command(['xacro ', urdf_file]),
                'use_sim_time': True}]
        ),
        
        SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=[robot_arm_model_descrip]),

         # Spawn
        Node(package='ros_gz_sim', executable='create',
            arguments=['-name', 'robot_arm', '-topic', '/robot_description'], output='screen'),
        
        IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            ])
        ),
        launch_arguments={
            'gz_args': f'-r -v4 empty.sdf' 
        }.items()
        ),

        Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model'
        ],
        output='screen'
        ),

        ExecuteProcess(
            cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
            'joint_state_broadcaster'],
            output='screen'),
        
        ExecuteProcess(
            cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
            'arm_group_controller'],
            output='screen'
        ),
    ])