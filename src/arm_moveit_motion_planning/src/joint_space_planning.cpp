#include <moveit/move_group_interface/move_group_interface.h>

int main(int argc, char** argv){
    rclcpp::init(argc,argv);
    moveit::planning_interface::MoveGroupInterface::Plan my_plan;
    auto node = rclcpp::Node::make_shared("JointSpacePlanning");
    moveit::planning_interface::MoveGroupInterface move_group(node,"arm_group");
    std::vector<double> des_joint_pos = {0.0, 0.7, 0.5, 0.0, 0.3 };

    bool in_workspace = move_group.setJointValueTarget(des_joint_pos);
    bool success = (move_group.plan(my_plan) == moveit::core::MoveItErrorCode::SUCCESS);
    if (success) move_group.move();
}   