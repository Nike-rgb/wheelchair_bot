import rclpy
from rclpy.node import Node
import getch

from geometry_msgs.msg import Twist


class Teleop(Node):

    def __init__(self):
        super().__init__('arrow_keys_teleop')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel_keyboard', 10)

    def read_keystroke(self):
        twist = Twist()
        
        while True:
            twist.linear.x = twist.linear.y = twist.angular.z = 0.0
            key = getch.getch()
            if key == 'w':
                twist.linear.x = 0.5
            elif key == 's':
                twist.linear.x = -0.5
            elif key == 'd':
                twist.angular.z = -0.5
            elif key == 'a':
                twist.angular.z = 0.5
            else:
                twist.linear.x = twist.linear.y = twist.angular.z = 0.0
            self.publisher_.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    print("Drive your bot using keys W, A, S, D. Run ros2 topic echo /cmd_vel to output the twist messages")
    teleop = Teleop()
    teleop.read_keystroke()

    rclpy.spin(teleop)

if __name__ == '__main__':
    main()