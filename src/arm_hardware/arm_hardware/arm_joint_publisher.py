import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from sensor_msgs.msg import JointState
from st3215.st3215 import ST3215
import math, time

class ArmJointPublisherNode(Node):
    def __init__(self):
        super().__init__("arm_joint_publisher")
        self.publisher = self.create_publisher(JointState, "joint_states",10)
        self.add_post_set_parameters_callback(self.parameters_callback)
        
        # Setting up parameters
        self.declare_parameter("port","/dev/ttyACM0")
        self.declare_parameter("frequency", 50)
        self.port = self.get_parameter("port").value
        self.frequency = 1 / self.get_parameter("frequency").value

        # Setting up servo motors
        self.servo = ST3215(self.port)
        self.current_joint_names = [""]*6
        self.current_joint_positions = [0.0]*6
        self.current_joint_velocities = [0.0]*6
        self.joint_state_timer = self.create_timer(self.frequency,self.publish_joint_states)
        self.ids = self.servo.ListServos()
        self.get_logger().info(f"Current Servos: {self.ids}")

        # Setting up conversions
        self.pos_to_deg = 360/4095.0
        self.deg_to_rad = math.pi/180.0

    def publish_joint_states(self):
        msg = JointState()

        for id, joint in enumerate(self.ids):
            position = self.servo.ReadPosition(joint)
            speed, comm, error = self.servo.ReadSpeed(joint)

            if position is None or speed is None:
                self.get_logger().warn(f'Failed to read joint_{joint}')
                continue

            self.current_joint_names[id] = "Joint_" + str(joint)
            self.current_joint_positions[id] = (position- 2048) * self.pos_to_deg * self.deg_to_rad
            self.current_joint_velocities[id] = speed
            
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.current_joint_names[0:5]
        msg.position = self.current_joint_positions[0:5]
        msg.velocity = self.current_joint_velocities[0:5]
        self.publisher.publish(msg)
    
    def parameters_callback(self, params:list[Parameter]):
        for param in params:
            if param.name == "port":
                self.port = param.value
            elif param.name == "frequency":
                self.frequency = param.value

def main(args=None):
    rclpy.init(args=args)
    node = ArmJointPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()