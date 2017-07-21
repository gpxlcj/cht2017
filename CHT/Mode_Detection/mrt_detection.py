import os
import datetime
import time
import math

def initial_reference_system(rf_sys_path):    
    tower_dic = {}   
    f = open(rf_sys_path)
    for line in f:
        line = line.strip()
        info = line.split(',')
        if tower_dic.has_key(info[0]+info[1]):
            p1 = tower_dic[info[0]+info[1]]
            p2 = [float(info[2]),float(info[3])]
            p0 = [float(info[0]),float(info[1])]
            if d(p0,p2) < d(p0,p1):
                tower_dic[info[0]+info[1]] = [float(info[2]),float(info[3])]
            else:
                continue
        else:
            tower_dic[info[0]+info[1]] = [float(info[2]),float(info[3])]    
    f.close()
    return tower_dic

def load_MRT_route(mrt_route_file):
    mrt_route = []
    route_name = []
    f = open(mrt_route_file)
    count = 0
    for line in f:
        info = line.strip().split(',')
        count += 1 
        if count == 1:
            route_name.append(info[0])
            route_name.append(info[0])
            continue
        elif count == 4:
            count = 1
            route_name.append(info[0])
            route_name.append(info[0])
            continue
        else:
            
            route = []
            for i in range(0,len(info)):
                if len(info[i]) < 1:
                    continue
                route.append(info[i])
            mrt_route.append(route)
    f.close()
    #print route_name
    return [route_name,mrt_route]
	
def entrance_to_station(mrt_entrance_file):    
    dic_lat_lon_to_name = {}
    f = open(mrt_entrance_file)
    for line in f:
        break
    for line in f:
        #print "line"
        #print line
        line = line.strip()
        info = line.split(',')        
        dic_lat_lon_to_name[info[-2]+info[-1]] = info[1]
    f.close()
    return dic_lat_lon_to_name


#[name_list,travel_time_list,stop_time_list] = get_travel_time_list()

def get_station_entrance(mrt_entrance_file):    
    com_station_entrance = {}
    f = open(mrt_entrance_file)
    for line in f:
        break
    for line in f:
        line = line.strip()
        info = line.split(',')
        station_name = info[1]
        lon = float(info[-2])
        lat = float(info[-1])
        if com_station_entrance.has_key(station_name):
            com_station_entrance[station_name].append([lon,lat])
        else:
            com_station_entrance[station_name] = [[lon,lat]]        
    f.close()
    return com_station_entrance
    
def get_travel_time_list(travel_time_file):
    f_t = open(travel_time_file)
    name_list = []
    tmp_name_list = []
    travel_time_list = []
    tmp_t_list = []
    stop_time_list = []
    tmp_stop_time_list = []
    
    line_name = ''
    for line in f_t:
        line = line.strip()
        info = line.split(',')
        line_name = info[0]
        start = info[1]
        end = info[2]
        t = info[3]
        st = info[-1]
        tmp_name_list.append(start)
        tmp_name_list.append(end)
        tmp_t_list.append(0)
        tmp_t_list.append(t)
        tmp_stop_time_list.append(0)
        tmp_stop_time_list.append(st)
        break
    for line in f_t:
        line = line.strip()
        info = line.split(',')
        
        if info[0] == line_name:    
            end = info[2]
            t = info[3]
            st = info[-1]
            tmp_name_list.append(end)
            tmp_t_list.append(t)
            tmp_stop_time_list.append(st)
        else:
            line_name = info[0]
            name_list.append(tmp_name_list)
            travel_time_list.append(tmp_t_list)
            stop_time_list.append(tmp_stop_time_list)
            tmp_name_list = []
            tmp_name_list.append(info[1])
            tmp_name_list.append(info[2])
            tmp_t_list = []
            tmp_t_list.append(0)
            tmp_t_list.append(info[3])
            tmp_stop_time_list = []
            tmp_stop_time_list.append(0)
            tmp_stop_time_list.append(info[-1])
            
    travel_time_list.append(tmp_t_list)
    name_list.append(tmp_name_list)
    stop_time_list.append(tmp_stop_time_list)
    f_t.close()
      
    return [name_list,travel_time_list,stop_time_list]
  
