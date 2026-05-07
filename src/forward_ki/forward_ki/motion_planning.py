#!/home/leek/venvs/myenv/bin/python

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from st3215.st3215 import ST3215
import math

class MotionPlanningNode(Node):
    def __init__(self):
        super().__init__("motion_planning")
        self.subscriber = self.create_subscription(JointState,"joint_states",self.read_joints,10)
        self.servo = ST3215("/dev/ttyACM0")
        self.ids = self.servo.ListServos()
        self.get_logger().info("Starting Forward Kinematics.")
        self.get_logger().info(f"Current Servos: {self.ids}")

    def read_joints(self,msg:JointState):
        self.last_position = None
        if self.last_position == msg.position:
            return
        self.last_position = msg.position
        # For Motor 6
        msg.position.append(-msg.position[1])
        rad2deg = 180.0/math.pi
        deg2servopos = 4095.0/360.0
        for id,pos in enumerate(msg.position):  
            pos_deg = pos*rad2deg
            if (id == 0 or id == 2 or id ==3):
                servo_pos = int(-pos_deg * deg2servopos) + 2048
            else:
                servo_pos = int(pos_deg * deg2servopos) + 2048
            servo_pos = max(0,min(4095, servo_pos))
            self.get_logger().info(f"{id+1}: {servo_pos}")
            self.servo.MoveTo(id+1,servo_pos)
    
def main(args=None):
    rclpy.init(args=args)
    node = MotionPlanningNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()