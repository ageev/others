import os, time, sys
from datetime import datetime
from shutil import copy2

SRC_FOLDER = 'd:\\_разобрать\\'
DST_FOLDER = 'd:\\готово\\'
EXTENTIONS = ['.avi', '.mpeg', '.mpg', '.mov', '.vob', '.mp4', '.jpeg', '.jpg', '.cr2', '.nef', '.raw', '.dng']

def main():
    for dirpath, dirnames, filenames in os.walk(SRC_FOLDER):
        for f in filenames:
            filename, file_extension = os.path.splitext(f)
            if file_extension.lower() in EXTENTIONS:
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
# Synology Photos stopped indexing dirs with dot (e.g. ".jpg"), so I used this function to rename ".jpg" -> "jpg"
def rename_dir_no_dot():
    for dirpath, dirnames, filenames in os.walk(SRC_FOLDER):
        for d in dirnames:
        	if d in EXTENTIONS:
        		os.rename(os.path.join(SRC_FOLDER,dirpath,d), os.path.join(SRC_FOLDER,dirpath,d[1:]))
        		print("[+] folder ", os.path.join(dirpath,d), " was renamed")


if __name__ == "__main__":
    main()   