def get_complete_route(user_route,mrt_route): # user_route: user route; mrt_route: all mrt route
    start_index = 0
    end_index = 0
    result = []
    whether_break = False
    #print user_route
    #print mrt_route
    count = -1
    while end_index <= len(user_route) - 1:
        if count != -1 and len(result) == 0:
            return result
        count = -1
        modify_flag = False
        
        for route in mrt_route:
            whether_break = False
            count += 1
            
            if user_route[start_index] in route:
                #print 'yes'
                for i in range(start_index+1,len(user_route)):
                    if user_route[i] in route:
                        
                        #end_index = i
                        #print '=================================='
                        #print count 
                        #print route.index(user_route[i])
                        #print route.index(user_route[start_index])
                        if int(route.index(user_route[i])) < int(route.index(user_route[start_index])):
                            if end_index > start_index:
                                result.append([count,route.index(user_route[start_index]),route.index(user_route[end_index])])
                                start_index = i-1
                                end_index = i-1
                                whether_break = True
                            break
                                
                            
                        else:
                            end_index = i
                            modify_flag = True
                        
                    else:
                        if start_index == end_index:
                            
                            whether_break = False
                            break
                        else: 
                            try:
                                #print count 
                                #print route.index(user_route[start_index])
                                #print route.index(user_route[end_index])                         
                                result.append([count,route.index(user_route[start_index]),route.index(user_route[end_index])])
            
                            except Exception:
                                {}
                                
                                #print '1'
                            start_index = i-1
                            end_index = i-1
                            whether_break = True
                            break
                
                if end_index == len(user_route) - 1 and start_index != end_index:
                    #print start_index
                    #print end_index
                    
                    try:
                        result.append([count,route.index(user_route[start_index]),route.index(user_route[end_index])])
                    except:
                        {}
                        #print '2'
                    return result                   
                if whether_break == True:
                    
                    break
        if modify_flag == False:
            start_index = start_index + 1
            end_index = start_index 
            
                
                
    #print "==========================="
    #print result
    return result

