from rtree import index
import numpy
import math
from datetime import datetime

def d(p1, p2):
    # p1, p2 = [long, lat]
    if p1 == p2: # special case: p1 = p2
        return 0.0
    # end of if
    #print '1'
    # Great-circle distance
    phi_s = math.radians(p1[1])
    phi_f = math.radians(p2[1])

    delta_lampda = math.radians(p1[0]) - math.radians(p2[0])
    delta_phi = phi_s - phi_f
    #print '2'
    delta_sigma = 2 * math.asin(math.sqrt( math.sin(delta_phi / 2) * math.sin(delta_phi / 2) + math.cos(phi_s) * math.cos(phi_f) * math.sin(delta_lampda / 2) * math.sin(delta_lampda / 2)))
    return delta_sigma * 6378137 # unit (meter)

def find_min_dis(point,location):
    min_1 = 10000000
    min_2 = 10000000
    min_3 = 10000000
    lat_a = point[0]
    lon_a = point[1]
    min_station_1 = []
    min_station_2 = []
    min_station_3 = []
    for l in location:
        lat_b = l[0]
        lon_b = l[1]
        p1 = [lon_a,lat_a]
        p2 = [lon_b,lat_b]
        dis = d(p1,p2)
        if dis < min_1:
            min_3 = min_2
            min_station_3 = min_station_2
            min_2 = min_1
            min_station_2 = min_station_1
            min_1 = dis
            min_station_1 = l
        else:
            if dis < min_2:
                min_3 = min_2
                min_station_3 = min_station_2
                min_2 = dis
                min_station_2 = l
            else:
                if dis < min_3:
                    min_3 = dis
                    min_station_3 = l
    return [min_station_1,min_station_2,min_station_3]


def get_cover_tower(cell_tower,entrance,cover_range):

    #entrance = [lon,lat]
    ref_tower = []
    for tower in cell_tower: #tower = [lon,lat]
        if d(entrance,(tower[1],tower[0])) <= cover_range:
            ref_tower.append([tower[1],tower[0]])
    return ref_tower


def collect_cell_tower(all_user_data,output_file):
    # [imsi,start_time,end_time,lon,lat]
    cell_tower = set()
    f = open(output_file,"w")
    for key in all_user_data:
        for row in all_user_data[key]:
            lon,lat = str(row[3]),str(row[4])
            cell_tower.add( (lon,lat) )

    for lon,lat in cell_tower:
        f.write(lon+","+lat+"\n")

    f.close()


def HSR_reference_system(cell_file,stations):
    cell_f = open("%s"%(cell_file),"r")
    cell_data = [[float(row.rstrip().split(",")[1]),float(row.rstrip().split(",")[0])] for row in cell_f]
    k = 3
    HSR_ref_sys = {}
    for s in stations.keys():
        lon,lat = stations[s]['position']
        min_stations = find_min_dis([lat,lon],cell_data)
        HSR_ref_sys[s] = list()
        for i in range(0,k):
            HSR_ref_sys[s].append([min_stations[i][1],min_stations[i][0]])
    #print(HSR_ref_sys)
    return HSR_ref_sys


def rail_reference_system(cell_file,stations):
    cell_f = open("%s"%(cell_file),"r")
    cell_data = [[float(row.rstrip().split(",")[1]),float(row.rstrip().split(",")[0])] for row in cell_f]
    k = 3
    rail_ref_sys = {}
    for s in stations.keys():
        lon,lat = stations[s]['position']
        min_stations = find_min_dis([lat,lon],cell_data)
        rail_ref_sys[s] = []
        for i in range(0, k):
            rail_ref_sys[s].append([min_stations[i][1],min_stations[i][0]])

    return rail_ref_sys

