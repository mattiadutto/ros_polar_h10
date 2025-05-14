from setuptools import find_packages, setup

package_name = 'ros2_polar_h10'

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
    maintainer='Mattia Dutto',
    maintainer_email='mattia.dutto@polito.it',
    description='Package for reading Polar H10 data in ROS2.',
    license='TODO',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            f"polar_h10_exe = {package_name}.polar_h10:main"
        ],
    },
)
