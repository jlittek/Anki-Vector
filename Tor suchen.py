import anki_vector
from anki_vector.util import degrees, distance_mm

robot = anki_vector.Robot()
robot.connect()
robot.behavior.set_head_angle(degrees(0))

while robot.world.connected_light_cube == None:
    print("connecting to cube...")
    robot.world.connect_cube()
print("connected")
cube = robot.world.connected_light_cube
print(cube.pose)
while cube.pose == None:
    robot.motors.set_wheel_motors(-20, 20)
robot.motors.set_wheel_motors(0, 0)
robot.behavior.go_to_object(cube, distance_from_object=distance_mm(70), num_retries=0)
print("Stop")

