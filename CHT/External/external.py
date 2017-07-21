# -*- coding: utf-8 -*-
import simplejson, urllib
import time
import datetime
import os
import pickle



def rail_station():
	# detail refer this link: http://ptx.transportdata.tw/MOTC/Swagger/#!/CityBusApi/CityBusApi_StopOfRoute
	url = "http://ptx.transportdata.tw/MOTC/v2/Rail/TRA/Station?$format=JSON"
	result= simplejson.load(urllib.urlopen(url))
	#stations: stations[station_id][station_name and position]
	stations = {}
	for row in result:
		station_id = row["StationID"]
		station_name = row["StationName"]["En"]
		lon = float(row["StationPosition"]["PositionLon"])
		lat = float(row["StationPosition"]["PositionLat"])
		stations[station_id] = {}
		stations[station_id]['name'] = station_name
		stations[station_id]['position'] = (lon,lat)

	return stations


def HSR_station():
	# detail refer this link: http://ptx.transportdata.tw/MOTC/Swagger/#!/CityBusApi/CityBusApi_StopOfRoute
	url = "http://ptx.transportdata.tw/MOTC/v2/Rail/THSR/Station?$format=JSON"
	result= simplejson.load(urllib.urlopen(url))
	#stations: stations[station_id][station_name and position]
	stations = {}
	for row in result:
		station_id = row["StationID"]
		station_name = row["StationName"]["En"]
		lon = float(row["StationPosition"]["PositionLon"])
		lat = float(row["StationPosition"]["PositionLat"])
		stations[station_id] = {}
		stations[station_id]['name'] = station_name
		stations[station_id]['position'] = (lon,lat)

	return stations

def datetime2unixtime(time_info,date_info):
	unix_time = int(time.mktime(time.strptime('%s %s:00'%(date_info,time_info), '%Y-%m-%d %H:%M:%S')))
	return unix_time

def HSR_travel_time(date):
	# date = YY-MM-DD
	station_url = "http://ptx.transportdata.tw/MOTC/v2/Rail/THSR/Station?$format=JSON"
	result = simplejson.load(urllib.urlopen(station_url))
	all_stations = set()
	for row in result:
		all_stations.add( row["StationID"] )

	travel_time = {}
	for dep_station in all_stations:
		travel_time[dep_station] = {}
		for arr_station in all_stations:
			if dep_station != arr_station:
				travel_time[dep_station][arr_station] = []
				timetable_url = "http://ptx.transportdata.tw/MOTC/v2/Rail/THSR/DailyTimetable/OD/%s/to/%s/%s?$format=JSON"%(dep_station,arr_station,date)
				result = simplejson.load(urllib.urlopen(timetable_url))
				for row in result:
					train_no = row["DailyTrainInfo"]["TrainNo"]
					depart_time = datetime2unixtime(row["OriginStopTime"]["DepartureTime"],date)
					arrival_time = datetime2unixtime(row["DestinationStopTime"]["ArrivalTime"],date)
					travel_time[dep_station][arr_station].append( [train_no,depart_time,arrival_time] )

	return travel_time

def bus_route(city):
	# detail refer this link: http://ptx.transportdata.tw/MOTC/Swagger/#!/CityBusApi/CityBusApi_StopOfRoute
	url = "http://ptx.transportdata.tw/MOTC/v2/Bus/StopOfRoute/City/%s?$format=JSON"%(city)
	result= simplejson.load(urllib.urlopen(url))
	route_dict = {}
	for row in result:
		name = row['RouteUID']
		direction = row['Direction']
		sequence = []
		for stop in row['Stops']:
			sequence.append([stop['StopSequence'],stop['StopUID'],stop['StopPosition']['PositionLon'],stop['StopPosition']['PositionLat']])
		route_dict[name+"_"+str(direction)] = sequence


	return route_dict



