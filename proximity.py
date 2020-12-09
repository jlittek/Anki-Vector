import anki_vector
from anki_vector.util import distance_mm, Distance, speed_mmps

with anki_vector.Robot() as robot:
	robot.motors.set_wheel_motors(50,50)
	while True:
		proximity_data = robot.proximity.last_sensor_reading
		print('Proximity distance: {0}'.format(proximity_data.distance))
		if proximity_data.distance.distance_mm < 40:
			robot.motors.stop_all_motors()
			
	