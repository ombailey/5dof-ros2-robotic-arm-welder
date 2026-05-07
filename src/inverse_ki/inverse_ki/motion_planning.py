import rclpy
from moveit.planning import MoveItPy
from geometry_msgs.msg import PoseStamped
from rclpy.logging import get_logger
import time

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

    # execute the plan
    if plan_result:
        logger.info("Executing plan")
        robot_trajectory = plan_result.trajectory
        robot.execute(robot_trajectory, controllers=["arm_controller"])
    else:
        logger.error("Planning failed")

    time.sleep(sleep_time)

def main():
    rclpy.init()
    logger = get_logger("moveit_py.pose_goal")
    # Give ros2_control and controllers a moment to come up when launched together.
    time.sleep(1.0)
    robot = MoveItPy(node_name="moveit_py")
    robot_arm = robot.get_planning_component("arm")
    logger.info("MoveItPy instance created")

    robot_arm.set_start_state_to_current_state()
    # Move to Starting Point
    pose_goal = PoseStamped()
    pose_goal.header.frame_id="base_link"
    pose_goal.pose.orientation.w = 1.0
    pose_goal.pose.position.x = 0.0
    pose_goal.pose.position.y = 0.0
    pose_goal.pose.position.z = 0.1
    robot_arm.set_goal_state(pose_stamped_msg=pose_goal, pose_link="End_Effector")
    plan_and_execute(robot,robot_arm,logger,sleep_time=3.0)

if __name__ == "__main__":
    main()
