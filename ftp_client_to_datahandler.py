

from ftplib import FTP
import os


ftp = FTP()
ftp.connect('192.168.8.101', 2000)

ftp.login('192.168.8.104', 'passwd')




dir = './'

FILE_NAMES = os.listdir(dir)

print(FILE_NAMES)

for file_name in FILE_NAMES:
    if file_name == 'extraction.txt':
        src_path = dir + file_name
        print('rwgfjerqijgiojegoj')
        with open(src_path, 'rb') as file:
            ftp.storbinary('STOR ' + src_path, file)
            pass
    
ftp.quit()
