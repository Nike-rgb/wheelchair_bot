from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    #for ros2 run controller_manager spawner.py diff_cont
    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner.py",
        arguments = ["diff_cont"]
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner.py",
        arguments=['joint_broad']
    )

    twist_mux_starter = Node(
        package="twist_mux",
        executable="twist_mux",
        arguments = ['--ros-args', '--params-file', './src/wheelchair_bot/config/twist_mux.yaml',
         '-r','cmd_vel_out:=/diff_cont/cmd_vel_unstamped']
    )

    slam_toolbox_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('slam_toolbox'), 'launch', 'online_async_launch.py')]),
        launch_arguments={
            'params_file': './src/wheelchair_bot/config/mapper_params_online_async.yaml',
            'use_sim_time': 'true'
        }.items()
    )

    return LaunchDescription([
        diff_drive_spawner,
        joint_broad_spawner,
        twist_mux_starter,
        slam_toolbox_launch
    ])