import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from st3215.st3215 import ST3215

class CenterArmJointsNode(Node):
    def __init__(self):
        super().__init__("center_arm_joints")
        self.add_post_set_parameters_callback(self.parameters_callback)
        self.declare_parameter("joints", [1,2,3,4,5,6])
        self.declare_parameter("port", "/dev/ttyACM0")

        self.joints = self.get_parameter("joints").value
        self.port = self.get_parameter("port").value
        self.servo = ST3215(self.port)

        for joint in self.joints:
            self.servo.DefineMiddle(joint)
            self.get_logger().info(f'Joint_{joint}:{self.servo.ReadPosition(joint)}')

    def parameters_callback(self, params: list[Parameter]):
        for param in params:
            if param.name == "joints":
                self.joints = param.value
            elif param.name == "port":
                self.port = param.value

def main(args=None):
    rclpy.init(args=args)
    node = CenterArmJointsNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()