def bus_SpeedDis(city,update_frequency=5):
	date = datetime.datetime.now().strftime('%Y-%m-%d')
	bus = {}
	pre = -1
	while 1:

		if (datetime.datetime.now().strftime('%Y-%m-%d') != date):
			speed = SpeedDistribution(bus)
			pickle.dump(speed,open("%s_SpeedDis_%s.pkl"%(city,date),"wb"))
			bus = {}
			pre = int(datetime.datetime.now().strftime('%H'))
			date = datetime.datetime.now().strftime('%Y-%m-%d')


		try:
			url = "http://ptx.transportdata.tw/MOTC/v2/Bus/RealTimeByFrequency/City/%s?$format=JSON"%(city)
			result= simplejson.load(urllib.urlopen(url))
		except:
			continue

		for row in result:
			try:
				routeID = row['RouteUID']
				direction = row['Direction']
				platenum = row['PlateNumb']
				lat,lon = row['BusPosition']["PositionLat"],row['BusPosition']["PositionLon"]
				t = row["GPSTime"]

				if str(routeID) + "_" + str(direction) not in bus.keys():
					bus[str(routeID) + "_" + str(direction)] = {}

				if platenum not in bus[str(routeID) + "_" + str(direction)].keys():
					bus[str(routeID) + "_" + str(direction)][platenum] = []
				bus[str(routeID) + "_" + str(direction)][platenum].append( [lat,lon,t] )
			except:
				continue


		time.sleep(60*update_frequency)

def SpeedDistribution(bus_real_record):
	SpeedDis = {}
	for bus_name in bus_real_record.keys():
		#print "Bus Route:",bus_name
		count = [0]*24
		total = [0]*24
		for bus_num in bus_real_record[bus_name].keys():
			#print "Car Number:",bus_num
			for row in bus_real_record[bus_name][bus_num]:
				hour = int(row[3].split("T")[1].split(":")[0])
				total[hour] = total[hour] + row[2]
				count[hour] = count[hour] + 1
		average = [0] * 24
		for i in range(0,24,1):
			if (total[i] != 0.0) & (count[i] != 0):
				average[i] = total[i]/count[i]

		SpeedDis[bus_name] = average
	return SpeedDis



def TimeTable(schedule,time_threshold):
	date_schedule = {}

	for bus_num in schedule.keys():

		if bus_num not in date_schedule.keys():
			date_schedule[bus_num] = {}

		for stop in schedule[bus_num].keys():

			if stop not in date_schedule[bus_num].keys():
				date_schedule[bus_num][stop] = []

			if len(schedule[bus_num][stop]) > 0:
				pre = schedule[bus_num][stop][0]
				for time in schedule[bus_num][stop][1:]:
					if abs(time-pre) > time_threshold*60:
						date_schedule[bus_num][stop].append(pre)
					pre = time
				date_schedule[bus_num][stop].append(schedule[bus_num][stop][-1])

	return date_schedule


def bus_schedule(city,time_threshold=5,update_frequency=5):
	date = datetime.datetime.now().strftime('%Y-%m-%d')
	pre = -1
	schedule = {}
	while 1:
		try:
			url = "http://ptx.transportdata.tw/MOTC/v2/Bus/EstimatedTimeOfArrival/City/%s?$format=JSON"%(city)
			result= simplejson.load(urllib.urlopen(url))
			unix_time = int(time.mktime(time.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')))
		except:
			continue

		if (datetime.datetime.now().strftime('%Y-%m-%d') != date):
			schedule = TimeTable(schedule,time_threshold)
			pickle.dump(schedule,open("schedule_%s_%s.pkl"%(city,date),"wb"))
			schedule = {}
			pre = int(datetime.datetime.now().strftime('%H'))
			date = datetime.datetime.now().strftime('%Y-%m-%d')

		for row in result:
			try:
				stopUID = row['StopUID']
				RouteID = row['RouteUID']
				direction = row['Direction']

				if str(RouteID)+"_"+str(direction)  not in schedule.keys():
						schedule[str(RouteID)+"_"+str(direction)] = {}

				if stopUID not in schedule[str(RouteID)+"_"+str(direction)].keys():
						schedule[str(RouteID)+"_"+str(direction)][stopUID] = []

				EsTime= int(row['EstimateTime'])
				arr_time = unix_time + EsTime
				schedule[str(RouteID)+"_"+str(direction)][stopUID].append(arr_time)
			except:
				continue
		time.sleep(update_frequency*60)
