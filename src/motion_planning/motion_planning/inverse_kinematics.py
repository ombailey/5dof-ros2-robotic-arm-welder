import time
import rclpy
from rclpy.logging import get_logger
from moveit.core.robot_state import RobotState
from moveit.planning import MoveItPy
from ament_index_python.packages import get_package_share_directory

def plan_and_execute(
    robot,
    planning_component,
    logger,
    single_plan_parameters=None,
    multi_plan_parameters=None,
    sleep_time=0.0,
):
    """Helper function to plan and execute a motion."""
    # plan to goal
    logger.info("Planning trajectory")
    if multi_plan_parameters is not None:
        plan_result = planning_component.plan(
            multi_plan_parameters=multi_plan_parameters
        )
    elif single_plan_parameters is not None:
        plan_result = planning_component.plan(
            single_plan_parameters=single_plan_parameters
        )
    else:
        plan_result = planning_component.plan()
    logger.info(f'{plan_result}')
    # execute the plan
    if plan_result:
        logger.info("Executing plan")
        robot_trajectory = plan_result.trajectory
        robot.execute(robot_trajectory, controllers=[])
    else:
        logger.error("Planning failed")

    time.sleep(sleep_time)


def main():

    rclpy.init()
    logger = get_logger("moveit_py.pose_goal")

    # instantiate MoveItPy instance and get planning component
    robot = MoveItPy(
        node_name="moveit_py",
        remappings={
            "monitored_planning_scene": "/moveit_cpp/monitored_planning_scene",
            "planning_scene": "/moveit_cpp/publish_planning_scene",
            "attached_collision_object": "/moveit_cpp/planning_scene_monitor",
        },
    )
    robot_arm = robot.get_planning_component("arm_group")
    logger.info("MoveItPy instance created")
    logger.info(f"Group: {robot_arm.planning_group_name}")
    logger.info(f"Start state: {robot_arm.get_start_state()}")
    logger.info(f"Named states: {robot_arm.named_target_states}")

    # set plan start state to current state
    time.sleep(1.0)
    robot_arm.set_start_state_to_current_state()
    # robot_arm.set_goal_state(configuration_name="home")

    # # set pose goal with PoseStamped message
    from geometry_msgs.msg import PoseStamped

    pose_goal = PoseStamped()
    pose_goal.header.frame_id = "base_link"
    pose_goal.pose.position.x = 0.29141
    pose_goal.pose.position.y = -0.0010746
    pose_goal.pose.position.z = 0.21885

    pose_goal.pose.orientation.x = -0.70708
    pose_goal.pose.orientation.y = 0.0098656
    pose_goal.pose.orientation.z = 0.0098092
    pose_goal.pose.orientation.w = 0.707

    goal_state = RobotState(robot.get_robot_model())
    found_ik = goal_state.set_from_ik(
        "arm_group",
        pose_goal.pose,
        "End_Effector",
        1.0,
    )
    if found_ik:
        robot_arm.set_goal_state(robot_state=goal_state)
    else:
        robot_arm.set_goal_state(pose_stamped_msg=pose_goal, pose_link="End_Effector")
    
    # plan to goal
    plan_and_execute(robot, robot_arm, logger, sleep_time=3.0)
    logger.info(f'{goal_state.get_joint_group_positions("arm_group")}')
    ## Goal 2
    pose_goal.pose.position.x = 0.29455
    pose_goal.pose.position.y = -0.0010197
    pose_goal.pose.position.z =  0.33272

    pose_goal.pose.orientation.x = -0.70702
    pose_goal.pose.orientation.y = 0.0097408
    pose_goal.pose.orientation.z = 0.0098275
    pose_goal.pose.orientation.w = 0.70706

    goal_state.set_from_ik(
        "arm_group",
        pose_goal.pose,
        "End_Effector",
        1.0,
    )
    robot_arm.set_goal_state(robot_state=goal_state)
    plan_and_execute(robot, robot_arm, logger, sleep_time=3.0)
    logger.info(f'{goal_state.get_joint_group_positions("arm_group")}')


if __name__ == "__main__":
    main()
