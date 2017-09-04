import sqlite3
import os, sys, errno


def main():
    with sqlite3.connect("./CHT.db") as connection:
        print "open database"

        #input_folder = raw_data_path
        date_list = os.listdir(os.path.join('data', 'raw_data'))
        for date in date_list:
            sql_text = "select distinct imsi from t_%s"%(date)
            print sql_text
            cursor = connection.execute(sql_text)

            result = []
            for row in cursor:
                print row
                result.append(row)

            result = set(result)
            print date, "# of users:",len(result)
            try:
                os.makedirs(os.path.join("./data/user_data",date))
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            for user in result:
                sql_text = "select * from t_%s where imsi = \"%s\""%(date,str(user[0]))
                print sql_text
                cursor = connection.execute(sql_text)
                with open(os.path.join("./data/user_data",date,"u_"+str(user[0])),"w+") as f:
                    for row in cursor:
                        row = [str(item) for item in row]
                        f.write("|".join(row))
                        f.write("\n")
    if connection:
        connection.close()


if __name__ == "__main__":
    #raw_data_path = sys.argv[1]
    main()
