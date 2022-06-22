# #This script reads and updates the channel and signal 
# #strength information to the database.
import subprocess, csv, os, time
import MySQLdb, sshtunnel

class Scanner:
    scanner_pid = os.getpid()
    scan_flag = True

    #Scanning based on central frequency and bandwidth
    def rf_sweep(self,central_freq,bw,bin):
        min_freq = central_freq-bw//2
        max_freq = central_freq+bw//2

        parsed_rf = []
        sig_str_info = []
        # rf_scan = subprocess.check_output(['hackrf_sweep', '-1', '-f %d:%d'%(min_freq,max_freq), '-w %d'%(bin*1000000),'/dev/null'],stderr=subprocess.DEVNULL)
        rf_scan = subprocess.check_output(['hackrf_sweep -1 -f %d:%d -w %d /dev/null'%(min_freq,max_freq,bin*1000000)],stderr=subprocess.DEVNULL)
        rf_scan = rf_scan.decode('utf-8')
        rf_scan = rf_scan.split('\n')[:-1]
        for rec in rf_scan:
            rec = rec.split(',')
            rec = rec[2:4]+rec[6:]
            parsed_rf.append(rec)

        #Sort parsed frequencies in ascending order
        parsed_rf.sort(key=lambda x:int(x[0]))

        for rf in parsed_rf:
            sig_str_info.extend(rf[2:])
        
        #add channel information to each signal strength
        #channel = subfrequencies below each freqeuncy range; 5MHz/(binsize) 
        for ind in range(len(sig_str_info)):
            chan = min_freq + bin*ind
            strength = sig_str_info[ind]
            sig_str_info[ind] = (str(chan),strength)
        # print("sig_str_info: ", sig_str_info)
        return sig_str_info
        ## each signal strengths represent the values at start of each range; this means that the last frequency (maximum frequency will not have a signal strength)

    #Scanning based on start & end frequency
    def rf_sweep_start_end(self, min_freq, max_freq, bin):
        parsed_rf = []
        sig_str_info = []
        # rf_scan = subprocess.check_output(['hackrf_sweep', '-1', '-f %d:%d'%(min_freq,max_freq), '-w %d'%(bin*1000000),'/dev/null'],stderr=subprocess.DEVNULL)
        rf_scan = subprocess.check_output(['hackrf_sweep -1 -f %d:%d -w %d /dev/null'%(min_freq,max_freq,bin*1000000)],stderr=subprocess.DEVNULL)
        rf_scan = rf_scan.decode('utf-8')
        rf_scan = rf_scan.split('\n')[:-1]
        for rec in rf_scan:
            rec = rec.split(',')
            rec = rec[2:4]+rec[6:]
            parsed_rf.append(rec)

        #Sort parsed frequencies in ascending order
        parsed_rf.sort(key=lambda x:int(x[0]))

        for rf in parsed_rf:
            sig_str_info.extend(rf[2:])
        
        #add channel information to each signal strength
        #channel = subfrequencies below each freqeuncy range; 5MHz/(binsize) 
        for ind in range(len(sig_str_info)):
            chan = min_freq + bin*ind
            strength = sig_str_info[ind]
            sig_str_info[ind] = (str(chan),strength)
        # print("sig_str_info: ", sig_str_info)
        return sig_str_info
        ## each signal strengths represent the values at start of each range; this means that the last frequency (maximum frequency will not have a signal strength)


    #Function used to generate csv file used as sample data when running front-end without connection to idciti_drone_defense database
    def rf_sweep_n_write(self,central_freq,bw,bin):
        min_freq = central_freq-bw//2
        max_freq = central_freq+bw//2

        parsed_rf = []
        sig_str_info = []
        rf_scan = subprocess.check_output(['hackrf_sweep', '-1','-f %d:%d'%(min_freq,max_freq), '-w %d'%(bin*1000000),'/dev/null'],stderr=subprocess.DEVNULL)
        rf_scan = rf_scan.decode('utf-8')
        rf_scan = rf_scan.split('\n')[:-1]
        for rec in rf_scan:
            rec = rec.split(',')
            rec = rec[2:4]+rec[6:]
            parsed_rf.append(rec)

        #Sort parsed frequencies in ascending order
        parsed_rf.sort(key=lambda x:int(x[0]))

        for rf in parsed_rf:
            sig_str_info.extend(rf[2:])
        
        #add channel information to each signal strength
        #channel = subfrequencies below each freqeuncy range; 5MHz/(binsize) 
        for ind in range(len(sig_str_info)):
            chan = min_freq + bin*ind
            strength = sig_str_info[ind]
            sig_str_info[ind] = (str(chan),strength)
        # print("sig_str_info: ", sig_str_info)
        with open('2400_4.csv','w') as f:
            writer = csv.writer(f)
            for signals in sig_str_info:
                writer.writerow(signals)
        ## each signal strengths represent the values at start of each range; this means that the last frequency (maximum frequency will not have a signal strength)

    #Update parsed frequency information (channel & signal strength) into local database
    def update_db(self, SSH_CONFIG, DB_CONFIG,freq_info,init_flag):
        #Establish ssh tunnel
        ssh_host = SSH_CONFIG[0]
        ssh_user = SSH_CONFIG[1]
        ssh_pw = SSH_CONFIG[2]
        tunnel = sshtunnel.SSHTunnelForwarder(
            (ssh_host,22),
            ssh_username = ssh_user,
            ssh_password = ssh_pw,
            remote_bind_address=('127.0.0.1',3306)
        )

        tunnel.start()

        #Connect to DB
        local_host = DB_CONFIG[0]
        local_user = DB_CONFIG[1] 
        local_passwd = DB_CONFIG[2]
        local_db = DB_CONFIG[3] 
        local_port = DB_CONFIG[4] 

        local_conn = MySQLdb.connect(host = local_host,
                                    user = local_user,
                                    passwd = local_passwd,
                                    port = tunnel.local_bind_port)
        local_cursor = local_conn.cursor(MySQLdb.cursors.DictCursor)
        
        #Load the database & check if a table for given central frequency exists
        local_cursor.execute("USE idciti_drone_defense")
        local_conn.commit()


        local_cursor.execute("SHOW TABLES")
        tables = local_cursor.fetchall()
        local_conn.commit()

        table_name = "signal_str"

        if init_flag and {'Tables_in_idciti_drone_defense':'%s'%(table_name)} in tables:
            print("Dropping old signal strength record")
            drop_query = "drop table signal_str;"
            local_cursor.execute(drop_query)
            local_conn.commit()

            tables = list(tables)
            tables.remove({"Tables_in_idciti_drone_defense":"signal_str"})

        #Create & populate the table if none already exists; otherwise, update each channel accordingly
        #Table name cannot consist only of numbers, so _mhz must be added.
        if {'Tables_in_idciti_drone_defense':'%s'%(table_name)} in tables:
            print("Updating table %s"%(table_name))
            bulk_upload_query = "UPDATE signal_str SET y = CASE "
            channels = "("
            for info in freq_info[0]:
                case_str = "WHEN x = %s THEN %s "%(info[0],info[1])
                bulk_upload_query+=case_str
                channels+="%s, "%info[0]
            channels = channels[:-2]+")"
            bulk_upload_query+="END WHERE x IN %s"%channels
            # print("bulK : ", bulk_upload_query)
            local_cursor.execute(bulk_upload_query)
            local_conn.commit()
            # for record in freq_info[0]:
            #     local_cursor.execute("UPDATE %s SET sig_str = %f WHERE channel = %s"%(table_name,float(record[1]),record[0]))
            #     local_conn.commit()
            # if table_name != 'full_range':
            #     for record in freq_info[0]:
            #         local_cursor.execute("UPDATE full_range SET sig_str = %f WHERE channel = %s"%(float(record[1]),record[0])))
            #         local_conn.commit()

        else:
            print("Creating table %s"%(table_name))
            local_cursor.execute("CREATE TABLE %s(x INT, y FLOAT)"%(table_name))
            local_conn.commit()

            insert_query = "INSERT INTO %s VALUES "%(table_name)
            for record in freq_info[0]:
                insert_query += "(%s,%s),"%(record[0],record[1])
            #remove the last comma
            insert_query = insert_query[:-1]
            # print("insert: ", insert_query)
            local_cursor.execute(insert_query)
            local_conn.commit()
        local_conn.close()
        tunnel.close()


    #Scanning frequency based on central frequency and bandwidth;
    #Less likely to be used- recommended to use freq_scan_start_end. It's more intuitive
    def freq_scan(self, SSH_CONFIG, DB_CONFIG, central_freq, bw, bin, init_flag):
        #This function continuosly scans the selected frequency range && updates this data to the local DB
        #This function triggers both the frequency scan function along with the db update function.

        central_freq = int(central_freq)

        bw = int(bw)
        bin = int(bin)
        while True:
            startTime = time.time()
            freq_info = self.rf_sweep(self,central_freq,bw,bin)
            # print("freq_info : ", freq_info)
            self.update_db(self, SSH_CONFIG, DB_CONFIG, [freq_info], init_flag)
            print("Elapase : ", time.time()-startTime)
            if self.scan_flag == False:
                break

    def freq_scan_start_end(self, SSH_CONFIG, DB_CONFIG, min_freq, max_freq, init_flag):
        #This function continuosly scans the selected frequency range && updates this data to the local DB
        #This function triggers both the frequency scan function along with the db update function.

        self.scan_flag = True

        while self.scan_flag:
            start_time = time.time()
            bin = (max_freq-min_freq)//5000
            freq_info = self.rf_sweep_start_end(self,min_freq,max_freq,bin)
            self.update_db(self, SSH_CONFIG, DB_CONFIG, [freq_info], init_flag)
            print("elapse: ", time.time()-start_time)

    def init_table(self, SSH_CONFIG, DB_CONFIG):
        self.scan_flag = False
        self.freq_scan(self, SSH_CONFIG, DB_CONFIG,2716, 4606, 1, 1)
