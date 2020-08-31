import datetime as dt
from ftplib import FTP
import time as t

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
############################# // FTP  class // ################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class FTP_CLIENT:
    
    def __init__(self, ip_host=None, port=None, ip_client=None, passwd=None):
        
        self.ip_host   = ip_host
        self.port      = port
        self.ip_client = ip_client
        self.passwd    = passwd
        
        
    def send_file_to_server(self, file_ref=None):  
    
        delay       = 0.1
        max_retries = 5
    
        retry = 0
        while retry < max_retries:
            try:
                ftp = FTP()       
                ftp.connect(self.ip_host, self.port)       
                ftp.login(self.ip_client, self.passwd)
                ftp.storbinary('STOR '+ file_ref, open(file_ref, 'rb'))
                ftp.quit()
                break
                
            # case of server binding problems
            except IOError as conn_err:
                t.sleep(delay)
                retry += 1
                
            # the return value will induce a buffer storing of the extracted
            # data until the FTP-Server is available again. See main script.
            if retry == max_retries:
                return 'connection_error'
        


        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
############################# // File class // ################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class File:

    def __init__(self, src_path=None):
        self.src_path = src_path

    def get_encoding(self):
        '''
        returns the ASCII encoding of the File-object.
        It's a predebug for the case, that the encoding format of the 
        ASCII file was changed.
        '''
        
    
        try:
            with open(self.src_path, 'r', encoding = 'utf8') as input:
                line = input.readline()
                encoding = 'utf8'
                
        except UnicodeDecodeError:
            try:
                with open(self.src_path, 'r', encoding = 'latin-1') as input:
                    line = input.readline()
                    encoding = 'latin-1' 
                    
            except UnicodeDecodeError:
                try:
                    with open(self.src_path, 'r', encoding = 'ISO-8859-1') as input:
                        line = input.readline()
                        encoding = 'ISO-8859-1'    
                        
                except UnicodeDecodeError:
                    import time as t 
                    
                    print(''.join(['!' for i in range(80)]))
                    print("Can't decode data file !!!")
                    print('Please check the file encoding and add here the encoding style')
                    print(''.join(['!' for i in range(80)]))
                    t.sleep(30)
                    

        return encoding  
        
        
        
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
############################# // Header class // ##############################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



class Header:

    def __init__(self, line=None):
        self.line = line



             
    def is_header(self):
    
        '''
        checks if a corresponded line object is a header line, or not.
        '''
        
        if 'Messstelle' in self.line:
            return True
        else:
            return False
 
         
         
    def get_header_items_to_indizes_map(self):
    
        '''
        returns a dictionary with a mapping of the header items to it line index
        in order of them sequence.
        Every parameter got an index induced by its sequence in line.
        An important faeture is, that equal meta parameter names get renamed.
        For explaination: One of the metaparameter names is "Einheit".
        It occours for each substance parameter. The proble is, SQL needs
        unique key names for mapping columns by key names. 
        To prevent corrersponding errors, these mete parameternames are renamed
        in the old name with the corresponding substance name suffix.
        If substance name is "H2O" than "Einheit" -> "Einheit_H2O".
        '''
    
        MAP = {}
        
        i = 0
        for item in self.line:
            if item == 'Einheit':
                item = self.line[i-1] + '_' + item
            if item == 'Rest':
                item = self.line[i-3] + '_' + item
            if item == 'Kompensation':
                item = self.line[i-2] + '_' + item
               
            MAP.update({item:i})
            
            i += 1
            
        return MAP    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
############################# // CONFIG_FILE // ###############################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  

        

class ConfigFile:

    def __init__(self, src_path):
        self.src_path = src_path

    def __get_config(self):

        param_dict = { 'HOST'    : 0,
                       'PORT'    : 1,
                       'CLIENT'  : 2,
                       'PASSWD'  : 3,
        }

        params = ['host_dummy', 
                  'port_dummy',
                  'client_dummy',
                  'passwd_dummy'              
        ]

        
        with open(self.src_path, 'r') as input:
            for line in input.readlines():
                if line.startswith('//') or line.startswith('~'):
                    continue
                else:
                    line = line.strip('\n').split('=')
                    if line == ['']:
                        continue
                    else:
                        for key in param_dict:
                            if key == line[0].strip(' '):
                                params[param_dict[key]] = line[-1].strip(' ')

        return params
        
        

    def get_param_definition(self):
    
        PARAM_NAMES = []
    
        flag = 'standby'
        with open(self.src_path, 'r') as input:
            for line in input.readlines():
                if line.startswith('SELECTION'):
                    flag = 'go'
                    continue
                    
                if flag == 'go' and line.startswith(']') == False:

                    PARAM_NAMES.append(line.strip('\n'))
                                 
        return PARAM_NAMES
                        
                


    def host(self):
        return self.__get_config()[0]

    def port(self):
        return int(self.__get_config()[1])

    def client(self):
        return self.__get_config()[2]

    def passwd(self):
        return self.__get_config()[3]
        



class Header:

    def is_header(line):
        
        if line.startswith('Messstelle'):
            return True
        else:
            return False
    
    
    
