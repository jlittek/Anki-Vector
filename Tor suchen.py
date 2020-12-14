import time
import anki_vector
from anki_vector.events import Events
from anki_vector.util import degrees, distance_mm, Pose, Angle

def handle_object_observed(robot, event_type, event):
    # This will be called whenever an EvtObjectObserved is dispatched -
    # whenever an Object comes into view.
    #print(f"--------- Vector observed an object --------- \n{event.obj}")
    robot.motors.stop_all_motors()
    for obj in robot.world.visible_custom_objects:
        print("Object observed")
        robot.Tor_pose = obj.pose
        break # nach dem ersten direkt aufhören



robot = anki_vector.Robot()
robot.connect()
robot.behavior.set_lift_height(0.0)
robot.behavior.set_head_angle(degrees(10.0))
robot.events.subscribe(handle_object_observed, Events.object_observed)
robot.enable_custom_object_detection=True
robot.world.define_custom_wall(anki_vector.objects.CustomObjectTypes.CustomType00, anki_vector.objects.CustomObjectMarkers.Triangles5, width_mm=100.0, height_mm=50.0, marker_width_mm=100.0, marker_height_mm=100.0)
robot.Tor_pose = None
while robot.Tor_pose == None:
    pass
robot.events.unsubscribe(handle_object_observed, Events.object_observed)
p = Pose(x=robot.Tor_pose.position.x-100, y=0, z=0, angle_z=Angle(degrees=0))
# aufgeteilt nach x und y, sonst gibt es immer eine Fehlermeldung:
success = robot.behavior.go_to_pose(p, relative_to_robot=True, num_retries=0)
print(success)
print(p)
p = Pose(x=0, y=robot.Tor_pose.position.y, z=0, angle_z=Angle(degrees=0))
success = robot.behavior.go_to_pose(p, relative_to_robot=True, num_retries=0)
print(success)
print(p)
print("Stop")
