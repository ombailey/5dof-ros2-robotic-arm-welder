cmake_minimum_required(VERSION 3.8)
project(arm_moveit_motion_planning)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(rclcpp REQUIRED)
add_executable( joint_space_planning src/joint_space_planning.cpp )
ament_target_dependencies(joint_space_planning rclcpp std_msgs moveit_ros_planning_interface)
install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})
install(TARGETS joint_space_planning RUNTIME DESTINATION lib/${PROJECT_NAME} )

ament_package()
