import anki_vector

with anki_vector.Robot() as robot:
	while True:
	    proximity_data = robot.proximity.last_sensor_reading
	    if proximity_data is not None:
	        print('Proximity distance: {0}'.format(proximity_data.distance))
