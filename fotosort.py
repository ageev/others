import os, time, sys
from datetime import datetime
from shutil import copy2

SRC_FOLDER = 'd:\\_разобрать\\'
DST_FOLDER = 'd:\\готово\\'

def main():
    for dirpath, dirnames, filenames in os.walk(SRC_FOLDER):
        for f in filenames:
            filename, file_extension = os.path.splitext(f)
            if file_extension.lower() == '.avi' or \
               file_extension.lower() == '.mpeg' or \
               file_extension.lower() == '.mpg' or \
               file_extension.lower() == '.mov' or \
               file_extension.lower() == '.vob' or \
               file_extension.lower() == '.jpeg' or \
               file_extension.lower() == '.jpg' or \
               file_extension.lower() == '.raw' or \
               file_extension.lower() == '.mp4' or \
               file_extension.lower() == '.cr2' or \
               file_extension.lower() == '.nef':

                file_modified_time = datetime.fromtimestamp(os.path.getmtime(os.path.join(SRC_FOLDER, dirpath, f)))
                new_path = datetime.strftime(file_modified_time, '%Y/%m - %B/') + file_extension.lower() + "/"
                day = datetime.strftime(file_modified_time, '%d')

                old_file = os.path.join(SRC_FOLDER, dirpath, f)
                new_file = os.path.join(DST_FOLDER, new_path, day + '_' + f)

                if not os.path.exists(os.path.join(DST_FOLDER, new_path)): #create new folder if not exists
                    os.makedirs(os.path.join(DST_FOLDER, new_path))

                if os.path.isfile(new_file):  #if file already exists
                    if os.path.getsize(old_file) != os.path.getsize(new_file): #if size different
                        new_file = os.path.join(DST_FOLDER, new_path, day + '_'+ str(os.path.getsize(old_file)) + "_" + f)
                
                os.replace(old_file, new_file)
                
#                copy2(old_file, new_file) # dry run

if __name__ == "__main__":
    main()   