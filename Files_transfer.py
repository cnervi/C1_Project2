import os
import logging
import time
import schedule
import shutil
from ftplib import FTP


logging.basicConfig(filename='download.log', level=logging.INFO)


def download_files(user, password, remote_dir, local_dir, destination):
    '''
    It connects to an external FTP server, and retrieves a list of files in a specific directory.
    It checks if a local directory where the files will be saved exists, If not it raises an exception.
    It goes through the files on the FTP server, and downloads them to the local directory.
    Finally, it moves the files from the local directory to an internal network destination.
    '''
    try:
        ftp = FTP(host)
        ftp.login(user=user, passwd=password)
        logging.info(f'The connection is established.')
        if os.path.exists(local_dir) is not True:
            directory = "Files"
            parent_dir = "/Users/Alexandra/Desktop/"
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)
        ftp.cwd(remote_dir)
        files = ftp.nlst()
        for file_name in files:    
            if ftp.size(file_name) <= 10485760:             #In order not to download very large files.
                logging.info(f'Downloading... {file_name}')
                ftp.retrbinary('RETR %s' %file_name,
                               open(os.path.join(local_dir, file_name), 'wb').write)
        ftp.close()
    except Exception as e:
        logging.error(f"Error connecting to FTP host: {e}")
    try:
        shutil.move(local_dir, destination)
        logging.info(f'{file_name} moved to {destination}')
    except Exception as e:
        logging.error(f"Error moving file: {e}")

if __name__=='__main__':
    host = 'ftp.otenet.gr'
    user = 'speedtest'  
    password = 'speedtest'
    remote_dir ='/' 
    local_dir = '/Users/Alexandra/Desktop/Files'
    destination = '\\\\network\\files_for_sharing\\'
    
    schedule.every(20).seconds.do(download_files,
                                 user=user,
                                 password=password,
                                 remote_dir=remote_dir,
                                 local_dir=local_dir,
                                 destination=destination)
    logging.info("Script scheduled to run every 20 sec")
    while True:
         schedule.run_pending()
         time.sleep(1)