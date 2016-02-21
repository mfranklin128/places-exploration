increment = 0.0012
starting_lat = 40.7066128
starting_long = -74.0129726
for i in range(50):
	for j in range(10):
		print str((starting_lat + increment*i)) + " " + str((starting_long + increment*j))
