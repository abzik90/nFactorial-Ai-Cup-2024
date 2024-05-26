from robolink import *
from robodk import *

# Initialize the RoboDK API
RDK = Robolink()

# Get the robot item (KUKA KR 10 R1420)
robot = RDK.Item('KUKA KR 10 R1420')

# Get the home and target reference points
home = RDK.Item('Home')
target = RDK.Item('Target 1')

# Get the pose of the target (4x4 matrix)
poseref = target.Pose()

# Move the robot to home, then to the target
robot.MoveJ(home)
robot.MoveJ(target)

# Parameters for the triangular prism
tri_base_length = 100  # Length of the base of the triangle
tri_base_width = 50    # Height of the base of the triangle
tri_height = 100       # Height of the prism

# Function to move the robot to the specified pose
def move_to_pose(x, y, z):
    pose = poseref * transl(x, y, z)
    robot.MoveL(pose)

# Draw the base of the triangular prism
move_to_pose(0, 0, 0)
move_to_pose(tri_base_length, 0, 0)
move_to_pose(tri_base_length / 2, tri_base_width, 0)
move_to_pose(0, 0, 0)

# Draw the vertical edges of the prism
move_to_pose(0, 0, tri_height)
move_to_pose(tri_base_length, 0, tri_height)
move_to_pose(tri_base_length / 2, tri_base_width, tri_height)
move_to_pose(0, 0, tri_height)

# Draw the top of the triangular prism
move_to_pose(tri_base_length, 0, tri_height)
move_to_pose(tri_base_length / 2, tri_base_width, tri_height)
move_to_pose(0, 0, tri_height)

# Draw the vertical edges between the top and bottom
move_to_pose(tri_base_length, 0, 0)
move_to_pose(tri_base_length, 0, tri_height)
move_to_pose(tri_base_length / 2, tri_base_width, tri_height)
move_to_pose(tri_base_length / 2, tri_base_width, 0)
move_to_pose(tri_base_length, 0, 0)

# Move the robot back to home
robot.MoveJ(home)