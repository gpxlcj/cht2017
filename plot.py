import matplotlib.pyplot as plt
import mplleaflet
import os, errno
import time
import numpy as np
import cPickle as pickle
import csv
import datetime
import argparse
import pandas

def plot_train(trip, data_date, route):
    print trip

    data_path = 'data/user_data/' + data_date

    u = 'u_'+trip[0]
    f = open(os.path.join(data_path,u), "r")
    data = [[row[0], int(row[4]), float(row[2]), float(row[3])] for row in csv.reader(f, delimiter='|')] #[imsi, unix_time, lon, lat]
    data_df = pandas.DataFrame(data, columns=['imsi', 'time', 'lon', 'lat'])
    data_df = data_df.sort_values(['time'])
    data = data_df.values.tolist()
    #data = np.array([row.rstrip().split("|") for row in f])  #-1943160471|16:57:03,966,490|121.526|25.088|1483520223
    f.close()

    start = int(trip[1])
    end = int(trip[2])
    user = []
    for row in data:
        if (row[1] >= start) and (row[1] <=end):
            user.append([row[2],row[3]])
    print user

    ### plot user data ###
    user = np.array(user)
    plt.hold(True)
    plt.plot(user[:,0],user[:,1],'mo',ms=15)
    plt.plot(user[:,0],user[:,1],'r--',linewidth=5)

    ### plot train station ###
    rail_station = np.array([[rail[station]['position'][0], rail[station]['position'][1]] for station in trip[3:5]])
    print rail_station
    plt.plot(rail_station[:,0],rail_station[:,1],'bo',ms=15)

    try:
        os.makedirs('plot_train/'+data_date)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    mplleaflet.save_html(fileobj="./plot_train/%s/%s_%s_%s.html"%(data_date,u,trip[1],trip[2]))
    print

def plot_bus(trip, data_date, route):
    # trip: [-1003216209,1483537823,1483539806,NWT16595,1,11,42]
    # trip: [imsi,start_time,end_time,bus_number,go_or_back,start_stop,end_stop]
    print trip

    data_path = 'data/user_data/' + data_date

    u = 'u_'+trip[0]
    f = open(os.path.join(data_path,u), "r")
    data = [[row[0], int(row[4]), float(row[2]), float(row[3])] for row in csv.reader(f, delimiter='|')] #[imsi, unix_time, lon, lat]
    data_df = pandas.DataFrame(data, columns=['imsi', 'time', 'lon', 'lat'])
    data_df = data_df.sort_values(['time'])
    data = data_df.values.tolist()
    #data = np.array([row.rstrip().split("|") for row in f])  #-1943160471|16:57:03,966,490|121.526|25.088|1483520223
    f.close()

    '''
    year = int(data_date[0:4])
    month = int(data_date[5])
    date = int(data_date[7])

    ### sort user data by datetime ###
    for n,row in enumerate(data,0):
        hour,minute,second = row[1].split(",")[0].split(":")
        unix_time = int(time.mktime(time.strptime('%d-%d-%d %s:%s:%s'%(year,month,date,hour,minute,second), '%Y-%m-%d %H:%M:%S')))
        data[n][4] = str(unix_time)

    data = sorted(data,key=lambda x:x[4])
    data = [[row[0],int(row[4]),float(row[2]),float(row[3])] for row in data] #imsi,unixtime,lon,lat
    '''

    start = int(trip[1])
    end = int(trip[2])
    user = []
    for row in data:
        if (row[1] >= start) & (row[1] <=end):
            user.append([row[2],row[3]])
    print user

    ### plot user data ###
    user = np.array(user)
    plt.hold(True)
    plt.plot(user[:,0],user[:,1],'go',ms=15)
    plt.plot(user[:,0],user[:,1],'r--',linewidth=5)


    ### plot route data ###
    route_name = trip[3]+"_"+trip[4]
    route_list = route[route_name][int(trip[5]): int(trip[6])+1] #from start_stop to end_stop
    bus_line = np.array([[float(item[2]),float(item[3])] for item in route_list])	#lon,lat => bus route
    plt.plot(bus_line[:,0],bus_line[:,1],'co',ms=15)
    plt.plot(bus_line[:,0],bus_line[:,1],'b--',linewidth=5)

    try:
        os.makedirs('plot_bus/'+data_date)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    mplleaflet.save_html(fileobj="./plot_bus/%s/%s_%s_%s.html"%(data_date,u,trip[1],trip[2]))
    print

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=str, help='(bus/train)')
    parser.add_argument("date", type=str, help='(yyyymmdd)')
    args = parser.parse_args()

    data_date = args.date
    if args.mode == "bus" or args.mode == "Bus":
        route = pickle.load(open("data/bus_route.pickle", "rb"))
        with open("output/bus_"+data_date+".csv", "r") as f:
            for row in f:
                plot_bus(row.rstrip().split(','), data_date, route)
    elif args.mode == "train":
        rail = pickle.load(open("data/rail_information.pickle", "rb"))
        with open("output/rail_"+data_date+".csv", "r") as f:
            for row in f:
                plot_train(row.rstrip().split(','), data_date, rail)
    else:
        pass