class DateTimeStamp:
    
    def __init__(self, src_path=None):
        self.src_path = src_path

    
    def get_date_time_stamp(line):
        
        DATE_TIME_STAMP = ['date', 'time']
        
        line = Line(line).get_line_items(sep='\t')
        
        DATE_TIME_STAMP[0] = line[1]
        DATE_TIME_STAMP[1] = line[2]
        
        return DATE_TIME_STAMP
    
    
    def get_lst_dt_tm_tmp_frm_init(self):
    
        with open(self.src_path, 'r') as input:
            for line in input.readlines():
                if line.startswith('//') or line == '\n':
                    continue
                line = line.strip('\n').split('=')
                
                if 'LAST_TIME_STAMP' in line:
                    dt_tm_stmp = line[-1].split('\t')
                    
                if 'LAST_HEADER' in line:
                    lst_hdr = line[-1]
    
        return dt_tm_stmp, lst_hdr
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
############################## // File class // ###############################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



class File:

    def __init__(self, src_path=None):
        self.src_path = src_path


    def get_encoding(self):

        '''
        returns the ASCII encoding of File instance.
        '''


        ENCODINGs = ['utf8', 'ISO-8859-1', 'latin-1']
        _encoding = 42
        
        i = 0
        while True:
            if i == len(ENCODINGs):
                return 'error'
                break
            try:
                with open(self.src_path, 'r', encoding=ENCODINGs[i]) as input:
                    _encoding = ENCODINGs[i]
                    pass
       
            except UnicodeDecodeError:
                continue       

            else:
                _encoding = ENCODINGs[i]
                break
            i += 1

        return _encoding  
 

 
        
class Init:

    def print_attention(target):
        target.write(''.join(['!' for i in range(80)]))
        target.write('\n')
        target.write('// ACHTUNG !!!')
        target.write('\n')
        target.write(''.join(['!' for i in range(80)]))
        target.write('\n\n//Nach Reaktivierung des Messwerteloggers muessen die Werte\n'
               + '//LAST_TIME_STAMP und LAST_HEADER auf den Wert "NULL" gesettet werden' 
        )
        target.write('\n')
        target.write('//Beispiel:\n')
        target.write('//LAST_TIME_STAMP=NULL\n')
        target.write('//LAST_HEADER=NULL')
        target.write('\n\n')
        target.write('//Es duerfen keine Leerzeichen zwischen Variablenname und "=" sowie "="\n'
              + '//und Wert sein !!!'
        )
        target.write('\n')
        target.write('//Nach dem letzten Ausdruck (LAST_HEADER=NULL) muss ein Zeilenumbruch folgen')
        target.write('\n\n')
        target.write(''.join(['!' for i in range(80)]))
        target.write('\n\n\n')
        
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
############################## // Line class // ###############################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  

class Line:

    def __init__(self, line=None):
        self.line  = line

       
    def get_line_items(self,sep=None):

        '''
        returns the line as a list object with well formated items
        It means that a by formatstrings induced item name like
        for instance "  itemname " gets renamed to "item name".
        Note the blanks in "  item name ".
        '''

        if sep == None:
            line = self.line.strip('\n').split(' ')
        else:
            line = self.line.strip('\n').split(sep)

        
        ### remove blanks at beginning or end of item
        line_new = []

        for item in line:
            if item != '':
                line_new.append(item.strip(' '))

        del line

       
        return line_new    
        
  

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
############################ // extractor class // ############################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  

# class Extractor:


    # def __init__(self, )




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
############################ // ERR_LOG class // ##############################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   


    
class Log:
    
    def __init__(self, log_path=None):
        self.log_path = log_path

    def write_date_time(self):

        now   = dt.datetime.now()
        stamp = now.isoformat()
        stamp = stamp.replace('T', ' ' )
        with open(self.log_path, 'a') as log_obj:
            log_obj.write('\n\n')
            log_obj.write(''.join(['~' for i in range(80)]))
            log_obj.write('\n\n')
            log_obj.write('DATE: ' + stamp)


    def err(self,code=None):
        
        if code == 0:
            with open(self.log_path, 'a') as log_obj:
                log_obj.write('\nERR: 0\n\n')
                log_obj.write('The datalog file seems not to be exist.\n')
                log_obj.write('Please check for the file and the correct path.\n')
                
        if code == 1:
            with open(self.log_path, 'a') as log_obj:
                log_obj.write('\nERR: 1\n\n')
                log_obj.write('The datalog file can not be encoded.\n')
                log_obj.write('Maybe you have changed the ASCII encoding.\n')
                log_obj.write('Allowed are only utf-8, latin-1 and ISO-8859-1.\n')
 
        if code == 2:
            with open(self.log_path, 'a') as log_obj:
                log_obj.write('\nERR: 2\n\n')
                log_obj.write('The initialization file do not exists.\n')
                log_obj.write('Please make shure that the init.in file is in the main directory\n')
                log_obj.write('Chec the documentation for make a new file.\n')
                
        if code == 3:
            with open(self.log_path, 'a') as log_obj:
                log_obj.write('\nERR: 3\n\n')
                log_obj.write('The FTP-Server could not be connected.\n')
                log_obj.write('Have stored the extraction file into the buffer directory\n')            
                
                
 
    
    
        
        