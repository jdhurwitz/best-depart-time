import googlemaps
from datetime import datetime, date, time, timedelta
import argparse
import numpy as np
import matplotlib.pyplot as plt

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
def daterange(start_date, end_date):
	upper_lim_sec = int((end_date-start_date).seconds)
	upper_lim_hr = int(upper_lim_sec / 3600)
	print("Hours in range", upper_lim_hr)
	for n in range(upper_lim_hr):
		hr_delta_in_secs = n*3600
		yield start_date + timedelta(seconds = hr_delta_in_secs)

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	#TODO: need to add start and end locations

	parser.add_argument("-start")
	parser.add_argument("-end")

	args = parser.parse_args()
	if args.start is None or args.end is None:
		raise Exception("Need to specify a start and end date")

	start = datetime.strptime(args.start, "%Y-%m-%dT%H:%M")
	end = datetime.strptime(args.end, "%Y-%m-%dT%H:%M")

	trip_data = []
	travel_times = []
	time_list = []
	for cur_date in daterange(start, end):
		time_list.append(cur_date)
		print(cur_date)

		#hard coded for now - need to oull from args
		#TODO: add configs for tolls, highways, etc
		directions_result = gmaps.directions("32.836069, -117.099243",
		                                     "34.061141, -118.436618",
		                                     mode="driving",
		                                     avoid="ferries",
		                                     departure_time=cur_date
		                                    )
		print("res", directions_result[0]['legs'][0]['duration_in_traffic']['value']/3600)
		trip_data = np.append(trip_data, directions_result)
		travel_times = np.append(travel_times, directions_result[0]['legs'][0]['duration_in_traffic']['value']) #default is in secs


	#use this as index into trip_data
	min_idx = np.argmin(travel_times)
	print(travel_times/3600)
	plt.bar(time_list , travel_times/3600)
	plt.show()

	print("best time to leave is: ")
	print(time_list[min_idx])


