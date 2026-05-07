import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    IncludeLaunchDescription,
    TimerAction,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from moveit_configs_utils import MoveItConfigsBuilder

package_path = get_package_share_directory("robot_moveit_config")
inverse_ki_package_path = get_package_share_directory("inverse_ki")
urdf_path = os.path.join(package_path, "config", "robot_arm.urdf.xacro")
moveit_py_config_path = os.path.join(
    inverse_ki_package_path, "motion_planning_config.yaml"
)

def generate_launch_description():
   
    moveit_config = (
        MoveItConfigsBuilder(
            robot_name="robot_arm",             
            package_name="robot_moveit_config"  
            )
        .robot_description(file_path=urdf_path)
        .trajectory_execution(
            file_path=os.path.join(package_path, "config", "moveit_controllers.yaml")
        )
        .moveit_cpp(
            file_path=moveit_py_config_path
        )
        .to_moveit_configs())
    
    example_file = DeclareLaunchArgument(
        "example_file",
        default_value="motion_planning",
        description="Motion Planning with python API",
    )

    moveit_py_node = Node(
        name="motion_planning",
        package="inverse_ki",
        executable=LaunchConfiguration("example_file"),
        output="both",
        parameters=[moveit_config.to_dict()],
    )
    delayed_moveit_py_node = TimerAction(period=3.0, actions=[moveit_py_node])

    rviz_config_file = os.path.join(
       package_path,
        "config",
        "moveit.rviz",
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        output="log",
        arguments=["-d",rviz_config_file],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
        ],
    )

    move_group_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(package_path, "launch", "move_group.launch.py")
        )
    )

    static_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="static_transform_publisher",
        output="log",
        arguments=["--frame-id", "world", "--child-frame-id", "base_link"],
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="log",
        parameters=[moveit_config.robot_description],
    )

    ros2_controllers_path = os.path.join(package_path, "config", "ros2_controllers.yaml")
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
        "arm_controller",
        "joint_state_broadcaster",
    ]:
        load_controllers.append(
            ExecuteProcess(
                cmd=["ros2 run controller_manager spawner {}".format(controller)],
                shell=True,
                output="log",
            )
        )

    return LaunchDescription(
        [
            example_file,
            delayed_moveit_py_node,
            move_group_launch,
            robot_state_publisher,
            ros2_control_node,
            rviz_node,
            static_tf,
        ]
        + load_controllers
    )