def tower_station_matching(tower_dic,dic_lat_lon_to_name,user_data): #user_data: [[imsi,start_time,end_time,lon,lat]]
    mrt_list = []
    
    for data in user_data:
        lon = str(data[3])
        lat = str(data[4])
        
        if (lon+lat) in tower_dic:
            tmp = {}
            start_time = data[1]  
            end_time = data[2]
            duration = float(end_time) - float(start_time)       
            tmp[lon + ',' +lat] = [start_time,end_time,duration]
            mrt_list.append(tmp)
    
    if len(mrt_list) == 0:
        return [] 
        
        
    #smooth
    name_mrt_list = []
    #count = 0
    #record = 0
    begin_time = 0
    end_time = 0
    duration = 0
    last_mrt_station_name = ''
    this_mrt_station_name = ''
    for key in mrt_list[0]:
        info = key.split(',')
        lon = info[0]
        lat = info[1]
        station = tower_dic[str(lon)+str(lat)]
        k = str(station[0]) + str(station[1])
        last_mrt_station_name = dic_lat_lon_to_name[k]  
        #count = int(mrt_list[0][key][0])
        #record = int(mrt_list[0][key][1])
        begin_time = float(mrt_list[0][key][0])
        end_time = float(mrt_list[0][key][1])
        duration = float(mrt_list[0][key][2])
        break
        
        
    for i in range(1, len(mrt_list)):
        for key in mrt_list[i]:
            info = key.split(',')
            lon = info[0]
            lat = info[1]
            station = tower_dic[str(lon)+str(lat)]
            k = str(station[0]) + str(station[1])
            this_mrt_station_name = dic_lat_lon_to_name[k]
            if this_mrt_station_name == last_mrt_station_name:
                end_time = float(mrt_list[i][key][1])
                duration = duration + float(mrt_list[i][key][2])
            else:
                tmp = {}
                tmp[last_mrt_station_name] = [0,0,begin_time,end_time,duration]
                name_mrt_list.append(tmp)
                last_mrt_station_name = this_mrt_station_name
                #count = int(mrt_list[i][key][0])
                #record = int(mrt_list[i][key][1])
                begin_time = float(mrt_list[i][key][0])
                end_time = float(mrt_list[i][key][1])
                duration = float(mrt_list[i][key][2])
    
                
    tmp = {}
    tmp[last_mrt_station_name] = [0,0,begin_time,end_time,duration]
    name_mrt_list.append(tmp)
    
    
    result_mrt_list = []
    name_0 = 0
    name_1 = 0
    name_2 = 0
    duration = 0
    begin = 0
    end = 0 
    end_0 = 0
    duration_0 = 0           
    flag = 0
    i = 0
    while i <= (len(name_mrt_list)-3):
        flag = 0
        for key in name_mrt_list[i]:
            name_0 = key
            begin = float(name_mrt_list[i][key][2]) 
            end_0 = float(name_mrt_list[i][key][3])
            duration_0 = float(name_mrt_list[i][key][-1])
        for key in name_mrt_list[i+1]:
            name_1 = key
            duration = float(name_mrt_list[i+1][key][-1])
        for key in name_mrt_list[i+2]:
            name_2 = key
            end = float(name_mrt_list[i+2][key][3])
        if name_0 == name_2 and name_1 != name_2 and duration < 60:
            duration = end - begin
            tmp = {}
            tmp[name_0] = [0,0,begin,end,duration]
            result_mrt_list.append(tmp)
            flag = 1
            i = i + 3
        else:
            i = i + 1
            tmp = {}
            tmp[name_0] = [0,0,begin,end_0,duration_0]
            result_mrt_list.append(tmp)
    if flag == 0:
        try:
            for key in name_mrt_list[-2]:
                name_0 = key
                begin = float(name_mrt_list[-2][key][2])
                end_0 = float(name_mrt_list[-2][key][3])
                duration_0 = float(name_mrt_list[-2][key][-1])
                tmp = {}
                tmp[name_0] = [0,0,begin,end_0,duration_0]
                result_mrt_list.append(tmp)
        except Exception:
            
            return name_mrt_list
        for key in name_mrt_list[-1]:
            name_0 = key
            begin = float(name_mrt_list[-1][key][2])
            end_0 = float(name_mrt_list[-1][key][3])
            duration_0 = float(name_mrt_list[-1][key][-1])
            tmp = {}
            tmp[name_0] = [0,0,begin,end_0,duration_0]
            result_mrt_list.append(tmp)
    result_mrt_list_2 = []
    name_0 = 0
    name_1 = 0
    name_2 = 0
    duration = 0
    begin = 0
    end = 0 
    end_0 = 0
    duration_0 = 0           
    flag = 0
    i = 0
    while i <= (len(result_mrt_list)-3):
        flag = 0
        for key in result_mrt_list[i]:
            name_0 = key
            begin = float(result_mrt_list[i][key][2])
            end_0 = float(result_mrt_list[i][key][3])
            duration_0 = float(result_mrt_list[i][key][-1])
        for key in result_mrt_list[i+1]:
            name_1 = key
            duration = float(result_mrt_list[i+1][key][-1])
        for key in result_mrt_list[i+2]:
            name_2 = key
            end = float(result_mrt_list[i+2][key][3])
        if name_0 == name_2 and name_1 != name_2 and duration < 60:
            duration = end - begin
            tmp = {}
            tmp[name_0] = [0,0,begin,end,duration]
            result_mrt_list_2.append(tmp)
            flag = 1
            i = i + 3
        else:
            i = i + 1
            tmp = {}
            tmp[name_0] = [0,0,begin,end_0,duration_0]
            result_mrt_list_2.append(tmp)
    if flag == 0:
        try:
            for key in result_mrt_list[-2]:
                name_0 = key
                begin = float(result_mrt_list[-2][key][2])
                end_0 = float(result_mrt_list[-2][key][3])
                duration_0 = float(result_mrt_list[-2][key][-1])
                tmp = {}
                tmp[name_0] = [0,0,begin,end_0,duration_0]
                result_mrt_list_2.append(tmp)
        except Exception:
            return result_mrt_list
        for key in result_mrt_list[-1]:
            name_0 = key
            begin = float(result_mrt_list[-1][key][2])
            end_0 = float(result_mrt_list[-1][key][3])
            duration_0 = float(result_mrt_list[-1][key][-1])
            tmp = {}
            tmp[name_0] = [0,0,begin,end_0,duration_0]
            result_mrt_list_2.append(tmp)    
           
    return result_mrt_list_2     	
	
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
	
