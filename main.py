from ftplib import FTP
import datetime as dt
from mod.data_handler import *
import os 
import shutil
import sys

import time as t


# do instancing a conf object with the cinfiguration data defined in
# the configuration file 
conf = ConfigFile('./config.conf')


# get the definition of parameter selection from configuration file
PARAM_NAMES = conf.get_param_definition()



# make a buffer directory if it doesn't exist already for cache 
# extracted data if FTP-Server is not available
if os.path.isdir('./buffer') == False: 
    os.mkdir('./buffer')
    
    
        
BUFFER_DIR = './buffer'
### !!! permissions aender !!!
os.chmod(BUFFER_DIR, 0o774)



# do instancing a error log object for reporting runtime errors
err_log_obj = Log('./err_log_.log')
err_log_obj.write_date_time()




data_loger_file = '../../Datenlogger-Simulator/time_line.txt'
if os.path.isfile(data_loger_file):
    log_data = File(data_loger_file)       
    encoding = log_data.get_encoding()
    if encoding == 'error':
        err_log_obj = Log('./err_log_.log')
        err_log_obj.write_date_time()
        err_log_obj.err(code=1)
        sys.exit()
        
else:
    err_log_obj = Log('./err_log_.log')
    err_log_obj.write_date_time()  

    err_log_obj.err(code=0)
    sys.exit()




# get the last date/time stamp as well the last header
if os.path.isfile('./init.in'):
    last_date_time_stamp    = DateTimeStamp('./init.in')
    lst_dt_tm_stmp, lst_hdr = last_date_time_stamp.get_lst_dt_tm_tmp_frm_init()
    
else:
    err_log_obj = Log('./err_log_log')
    err_log_obj.write_date_time()
    err_log_obj.err(code=2)
    sys.exit()




EXTRACTION = []
new_header = 'empty'

flag = 'standby'

try:
    with open(log_data.src_path, 'r', encoding=encoding) as log_data_input:
        for line in log_data_input.readlines():
            dt_tm_stmp = DateTimeStamp.get_date_time_stamp(line)
        
        
            if flag == 'standby':
                if lst_dt_tm_stmp == ['NULL']:
                    flag = 'go'
            
                if dt_tm_stmp == lst_dt_tm_stmp:
                    flag = 'go'
                    continue
            
            
            if flag == 'go' and Header.is_header(line) == True:                
                new_header = line
                EXTRACTION.append(line)

            
            if  flag == 'go' and Header.is_header(line) == False:
                EXTRACTION.append(line)


         
except UnicodeDecodeError:
    err_log_obj = Log('./err_log_.log')
    err_log_obj.write_date_time()
    err_log_obj.err(code=1)
    sys.exit()    
            
            
            
        
            
  
# if there are no new gage data because the gage recorder is down
# this will be loged here
if EXTRACTION == []:

    with open('./GAUGE_STOP.log', 'a') as output:
        now   = dt.datetime.now()
        stamp = now.isoformat()
        stamp = stamp.replace('T', ' ' )
       
        output.write(''.join(['*' for i in range(80)]) + '\n\n')
        output.write(stamp + '\n')
        output.write('\nThere are no new data in this record period\n')
        
        sys.exit()
        
        
# overwrite the init data with the new initial date time stamp and header
with open('./init.in', 'w') as output:
    # print note
    Init.print_attention(output)


    # overwrite the old timestamp with the new one
    output.write('LAST_TIME_STAMP=' + '\t'.join(dt_tm_stmp) + '\n')
    # overwrite the old header with new one if exists
    # outherwise write the oldest known header
    if new_header != 'empty' or new_header != 'NULL':
        output.write('LAST_HEADER=' + new_header)
    else:
        output.write('LAST_HEADER=' + lst_hdr)


  
# write the extracted data as CSV file 

with open('./extraction.txt', 'w') as output:
    if Header.is_header(EXTRACTION[0]):
        for line in EXTRACTION:
            output.write(line)
    else: 
        output.write(lst_hdr + '\n')
        for line in EXTRACTION:
            output.write(line)
    
    
   



   
################################ FTP-TRANSFER #################################    



   
   
# do instancing a new ftp client object   

ftp_client = FTP_CLIENT()


# setting attributes (network access data) by using the config object and it's
# corresponding methods

ftp_client.ip_host   = conf.host()
ftp_client.port      = conf.port()
ftp_client.ip_client = conf.client()
ftp_client.passwd    = conf.passwd()

CON = ftp_client.send_file_to_server('./extraction.txt')


#### ::::::::::::::::  case of unavalable FTP-Server  ::::::::::::::: ####

buffer_dir = BUFFER_DIR + '/temp_buffer_dir'
if os.path.isdir(buffer_dir) == False:
    os.mkdir(buffer_dir)
    # change permissions to rwxrwxr--
    os.chmod(buffer_dir, 0o774)


if CON == 'connection_error':
    err_log_obj = Log('./err_log_.log')
    err_log_obj.write_date_time()  
    err_log_obj.err(code=3)
         
        
    N_buffer_files = len(os.listdir(buffer_dir))
    if N_buffer_files == 0:
        os.rename('./extraction.txt', buffer_dir + '/extraction_' + str(1).zfill(4) + '.txt')
        os.chmod(buffer_dir + '/extraction_' + str(1).zfill(4) + '.txt', 0o774)

    else:
        os.rename('./extraction.txt', buffer_dir + '/extraction_' + str(N_buffer_files + 1).zfill(4) + '.txt')
        os.chmod(buffer_dir + '/extraction_' + str(N_buffer_files + 1).zfill(4) + '.txt', 0o774)

     
else:
    
    #--------------------- auslagern bzw. die Zugangsdaten über config einladen !!!!

    if os.path.isdir(buffer_dir):
 
        conn = FTP()
        conn.connect('192.168.8.104', 2000)
        conn.login('192.168.8.104', 'passwd')
     
    
        FILE_NAMES = os.listdir(buffer_dir)
        for fname in FILE_NAMES:
            if os.path.isfile(buffer_dir + '/' + fname):
                print(buffer_dir + '/' + fname)
                conn.storbinary('STOR ' + fname, open('./buffer/temp_buffer_dir/' + fname, 'rb'))
                
  
        shutil.rmtree(buffer_dir)
    
            
     
sys.exit()














    