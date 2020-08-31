#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
############################# // File class // ##############################
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
############################## // Line class // ###############################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  
class Line:
    
    
    def __init__(self, line=None):
        self.line  = line
        
    
    def get_line_items(self):
        '''
        returns the line as a list object with well formated items
        It means that a by formatstrings induced itemname like
        for instance "  itemname " gets renamed to "itemname".
        Note the blanks in "  itemname ".
        '''
    
        line = self.line.strip('\n').split('\t')
        
        ### remove blanks at beginning or end of item
        line_new = []
        for item in line:
            line_new.append(item.replace(' ', ''))
        
        del line
        
        return line_new
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
############################# // CONFIG_FILE // ###############################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
        
class Config:

    def __init__(self, src_path):
        self.src_path = src_path
        
        
        
        
    def __get_config(self):
        def cleanItem(item):
            return item.replace(' ','')
    
        param_dict = { 'HOST'    : 0,
                       'USER'    : 1,
                       'PWD'     : 2,
                       'DB_NAME' : 3,
        }
        
        
        params = ['host_dummy', 
                  'user_dummy',
                  'pwd_dummy',
                  'db_name_dummy'              
        ]
        
        flag = 0
        with open(self.src_path, 'r') as input:
            for line in input.readlines():
            
                if line.startswith('//') or line.startswith('~'):
                    continue
                    
                else:
                    line = line.strip('\n').split('=')
                    line = [cleanItem(item) for item in line]
                    
                    if ']' in line:
                        break
                    
                    
                    for key in param_dict:
                        if key in line:
                            params[param_dict[key]] = line[1]
                            
                    if 'SELECTION' in line:
                        flag = 'go'
                        continue
                        
                        
                    if flag == 'go' and line != [''] and line != [']']:
                        params.append(line[0])
                        
        return params
        
        
        
    def host(self):
        return self.__get_config()[0]
        
    def user(self):
        return self.__get_config()[1]
        
    def passwd(self):
        return self.__get_config()[2]
        
    def database(self):
        return self.__get_config()[3]

    def param_selection(self):
        return self.__get_config()[4:]
        
    
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
############################# // MySQL class // ###############################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
        
