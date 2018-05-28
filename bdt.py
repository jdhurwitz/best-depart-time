import googlemaps
from datetime import datetime
import argparse

with open("data", 'r') as datafile:
	read_lines = datafile.readlines()
	read_lines = [line.rstrip('\n') for line in read_lines]

key = read_lines[0]

gmaps = googlemaps.Client(key=key)

"""
Input
type: string
format: %Y-%m-%dT%H:%M
e.g. 2018-09-10T23:55 
"""
if __name__=="__main__":
	parser = argparse.ArgumentParser()
	#TODO: need to add start and end locations

	parser.add_argument("-date")
	parser.add_argument("-now")

	args = parser.parse_args()
	user_entered_date = args.date
	if user_entered_date is None:
		user_entered_date = datetime.now()
	else:
		user_entered_date = datetime.strptime(user_entered_date, "%Y-%m-%dT%H:%M")



	print(user_entered_date)
	#hard coded for now - need to oull from args
	directions_result = gmaps.directions("32.836069, -117.099243",
	                                     "34.061141, -118.436618",
	                                     mode="driving",
	                                     avoid="ferries",
	                                     departure_time=user_entered_date
	                                    )

	#need to customize this
	print(directions_result[0]['legs'][0]['distance']['text'])
	print(directions_result[0]['legs'][0]['duration']['text'])