def get_interval_threshold(last_station,this_station,travel_time_file,theta):
    [name_list,travel_time_list,stop_time_list] = get_travel_time_list(travel_time_file)
    threshold = theta
    for i in range(0,len(name_list)):
        tmp_name_list = name_list[i]
        if last_station in tmp_name_list and this_station in tmp_name_list:
            start = tmp_name_list.index(last_station)
            end = tmp_name_list.index(this_station)
            
            interval = 0
            for j in range(start+1,end+1):
                interval += int(travel_time_list[i][j]) + int(stop_time_list[i][j-1])
            interval += int(stop_time_list[i][end])
            if interval > threshold:
                threshold = interval                   
    return (threshold + theta)

def get_origin(mrt_route,start_index,tower,time_interval,com_station_entrance,travel_time_file,theta = 60,delta_d = 500,delta_t = 400):
    
    result = []
    if start_index == 0:
        return []
    else:
        
        base_dis = 100000000
        #print com_station_entrance
        for entrance in com_station_entrance[mrt_route[start_index]]:
            dis = d(tower,entrance)
            if dis < base_dis:
                base_dis = dis
                
        for i in range(0,start_index):            
            for entrance in com_station_entrance[mrt_route[i]]:                
                dis = d(tower,entrance)
                         
                if dis < base_dis and dis < delta_d:
                    if time_interval < get_interval_threshold(mrt_route[i],mrt_route[start_index],travel_time_file,theta) + delta_t:
                        for j in range(i, start_index):
                            result.append(mrt_route[j])
                        return result
    return []
                        
def get_destination(mrt_route,end_index,tower,time_interval,com_station_entrance,travel_time_file,theta = 60,delta_d = 500,delta_t = 400):
    
    result = []
    if end_index == len(mrt_route) - 1:
        return []
    else:
        base_dis = 100000000
        for entrance in com_station_entrance[mrt_route[end_index]]:
            dis = d(tower,entrance)
            if dis < base_dis:
                base_dis = dis
        
        i = len(mrt_route)
        while i > end_index:
            i = i - 1    
            for entrance in com_station_entrance[mrt_route[i]]:
                dis = d(tower,entrance)   
                
                                    
                if dis < base_dis and dis < delta_d:
                    if time_interval < get_interval_threshold(mrt_route[end_index],mrt_route[i],travel_time_file,theta) + delta_t:
                        for j in range(end_index + 1, i+1):
                            result.append(mrt_route[j])
                        return result
    return []                        
                    
      
