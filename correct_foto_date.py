import os, time, sys
from datetime import datetime

#SRC_FOLDER = 'C:\\TEMP\\fotosort\\dst\\'
SRC_FOLDER = 'd:\\готово\\'

# ++++++ logger routine +++++++
import logging
logPath = 'C:/Temp/'
logFile = 'file_date_corrector'

logging.basicConfig(
    format='%(asctime)s %(levelname)-5s %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S', 
    level=logging.INFO,
    handlers=[
        logging.FileHandler("{0}/{1}.log".format(logPath, logFile)),
        logging.StreamHandler()
        ]
    )
logger = logging.getLogger(__name__)
# +++++++++++++++++++++++++++++

def main():
    for dirpath, dirnames, filenames in os.walk(SRC_FOLDER):
        for f in filenames:
            do_the_magic(dirpath + "\\" + f)

def do_the_magic(file):
    path_list = file.split('\\')
    try:
        path_time = path_list[-3] + ' ' + path_list[-4]
        file_path_time = datetime.strptime(path_time, '%m - %B %Y')
        mtime = datetime.fromtimestamp(os.path.getmtime(file))
        atime = os.path.getatime(file)

        if (file_path_time.year != mtime.year) and (file_path_time.month != mtime.month):
            logger.info('Changing date from {0}/{1} to {2}/{3} for file {4}'.format(mtime.year, 
                                                                            mtime.month, file_path_time.year, 
                                                                            file_path_time.month, file))
            os.utime(file, (atime, file_path_time.timestamp()))
    except Exception as err:
        logger.error('Error working with file ' + file + ' Error: ' + str(err))

if __name__ == "__main__":
    main()