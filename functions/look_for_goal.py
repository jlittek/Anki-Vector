import time
import anki_vector
from anki_vector.events import Events
from anki_vector.util import degrees, distance_mm, Pose, Angle

def handle_object_observed(robot, event_type, event):
    # This will be called whenever an EvtObjectObserved is dispatched -
    # whenever an Object comes into view. In case it is the CustomMarker 
    # used to mark the goal the observed position of the marker becomes the new goal position.
    robot.motors.stop_all_motors()
    print("Object observed")
    for obj in robot.world.visible_custom_objects:
        print(obj.archetype)
        if obj.archtype == anki_vector.objects.CustomObjectTypes.CustomType00:
            robot.goal_pose = obj.pose

# initialize the robot and the goal marker:
robot = anki_vector.Robot()
robot.connect()
robot.behavior.set_lift_height(0.0)
robot.behavior.set_head_angle(degrees(20.0))
robot.events.subscribe(handle_object_observed, Events.object_observed)
robot.enable_custom_object_detection = True
goal = robot.world.define_custom_wall(anki_vector.objects.CustomObjectTypes.CustomType00, anki_vector.objects.CustomObjectMarkers.Triangles5, width_mm=200.0, height_mm=300.0, marker_width_mm=170.0, marker_height_mm=170.0)
print(goal)
print(goal.custom_type==anki_vector.objects.CustomObjectTypes.CustomType00)
robot.goal_pose = None

# wait for the robot to see the marker:
while robot.goal_pose == None:
    pass

# try to reach the goal:
success = robot.behavior.go_to_pose(robot.goal_pose, relative_to_robot=True, num_retries=0)
print(success)

print("Stop")
robot.behavior.say_text("I'm there!")