def interval_time_based_segment(mrt_list,tower_dic,dic_lat_lon_to_name,travel_time_file,theta = 60,beta = 900):
    last_mrt_station_name = ''
    this_mrt_station_name = ''
    old_start = 0
    old_end = 0
    start_duration = 0
    end_duration = 0
    for point_dic in mrt_list:
        for key in point_dic:            
            old_start = float(point_dic[key][2])          
            old_end = float(point_dic[key][3])            
            last_mrt_station_name = key
            break
        break
    
    
    selected_list = [[last_mrt_station_name,old_start,old_end]]
    start_duration = 61
    total_list = []
    
           
    for point_index in range(1,len(mrt_list)):
        point_dic = mrt_list[point_index]
        for key in point_dic:
            
            start_time = float(point_dic[key][2])            
            end_time = float(point_dic[key][3])           
            interval =  (start_time - old_end)
            duration = end_time - start_time
            
                    
            this_mrt_station_name =  key  
            if len(selected_list) == 0:
                selected_list.append([this_mrt_station_name,start_time,end_time])
                start_duration = float(end_time) - float(start_time)
                last_mrt_station_name = this_mrt_station_name
                continue 
            
            interval_threshold = get_interval_threshold(last_mrt_station_name,this_mrt_station_name,travel_time_file,theta)
            it = get_interval_threshold(this_mrt_station_name,last_mrt_station_name,travel_time_file,theta)
            if  it > interval_threshold:
                interval_threshold = it
           
            
            
            duration_threshold = beta
                
            if interval <= interval_threshold and duration <= duration_threshold:
                
                end_duration = duration
                selected_list.append([this_mrt_station_name,start_time,end_time])
                last_mrt_station_name = this_mrt_station_name
            elif interval > interval_threshold and duration <= duration_threshold:
                
                if interval <= interval_threshold:
                    selected_list.append([this_mrt_station_name,start_time,end_time])
                    end_duration = duration
                    
                
                if len(selected_list) >= 2: 
                    total_list.append(selected_list)
                selected_list = []
                
                selected_list.append([this_mrt_station_name,start_time,end_time])
                start_duration = float(end_time) - float(start_time)
                last_mrt_station_name = this_mrt_station_name
            elif interval <= interval_threshold and duration > duration_threshold:
                selected_list.append([this_mrt_station_name,start_time,end_time])
                end_duration = duration
                
                if len(selected_list) >= 2: 
                    total_list.append(selected_list)
                selected_list = []
                selected_list.append([this_mrt_station_name,start_time,end_time])
                start_duration = float(end_time) - float(start_time)
                last_mrt_station_name = this_mrt_station_name
            elif interval > interval_threshold and duration > duration_threshold:
                
                if interval < interval_threshold:
                    selected_list.append([this_mrt_station_name,start_time,end_time])
                    end_duration = duration
                #if len(selected_list) >= 2 and start_duration != 0 and end_duration != 0: 
                if len(selected_list) >= 2:
                    total_list.append(selected_list)
                selected_list = []
                selected_list.append([this_mrt_station_name,start_time,end_time])
                last_mrt_station_name = this_mrt_station_name
                start_duration = float(end_time) - float(start_time)
                                
            old_start = start_time
            old_end = end_time
            
    if len(selected_list) >= 2:          
        total_list.append(selected_list)
    
    return total_list    

    