class MySQL:
    '''
    This class represents the kernel of the main script.
    '''
  

    
    def __init__(self,
                 make_table_target_path = None,
                 header_line_list       = None, 
                 clmn_line_list         = None,
                 make_input_target_path = None,
                 item_index_map         = None,
                 param_extraction_defin = None
    ):

        '''
        ATRIBUTES OF MySQL class:
            -> make_table_target_path
                defines the target path of a file for make a 
                SQL promt tamplate to create a new SQL table
                This atribut is associated with the 
                make_create_mysql_table_cmd()-method
                
            -> header_line_list
                the list of the items of a header line which
                is produced in loopproces over the inputfile reading
                
            -> clmn_line_list
                is the list of items of a line if she is not a header line
                
            -> make_input_target_path
                defines the target path of a test file in form of 
                a SQL promt to input data in a table
                
            -> item_index_map 
                is the outside of this class produced
                map which maps the parameter name as key
                to a column index for indexing.
                
            -> param_extraction_defin
                is a list of valid parameternames (keys) that have 
                to be defined in main script to let the injector()-method
                know, which parameters of a column line are be significant.
            
        '''
       
        self.make_table_target_path = make_table_target_path
        self.header_line_list       = header_line_list
        self.clmn_line_list         = clmn_line_list
        self.make_input_target_path = make_input_target_path
        self.item_index_map         = item_index_map
        self.param_extraction_defin = param_extraction_defin
            
    def make_test_input_mysql_cmd(self, target_path=None):
        '''
        Method to generate a testinput file in form of a 
        SQL promt to insert values into a given table.
        The output path can be defined by the make_input_target_path-atribute
        If it was not defined, the method will use a dummy path
        named "'./MySQL_CREATE_INPUT_CMD.txt'"
        '''
    
        EXCEPT_NAMES = ['Datum', 'Zeit', 'Status']
    
        if target_path == None:
            target_path = './MySQL_CREATE_INPUT_CMD.txt'    

        with open(target_path, 'w') as output:
            
            i = 0
            while True:
            
            
                if i == 0:
                    output.write('INSERT INTO $gauge_i$(\n')
                if i == 1:
                    output.write('\nVALUES(\n')
                    
                    
                j = 0
                for item_name in self.param_extraction_defin:
                    if i == 0:
                        if j < len(self.param_extraction_defin)-1:
                            output.write(item_name + ', \n')
                        else:
                            output.write(item_name + ' \n')
                
                    if i == 1:  
                        index = self.item_index_map[item_name]
                        
                        val = str(self.clmn_line_list[index])
                        if item_name in EXCEPT_NAMES:
                            val = "'" + val + "'"
                            
                        if j < len(self.param_extraction_defin)-1:
                            output.write(val + ', \n')                      
                        else:
                            output.write(val + ' \n') 
                        
                    j += 1   
                        
                output.write(')')
                i += 1        
                        
                if i == 2:
                    output.write(';')
                    break
                       

         
    def make_create_mysql_table_cmd(self, target_path=None):
        '''
        This Method will produce a tamplate command line for instancing
        a SQL table based on the items defined in attribute param_extraction_defin.
        Note: you have to change the table name definition, which is 
        $gauge_i$ in the generated template file.
        The argument have to be the target_path like your working directory
        example: './MySQL_CREATE_TABLE_COMMAND.txt'
        
        By default, this is also the path if you do not give over an argument:
        '''
        
        
        if target_path == None:
            target_path = './MySQL_CREATE_TABLE_COMMAND.txt'
    
        with open(target_path, 'w') as output:
            output.write('CREATE TABLE $gauge_i$ (\nid INT AUTO_INCREMENT PRIMARY KEY, ')
            
            # These Names are maped to a non numeriacal parameter
            # SQL requires for CHAR Types a length definition
            EXCEPT_NAMES = ['Status']
            length_dict = {'Datum':'10', 'Zeit':'8', 'Status':'10'}
            
            i = 0
            for name in self.param_extraction_defin:        
                
                if i == len(self.param_extraction_defin)-1:  
                    if name not in EXCEPT_NAMES:
                        output.write(name + ' FLOAT\n')
                    else:
                        output.write(name + ' CHAR' + '(' + length_dict[name] + ')\n')
                        
                else:
                    if name not in EXCEPT_NAMES:
                        output.write(name + ' FLOAT, \n')
                    else:
                        output.write(name + ' CHAR' + '(' + length_dict[name] + '),\n')                    
                           
                    
                i += 1
            output.write(');')        
        
    
    def get_MySQL_inload_query(self):
        
        
        gauge_id = self.clmn_line_list[self.item_index_map['Messstelle']]
        
        date_time = "'"                                                            \
                    +                                                              \
                    self.clmn_line_list[self.item_index_map['Datum']]              \
                    +                                                              \
                    ' '                                                            \
                    +                                                              \
                    self.clmn_line_list[self.item_index_map['Zeit']]               \
                    +                                                              \
                    "'"                                                            \
                    
                    
        # print(date_time)            
                    
        query_part_1 = "INSERT INTO gage_"                                        \
                       + gauge_id                                                  \
                       + " ("                                                      \
                       + 'Date_Time, '                                             \
                       + ', '.join([name for name in self.param_extraction_defin]) \
                       + ") VALUES "
  
        _columns_ = []
        
        
        # print(self.clmn_line_list[self.item_index_map['H2O']])
        for param_name_key in self.param_extraction_defin:

            if param_name_key != 'Status':
                val = self.clmn_line_list[self.item_index_map[param_name_key]]
            else:
                if param_name_key not in ['Datum', 'Zeit']:
                    val = "'" + self.clmn_line_list[self.item_index_map[param_name_key]] + "'"
                
            _columns_.append(val)
            
        query_part_2 = "( " + date_time + ', ' + ', '.join(_columns_) + ")"

        inload_query = query_part_1 + query_part_2 
    
    
        # print(inload_query)
    
    
        return inload_query
    
    
    
    
    
    
    
    
    
