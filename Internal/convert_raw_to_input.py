import sqlite3
import os, sys, errno
import csv
import time

def bar(i, total_i, start_t):
    tt = time.time()-start_t
    n = int(i/float(total_i)*30)
    if i == total_i:
        bar = '['+('='*30)+']'
        sys.stdout.write(' ' * 80 + '\r')
        sys.stdout.flush()
        #print('{}/{} {} - {}s\r'.format(i, total_i, bar, tt))
        print "%s/%s %s - %ss\r"%(i, total_i, bar, tt)
    elif n <= 0:
        bar = '['+('='*n)+'>'+('.'*(30-n))+']'
        sys.stdout.write(' ' * 80 + '\r')
        sys.stdout.flush()
        #sys.stdout.write('{}/{} {}\r'.format(i, total_i, bar))
        sys.stdout.write("%s/%s %s\r"%(i, total_i, bar))
    else:
        eta = int((tt/i)*(total_i-i))
        bar = '['+('='*n)+'>'+('.'*(30-n))+']'
        sys.stdout.write(' ' * 80 + '\r')
        sys.stdout.flush()
        #sys.stdout.write('{}/{} {} - ETA: {}s\r'.format(i, total_i, bar, eta))
        sys.stdout.write("%s/%s %s - ETA: %ss\r"%(i, total_i, bar, eta))
    sys.stdout.flush()
    return


def main():
    with sqlite3.connect("./CHT.db") as connection:
        print "Open database: CHT.db"
        
        input_folder = os.path.join('data', 'raw_data')
        date_list = os.listdir(input_folder)


        for date in date_list:
            print "Import data of date: %s"%(date)
            sql_text = "drop table if exists t_%s"%(date)
            connection.execute(sql_text)
            # build table
            sql_text = "create table t_{} (imsi text not null, dt text not null, lont  float not null, lat float not null, ut int not null)".format(date)
            connection.execute(sql_text)

            start_t = time.time()
            for name in os.listdir(os.path.join(input_folder, date)):
                # import data
                print "Processing: %s"%(name)
                i = 0
                f = open(os.path.join(input_folder,date,name),"r")
                reader = csv.reader(f, delimiter='|')
                total_i = len(list(reader))
                f.seek(0, 0)
                for row in csv.reader(f, delimiter='|'):
                    i += 1
                    sql_text = "INSERT INTO t_{} (imsi,dt,lont,lat,ut) VALUES (\"{}\",\"{}\",{},{},{});".format(date,row[0],row[1][:8],row[2],row[3],row[4])
                    connection.execute(sql_text)
                    bar(i, total_i, start_t)
                f.close

        start_t = time.time()
        for date in date_list:
            print "Export data of date: %s"%(date)
            sql_text = "select distinct imsi from t_%s"%(date)
            #print sql_text
            cursor = connection.execute(sql_text)

            result = []
            for row in cursor:
                #print row
                result.append(row)

            result = set(result)
            total_j = len(result)
            print "# of users: ",total_j
            try:
                os.makedirs(os.path.join("./data/user_data",date))
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            j = 0
            for user in result:
                j += 1
                sql_text = "select * from t_%s where imsi = \"%s\""%(date,str(user[0]))
                #print sql_text
                cursor = connection.execute(sql_text)
                with open(os.path.join("./data/user_data",date,"u_"+str(user[0])),"w+") as f:
                    for row in cursor:
                        row = [str(item) for item in row]
                        f.write("|".join(row))
                        f.write("\n")
                bar(j, total_j, start_t)

    if connection:
        connection.close()
    print "Data has been converted completely and write into folder user_data/"

if __name__ == "__main__":
    main()
