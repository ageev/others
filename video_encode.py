import os, time, sys
from datetime import datetime
from shutil import copy2
import subprocess
import logging

SRC_FOLDER = 'd:/готово/_private/Видео/'
PATH_TO_FFMPEG = 'c:/Users/S/Downloads/ffmpeg-4.1-win64-static/bin/'
VIDEO_EXT = ['.avi', '.mpeg', '.mpg', '.mov', '.vob', '.mp4']
#ALLOWED_CODECS = ['h264', 'hevc']
ALLOWED_CODECS = ['hevc']
LOG_PATH = 'c:/Temp/video_converter.log'

# ffmpeg settings
audio_codec_settings = 'aac -vbr 4 '
video_codec_settings = 'libx265 -pix_fmt yuv420p -x265-params crf=23 -preset:v slow' # crf=28 is default value. crf=23 is better, but size x 2

logging.basicConfig(
    filename = LOG_PATH,
    format='%(asctime)s %(levelname)-5s %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S', 
    level=logging.DEBUG
    )
logger = logging.getLogger(__name__)

def main():
    for dirpath, dirnames, filenames in os.walk(SRC_FOLDER):
        for f in filenames:
            filename, file_extension = os.path.splitext(f)
            if file_extension.lower() in VIDEO_EXT:
                path_to_file = os.path.join(SRC_FOLDER, dirpath, f)
                print(path_to_file)
                #check codec. If not h264/265 - proceed
                if not check_codec(path_to_file):
                    try:
                        new_file = convert(path_to_file)
                        print(new_file)
                        if os.path.getsize(new_file) > os.path.getsize(path_to_file):
                            logger.warning('New file is bigger then original ' + path_to_file + '. Keeping both')
                        else:
                            logger.info('Old size;' + str(os.path.getsize(path_to_file)) + '; New size;' + str(os.path.getsize(new_file)))
                            os.remove(path_to_file)  # !!!! remove original file !!!!
                            logger.info('File ' + path_to_file + ' removed')
                    except:
                        logger.error('Error encoding ' + path_to_file + '. Skipping...')

def check_codec(file):
    output = subprocess.run(PATH_TO_FFMPEG + 'ffprobe.exe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "' + file + '"', capture_output=True)
    print(str(output.stdout))
    if any(x in str(output.stdout) for x in ALLOWED_CODECS):
#        logger.info('File ' + file + ' is already encoded with h.264/265')
        return True
    else: 
        return False

def convert(file):
    logger.info('Converting file ' + file)
    filename, file_extension = os.path.splitext(file)
    new_file = filename + '.mp4'
    if os.path.isfile(new_file): #if mp4 file exists in current dir
        filename, file_extension = os.path.splitext(new_file)
        new_file = filename + '_hevc.mp4' # rename to name+ _hevc.mp4

    output = subprocess.run(PATH_TO_FFMPEG + 'ffmpeg.exe -i "' + file + '"' 
        + ' -c:v ' + video_codec_settings 
        + ' -c:a ' + audio_codec_settings 
        + '"' + new_file + '"'
        + " -hide_banner -loglevel error -n")
    print(output.stdout)

    #preserve metadata
    mtime = os.path.getmtime(file)
    atime = os.path.getatime(file)
    os.utime(new_file, (atime, mtime))

    logger.info('File ' + new_file + ' converted')
    return new_file

if __name__ == "__main__":
    main()   