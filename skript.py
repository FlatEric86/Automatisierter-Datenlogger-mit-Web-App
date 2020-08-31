#!/usr/bin/python3

from modul.bib import *
import mysql.connector
import os, sys


# check if there are new data in this actuel service period
# if not, close application
if os.path.isfile('/media/sql_db_at_usb/_WURMLOCH_/extraction.txt') == False:
	print('NULL_RUN')
	sys.exit()
else:
	print('INJECTION_RUN')
	

# do instancing a config object with it's config file path
config = Config('/home/pi/Desktop/SQL_INJECTOR/data_to_sql.confg')



# do instancing a mysql API object with necessary access attributes
mydb = mysql.connector.connect(host     = config.host(),
                               user     = config.user(),
                               passwd   = config.passwd(),
                               database = config.database()
)



# declare the source path to input file
src_path = '/media/sql_db_at_usb/_WURMLOCH_/extraction.txt'

# do instancing a file object
file = File()

# set the src_path as attribute of the file object
file.src_path = src_path

# use get_encoding() method to check for the encoding kind of inputfile
encoding = file.get_encoding()





with open(file.src_path, 'r', encoding=encoding) as input:
    
    # do instancing a MySQL object
    MySQL_object = MySQL()
    
   
    # give over the parameter selection definition from config object
    MySQL_object.param_extraction_defin = config.param_selection()


    
    for line in input.readlines():

        # check if line is a header line
        if Header(line).is_header():
        
            # define a line list object with all items of header 
            header_line = Line(line).get_line_items()
 
            
            # give over the header line object as attribut to the MySQL object instance
            MySQL_object.header_line_list = header_line
            
            
            # give over the "header item to index map" as attribute to the mySQL object
            MySQL_object.item_index_map = Header(header_line).get_header_items_to_indizes_map()


            
        # BEING NOW IN A DATA LINE
        else:
            
            # do instancing a LINE-object
            data_line = Line(line).get_line_items()

            # give over the actual line object to the MySQL-object
            MySQL_object.clmn_line_list = data_line
            
            # get the actual MySQL inload query for the actually line object
            inload_query = MySQL_object.get_MySQL_inload_query()



            # >>> submit data into the corresponding MySQL database tables <<< #
            
             # instanting of a new courser object
            mycursor = mydb.cursor()
             # giver over the actually inload query
            mycursor.execute(inload_query)
             # trigger the query
            mydb.commit()

            
            
            #------------------------------------------------------------------
            
            ##### make a SQL-CMD to create a new table
            ## for more detail, plaese have a look at the description
            ## -> help(MySQL)
            ## MySQL_object.make_create_mysql_table_cmd()

            
            

            ##### make a test SQL-query for input data of actual line
            ## MySQL_object.make_test_input_mysql_cmd()
            

# Do store the actually extraction file as backup in the hidden directory ./.BAK with 
# enumerating suffix and 

with  open('/media/sql_db_at_usb/counter.txt', 'r') as last_counter:
	last_counter = last_counter.readline()
	last_counter = last_counter.strip('\n').split('=')[-1]
	
	actl_counter = int(last_counter) + 1
	
	os.rename('/media/sql_db_at_usb/_WURMLOCH_/extraction.txt', '/media/sql_db_at_usb/data_bak/extraction' + '_' + str(actl_counter) + '.txt')

	with open('/media/sql_db_at_usb/counter.txt', 'w') as output:
		output.write('COUNTER=' + str(actl_counter) + '\n')