def station_complement(user_data,total_list,mrt_route,com_station_entrance,travel_time_file,theta = 60,delta_d = 500,delta_t = 400):
    after_complement = []
    com_tower_list = []
    com_start_time_list = []
    com_end_time_list = []
    
    for data in user_data:
        com_tower_list.append([float(data[3]),float(data[4])])
        com_start_time_list.append(float(data[1]))
        com_end_time_list.append(float(data[2]))
                        
    result_route = []
    time_list = []
    for tra_list in total_list:           
        tmp_mrt_route = []
        tmp_time_list = []
        for point in tra_list:                
            key = point[0]
            if key not in tmp_mrt_route:
                tmp_mrt_route.append(key)
                tmp_time_list.append([point[-2],point[-1]])            
        result_route.append(tmp_mrt_route) 
        time_list.append(tmp_time_list)
        if len(tmp_mrt_route) < 2:
            continue            
        start_time = float(tmp_time_list[0][0])
        end_time = float(tmp_time_list[-1][1])
        try:
            com_start_index = com_start_time_list.index(start_time)
        except Exception:
            com_start_index = 0
        try:            
            com_end_index = com_end_time_list.index(end_time)
        except Exception:
            com_end_index = len(com_end_time_list)
                            
        user_route = get_complete_route(tmp_mrt_route,mrt_route)
        
        if len(user_route) == 0:
            continue
            
            
        
        com_origin = []
        com_des = []
        com_start_time = 0
        com_end_time = 0
        
        if com_start_index - 2 >= 0:

            num = user_route[0][0]
            start_index = user_route[0][1]
            com_start_time = com_end_time_list[com_start_index - 2]
            start_time = int(tmp_time_list[tmp_mrt_route.index(mrt_route[num][start_index])][1])
                            
            time_interval = start_time - com_start_time
            if time_interval > 0 :
                com_origin = get_origin(mrt_route[num],start_index,com_tower_list[com_start_index - 2],time_interval,com_station_entrance,travel_time_file,theta,delta_d,delta_t)                   
                if len(com_origin) == 0:
                    com_start_time = com_end_time_list[com_start_index - 1]
                    time_interval = start_time - com_start_time
                    com_origin = get_origin(mrt_route[num],start_index,com_tower_list[com_start_index - 1],time_interval,com_station_entrance,travel_time_file,theta,delta_d,delta_t)
                    
        elif com_start_index - 1 >= 0:
            num = user_route[0][0]
            start_index = user_route[0][1]
            com_start_time = com_end_time_list[com_start_index - 1]
            start_time = int(tmp_time_list[tmp_mrt_route.index(mrt_route[num][start_index])][1])
            time_interval = start_time - com_start_time
            if time_interval > 0 :
                com_origin = get_origin(mrt_route[num],start_index,com_tower_list[com_start_index - 1],time_interval,com_station_entrance,travel_time_file,theta,delta_d,delta_t)            
                    
                    
            
        if com_end_index + 2 < len(com_end_time_list):
            num = user_route[-1][0]
            end_index = user_route[-1][2]
            com_end_time = com_start_time_list[com_end_index + 2]
            end_time =  int(tmp_time_list[tmp_mrt_route.index(mrt_route[num][end_index])][0])
            time_interval = com_end_time - end_time
            if time_interval > 0:
                com_des = get_destination(mrt_route[num],end_index,com_tower_list[com_end_index + 2],time_interval,com_station_entrance,travel_time_file,theta,delta_d,delta_t)
                if len(com_des) == 0:
                    com_end_time = com_start_time_list[com_end_index + 1]
                    time_interval = com_end_time - end_time 
                    com_des = get_destination(mrt_route[num],end_index,com_tower_list[com_end_index + 1],time_interval,com_station_entrance,travel_time_file,theta,delta_d,delta_t)
                    
        elif com_end_index + 2 < len(com_end_time_list): 
            num = user_route[-1][0]
            end_index = user_route[-1][2]
            com_end_time = com_start_time_list[com_end_index + 1]
            end_time =  int(tmp_time_list[tmp_mrt_route.index(mrt_route[num][end_index])][0])
            time_interval = com_end_time - end_time
            if time_interval > 0:
                com_des = get_destination(mrt_route[num],end_index,com_tower_list[com_end_index + 1],time_interval,com_station_entrance,travel_time_file,theta,delta_d,delta_t)   
        after_complement.append([user_route,com_origin,com_des,tmp_time_list,tmp_mrt_route,com_start_time,com_end_time])
    return after_complement
       

