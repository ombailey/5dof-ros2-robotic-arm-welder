from setuptools import find_packages, setup

package_name = 'arm_hardware'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='leek',
    maintainer_email='leek@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "arm_joint_publisher = arm_hardware.arm_joint_publisher:main",
            "center_arm_joints = arm_hardware.center_arm_joints:main"
        ],
    },
)
