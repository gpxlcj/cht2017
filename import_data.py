import sqlite3
import os, sys
import csv

def main():
    with sqlite3.connect("./CHT.db") as connection:
        print "open database"

        #input_folder = raw_data_path
        input_folder = os.path.join('data', 'raw_data')
        date_list = os.listdir(input_folder)
        for date in date_list:
            sql_text = "drop table if exists t_%s"%(date)
            connection.execute(sql_text)
            print sql_text
            # build table
            sql_text = "create table t_{} (imsi text not null, dt text not null, lont  float not null, lat float not null, ut int not null)".format(date)
            connection.execute(sql_text)
            print sql_text

            for name in os.listdir(os.path.join(input_folder, date)):
                # import data
                with open(os.path.join(input_folder,date,name),"r") as tsv: 
                    for row in csv.reader(tsv, delimiter='|'):
                        sql_text = "INSERT INTO t_{} (imsi,dt,lont,lat,ut) VALUES (\"{}\",\"{}\",{},{},{});".format(date,row[0],row[1][:8],row[2],row[3],row[4])
                        print sql_text
                        connection.execute(sql_text)
    if connection:
        connection.close()

if __name__ == "__main__":
    #raw_data_path = sys.argv[1]
    main()
