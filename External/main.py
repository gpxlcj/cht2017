#! -*- coding:utf-8 -*-
from CHT import External
import os, errno
import csv
import time
import pandas
import argparse
import cPickle as pickle


def mrt_main():
    pass


def bus_main():
    # bus route
    TPE_route = External.bus_route('taipei')
    NWT_route = External.bus_route('newtaipei')
    route = TPE_route
    for key in NWT_route.keys():
        route[key] = NWT_route[key]

    pickle.dump(route, open("./external_data/bus/bus_route.pickle", "wb"))
    print "Data has been stored into external_data/bus/bus_route.pickle"
    # bus stop information


def hsr_main(date):
    try:
        request_date = date[:4] + '-' + date[4:6] + '-' + date[6:]
    except:
        print('date format error')
    hsr_station = External.HSR_station()
    hsr_travel_time = External.HSR_travel_time(request_date)

    hsr_travel_time_filename = 'hsr_travel_time_' + date + ".pickle"

    pickle.dump(hsr_station, open("./external_data/hsr/hsr_station.pickle", "wb"))
    pickle.dump(hsr_travel_time, open("./external_data/hsr/" + hsr_travel_time_filename, "wb"))

    print "Data has been stored into 'external_data/hsr/hsr_station.pickle'"
    print "Data has been stored into 'external_data/hsr/" + hsr_travel_time_filename + "'"


def train_main():
    train_station = External.rail_station()
    pickle.dump(train_station, open("./external_data/train/train_station.pickle", "wb"))
    print "Data has been stored into 'external_data/hsr/train_station.pickle'"


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=str, help='(mrt/bus/hsr/train)')
    parser.add_argument("-d", "--datetime", type=str, default='20170801', help="update datetime")
    args = parser.parse_args()
    print "Updating external data of mode: ", args.mode
    print "Start processing..."

    if args.mode == "mrt" or args.mode == "MRT":
        start_time = time.time()
        mrt_main()
        end_time = time.time()
        print "================"
        print "time: {:.2f} seconds".format(end_time - start_time)
    elif args.mode == "bus" or args.mode == "Bus":
        start_time = time.time()
        bus_main()
        end_time = time.time()
        print "================"
        print "time: {:.2f} seconds".format(end_time - start_time)
    elif args.mode == "hsr" or args.mode == "Hsr":
        start_time = time.time()
        hsr_main()
        end_time = time.time()
        print "================"
        print "time: {:.2f} seconds".format(end_time - start_time)
    elif args.mode == "train" or args.mode == "Train":
        start_time = time.time()
        train_main()
        end_time = time.time()
        print "================"
        print "time: {:.2f} seconds".format(end_time - start_time)
    else:
        print "Wrong mode type!"