def MRT_trip_detection(user_data,rf_sys_path,mrt_route_file,mrt_entrance_file,travel_time_file,theta = 60,beta = 900,delta_d = 500, delta_t = 400): #user_raw_data: the cellular data of a user, tower_dic: reference system
    tower_dic = initial_reference_system(rf_sys_path)
    mrt_trip_result = []
    mrt_trip_path = []
    dic_lat_lon_to_name = entrance_to_station(mrt_entrance_file)
    [route_name,mrt_route] = load_MRT_route(mrt_route_file)
    com_station_entrance = get_station_entrance(mrt_entrance_file)

    user_imsi = user_data[0][0]

    if len(user_data) == 0:
        return []

    mrt_list = tower_station_matching(tower_dic,dic_lat_lon_to_name,user_data)

    if len(mrt_list) == 0:
        return []
    total_list = interval_time_based_segment(mrt_list,tower_dic,dic_lat_lon_to_name,travel_time_file,theta,beta) # selected_list.append([this_mrt_station_name,start_time,end_time])
    after_complement = station_complement(user_data,total_list,mrt_route,com_station_entrance,travel_time_file,theta,delta_d,delta_t)

    for trip in after_complement:
        user_route = trip[0]
        com_origin = trip[1]
        com_des = trip[2]
        tmp_time_list = trip[3]
        tmp_mrt_route = trip[4]
        com_start_time = trip[5]
        com_end_time = trip[6]
        line_count = 0
        trip_str = ''
        for line in user_route:
            line_count += 1
            if line_count != 1:
                trip_str += '||'


            num = line[0]
            start_index = line[1]
            end_index = line[2]

            start_time = int(tmp_time_list[tmp_mrt_route.index(mrt_route[num][start_index])][1])
            end_time = int(tmp_time_list[tmp_mrt_route.index(mrt_route[num][end_index])][0])
            travel_time = int(tmp_time_list[tmp_mrt_route.index(mrt_route[num][end_index])][0]) - int(tmp_time_list[tmp_mrt_route.index(mrt_route[num][start_index])][1])
            origin_station = mrt_route[num][start_index]
            des_station = mrt_route[num][end_index]
            if line_count == 1 and len(com_origin) > 0:
                start_time = com_start_time
                origin_station = com_origin[0]
            if line_count == len(user_route) and len(com_des) > 0:
                end_time = com_end_time
                des_station = com_des[-1]
            start_time =  str(datetime.datetime.fromtimestamp(start_time))
            end_time = str(datetime.datetime.fromtimestamp(end_time))
            #issue!
            if type(route_name) == type("type"):
                temp_route_name = route_name
            else:
                temp_route_name = route_name[num]
            trip_str += str(user_imsi) + ';' + temp_route_name + ';' + str(start_time) + '%'+str(end_time)+';' + str(origin_station) + '-' + str(des_station)+';'
            if line_count == 1 and len(com_origin) > 0:
                for s in com_origin:
                    trip_str += str(s) + ','

            trip_str += mrt_route[num][start_index] + ','
            for i in range(start_index+1,end_index + 1):
                trip_str += mrt_route[num][i] + ','
            if line_count == len(user_route) and len(com_des) > 0:
                for s in com_des:
                    trip_str += str(s) + ','

        trip = trip_str.split("||")
        for t in trip:
            imsi,route_name,start_end,ori_des,path = t.split(";")
            start,end = start_end.split("%")
            start = int(time.mktime(time.strptime(start, '%Y-%m-%d %H:%M:%S')))
            end = int(time.mktime(time.strptime(end, '%Y-%m-%d %H:%M:%S')))
            ori,des = ori_des.split("-")
            path = path.split(",")
            mrt_trip_result.append( [imsi,start,end,ori,des] )
            mrt_trip_path.append( [imsi,start,end] )
            for p in path:
                mrt_trip_path[-1].append(p)

    return mrt_trip_result,mrt_trip_path
	


    