def MRT_reference_system(parameter,cell_file,entrance_file,output_file,ref_type='KNT'):

    cell_f = open("%s"%(cell_file),"r")
    entrance_f = open("%s"%(entrance_file),"r")
    output_f = open("%s"%(output_file),"w")

    cell_data = [ [float(row.rstrip().split(",")[1]),float(row.rstrip().split(",")[0])] for row in cell_f]

    if ref_type == 'CRS':
        coverage = parameter
        entrance2ref = {}
        for row in entrance_f:
            lon,lat = row.rstrip().split(",")[-2:]
            lon,lat = float(lon),float(lat)
            cover_stations = get_cover_tower(cell_data,[lon,lat],coverage)
            while len(cover_stations) == 0:
                coverage = coverage + 100
                cover_stations = get_cover_tower(cell_data,[lon,lat],coverage)
            entrance2ref[(lon,lat)] = []
            for ref in cover_stations:
                entrance2ref[(lon,lat)].append(ref)

        for ent in entrance2ref.keys():
            for ref in entrance2ref[ent]:
                # ref_tower => position of entrance
                output_f.write( str(ref[0])+","+str(ref[1])+","+str(ent[0])+","+str(ent[1])+"\n" )
    elif ref_type == 'KNT':
        k = parameter
        entrance2ref = {}
        for row in entrance_f:
            lon,lat = row.rstrip().split(",")[-2:]
            lon,lat = float(lon),float(lat)
            min_stations = find_min_dis([lat,lon],cell_data)
            entrance2ref[(lon,lat)] = []
            for i in range(1,k+1,1):
                entrance2ref[(lon,lat)].append(min_stations[i])

        for ent in entrance2ref.keys():
            for ref in entrance2ref[ent]:
                # ref_tower => position of entrance
                output_f.write( str(ref[1])+","+str(ref[0])+","+str(ent[0])+","+str(ent[1])+"\n" )

    cell_f.close()
    entrance_f.close()
    output_f.close()

def preprocessing(user_raw_data):
    #user_raw_data: [[user_imsi,unix_time,lon,lat]...]

    user_data = []
    user_data.append(user_raw_data[0])

    # remove oscillation data
    i = 1
    while i < len(user_raw_data) - 1:
        if str(user_raw_data[i-1][2]) + str(user_raw_data[i-1][3]) == str(user_raw_data[i+1][2]) + str(user_raw_data[i+1][3]) and\
            str(user_raw_data[i][2]) + str(user_raw_data[i][3]) != str(user_raw_data[i+1][2]) + str(user_raw_data[i+1][3]):
            user_data.append(user_raw_data[i+1])
            i = i + 2
        else:
            user_data.append(user_raw_data[i])
            i = i + 1

    if i < len(user_raw_data):
        user_data.append(user_raw_data[i])

    #merge data
    result_data = []
    start_time = user_data[0][1]
    end_time = user_data[0][1]
    imsi = user_data[0][0]
    lon = user_data[0][2]
    lat = user_data[0][3]
    for i in range(1,len(user_data)):
        if user_data[i][2] == lon and user_data[i][3] == lat:
            end_time = user_data[i][1]
        else:
            result_data.append([imsi,start_time,end_time,lon,lat])
            start_time = user_data[i][1]
            end_time = user_data[i][1]
            lon = user_data[i][2]
            lat = user_data[i][3]
    result_data.append([imsi,start_time,end_time,lon,lat])

    # result_data = [[imsi,start_time,end_time,lon,lat]...]
    return result_data


def bus_spatial_index(route,all_user_data,stay_time=10,grid_size=0.5):
    # build R-tree index for each bus stop
    p = index.Property()
    idx = index.Index(properties=p)
    route2rid = {}
    x_delta = 0.00198726326918 # 1km
    y_delta = 0.00179663056824 # 1km
    h_x = x_delta*grid_size
    h_y = y_delta*grid_size
    rid = 0
    for r in route.keys():
        route2rid[r] = []
        '''
        if r[:3] == 'NWT':
            for item in route[r]:
                h_x2 = x_delta*0.5
                h_y2 = y_delta*0.5
                x = float(item[2])
                y = float(item[3])
                bound = (x-h_x2,y-h_y2,x+h_x2,y+h_y2)
                idx.insert(rid,bound,obj=rid)
                route2rid[r].append(rid)
                rid = rid + 1
        '''
        for item in route[r]:
            x = float(item[2])
            y = float(item[3])
            bound = (x-h_x,y-h_y,x+h_x,y+h_y)
            idx.insert(rid,bound,obj=rid)
            route2rid[r].append(rid)
            rid = rid + 1


    users = all_user_data.keys()
    user2rid = {}
    rid2user = {}

    for i in range(0,rid+1,1):
        rid2user[i] = set()

    for num,u in enumerate(users,0):
        user2rid[u] = []
        user_data = all_user_data[u]

        for row in user_data:
            x,y = float(row[3]),float(row[4])
            result = [i for i in idx.intersection((x,y,x,y))]
            for r in result:
                rid2user[r].add(u)

            if (int(row[2])-int(row[1])) >= stay_time*60:
                user2rid[u].append([result,row[1],row[2],row[3],row[4],1])
            else:
                user2rid[u].append([result,row[1],row[2],row[3],row[4],0])

    return rid2user,user2rid,route2rid
