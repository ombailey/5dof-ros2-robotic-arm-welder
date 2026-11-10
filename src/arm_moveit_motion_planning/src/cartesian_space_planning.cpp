#include <moveit/move_group_interface/move_group_interface.hpp>
#include <moveit/planning_scene_interface/planning_scene_interface.hpp>
#include <moveit/robot_trajectory/robot_trajectory.hpp>
#include <moveit/trajectory_processing/time_optimal_trajectory_generation.hpp>
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "tf2/exceptions.hpp"
#include "tf2_ros/transform_listener.hpp"
#include "tf2_ros/buffer.hpp"

class CartesianPlanning: public rclcpp::Node{

    public:
    CartesianPlanning(): Node("cartesian_planning"){}
    void run();
    void plan();

    private:
    rclcpp::Node::SharedPtr _node;
};

void CartesianPlanning::plan(){
    bool tf_found = false;
    geometry_msgs::msg::TransformStamped t;

    auto tf_buffer {std::make_unique<tf2_ros::Buffer>(this->get_clock())};
    auto tf_listener { std::make_shared<tf2_ros::TransformListener>(*tf_buffer)};

    moveit::planning_interface::MoveGroupInterface move_group(_node,"arm_group");
    std::string fromFrameRel = move_group.getPlanningFrame().c_str();
    std::string toFrameRel = move_group.getEndEffectorLink().c_str();

    while ( !tf_found ) {    
        try {
            t = tf_buffer->lookupTransform(fromFrameRel, toFrameRel, tf2::TimePointZero);
            tf_found = true;
        } catch (const tf2::TransformException & ex) {
            RCLCPP_INFO(this->get_logger(), "Could not transform %s to %s: %s Try again",toFrameRel.c_str(), fromFrameRel.c_str(), ex.what());
            sleep(1);
        }
    }

    geometry_msgs::msg::Pose target_pose;
    std::vector<geometry_msgs::msg::Pose> waypoints;
    // target_pose.orientation.w = t.transform.rotation.w; target_pose.orientation.x = t.transform.rotation.x; target_pose.orientation.y = t.transform.rotation.y;
    // target_pose.orientation.z = t.transform.rotation.z; target_pose.position.x = t.transform.translation.x; target_pose.position.y = t.transform.translation.y;
    // target_pose.position.z = t.transform.translation.z;
    // waypoints.push_back(target_pose);
    target_pose.position.x -= 0.04;
    waypoints.push_back(target_pose);
    // target_pose.position.x -= 0.06;
    // waypoints.push_back(target_pose);

    moveit_msgs::msg::RobotTrajectory traj;
    const double step = 0.001;
    double fraction = move_group.computeCartesianPath(waypoints,step,traj);
    if (fraction > 0.7)
        {
            robot_trajectory::RobotTrajectory rt(
                move_group.getCurrentState()->getRobotModel(),
                "arm_group"
            );

            rt.setRobotTrajectoryMsg(
                *move_group.getCurrentState(),
                traj
            );

            trajectory_processing::TimeOptimalTrajectoryGeneration time_param;

            if (time_param.computeTimeStamps(rt))
            {
                rt.getRobotTrajectoryMsg(traj);
                move_group.execute(traj);
            }
        }
        else
        {
            RCLCPP_ERROR(
                rclcpp::get_logger("moveit_executor"),
                "Trajectory calculation failed"
            );
        }
};

void CartesianPlanning::run(){
    auto node = rclcpp::Node::make_shared("CartesianPlan");
    _node = node;
    std::thread cartesian_plan_t(&CartesianPlanning::plan, this);
    rclcpp::spin(node);
}

int main(int argc, char* argv[]){
    rclcpp::init(argc,argv);
    CartesianPlanning cp;
    cp.run();
}
