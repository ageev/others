#! /usr/bin/env python3

import sys
import os
import hashlib
import logging

# source: https://stackoverflow.com/questions/748675/finding-duplicate-files-and-removing-them

DEFAULT_PATH = '/volume1/photo'
REMOVE_DUPS = True #if true newer file will be deleted
EXCEPTION_DIRS = ['@eaDir', '#recycle']

logFile = os.path.splitext(os.path.realpath(__file__))[0] + '.log'
logging.basicConfig(
    format='%(asctime)s %(levelname)-5s %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S', 
    level=logging.INFO,
    handlers=[
        logging.FileHandler(logFile),
        logging.StreamHandler()
        ]
    )
logger = logging.getLogger(__name__)

def main(path, hash=hashlib.sha1):

    if not path:
        path = DEFAULT_PATH
    hashes_by_size = {}
    hashes_on_1k = {}
    hashes_full = {}
    duplicates = []

    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if check_exception_dir(EXCEPTION_DIRS, dirpath):
                continue
            full_path = os.path.join(dirpath, filename)
            try:
                # if the target is a symlink (soft one), this will 
                # dereference it - change the value to the actual target file
                full_path = os.path.realpath(full_path)
                file_size = os.path.getsize(full_path)
            except (OSError,):
                # not accessible (permissions, etc) - pass on
                continue

            duplicate = hashes_by_size.get(file_size)

            if duplicate:
                hashes_by_size[file_size].append(full_path)
            else:
                hashes_by_size[file_size] = []  # create the list for this file size
                hashes_by_size[file_size].append(full_path)

    # For all files with the same file size, get their hash on the 1st 1024 bytes
    for __, files in hashes_by_size.items():
        if len(files) < 2:
            continue    # this file size is unique, no need to spend cpy cycles on it

        for filename in files:
            try:
                small_hash = get_hash(filename, first_chunk_only=True)
            except (OSError,):
                # the file access might've changed till the exec point got here 
                continue

            duplicate = hashes_on_1k.get(small_hash)
            if duplicate:
                hashes_on_1k[small_hash].append(filename)
            else:
                hashes_on_1k[small_hash] = []          # create the list for this 1k hash
                hashes_on_1k[small_hash].append(filename)

    # For all files with the hash on the 1st 1024 bytes, get their hash on the full file - collisions will be duplicates
    for __, files in hashes_on_1k.items():
        if len(files) < 2:
            continue    # this hash of fist 1k file bytes is unique, no need to spend cpy cycles on it

        for filename in files:
            try: 
                full_hash = get_hash(filename, first_chunk_only=False)
            except (OSError,):
                # the file access might've changed till the exec point got here 
                continue

            duplicate = hashes_full.get(full_hash)
            if duplicate:
                duplicates.append([filename, duplicate])
            else:
                hashes_full[full_hash] = filename

    if REMOVE_DUPS:
        remove_duplicates(duplicates)
    else:
        print(duplicates)
    return

def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk

def check_exception_dir(e_dirs, dirpath):
    for e_dir in e_dirs:
        if e_dir in dirpath:
            return True
    return False

def get_hash(filename, first_chunk_only=False, hash=hashlib.sha1):
    hashobj = hash()
    file_object = open(filename, 'rb')

    if first_chunk_only:
        hashobj.update(file_object.read(1024))
    else:
        for chunk in chunk_reader(file_object):
            hashobj.update(chunk)
    hashed = hashobj.digest()

    file_object.close()
    return hashed

def remove_duplicates(dups):
    for dup in dups:
        mtime0 = os.path.getmtime(dup[0])
        try:
            mtime1 = os.path.getmtime(dup[1])
        except:
            logger.error('FileNotFound. Run dups again.')
            continue
        if mtime0 < mtime1:
            logger.info('Keep: {0}, Remove: {1}'.format(dup[0], dup[1]))
            try:
                os.remove(dup[1])
            except:
                logger.error('Access denied to ' + dup[1])
        else:
            logger.info('Keep: {1}, Remove: {0}'.format(dup[0], dup[1]))
            try:
                os.remove(dup[0])
            except:
                logger.error('Access denied to ' + dup[1])

if __name__ == "__main__":
    main(sys.argv[1:])