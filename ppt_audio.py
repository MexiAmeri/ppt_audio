#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, glob, pathlib, shutil, sys
from zipfile import ZipFile

def unzip(zip, path, audio_path): # Unzip to temp folder

    # Create a ZipFile Object and load the original zip into it
    with ZipFile(zip, 'r') as zipObj:

    # Get a list of all archived file names from the zip
        listOfFileNames = zipObj.namelist()

        # Iterate over the file names
        for fileName in listOfFileNames:

            # Check filename endswith jpeg
            if fileName.endswith('.m4a'):

                # Extract a single file from zip to the directory created from the original zip filename
                with open(audio_path + os.path.basename(fileName), 'wb') as f:
                    f.write(zipObj.read(fileName))

def stripLabel(audio_path): # Changes file names to int to strip 0's and for better ordering

    # Find all jpeg files
    files = glob.glob(audio_path + '*.m4a')

    # Loop through list of files to rename
    for file in files:
        prepToConvert = os.path.basename(file).replace('.m4a','')
        converted = prepToConvert.replace('media','').zfill(10)
        renamed = str(converted) + '.m4a'
        os.rename(file,audio_path + renamed)

if __name__ == '__main__':

    ppt = sys.argv[1]

    if '.ppt' not in pathlib.Path(ppt).suffix:
        sys.exit("Not a recognized PPT/PPTX format.")

    file = os.path.basename(ppt)
    path = os.path.dirname(os.path.abspath(ppt)) + '/'

    file_no_ext = pathlib.Path(file).stem

    shutil.copyfile(path + file, path + 'temp.zip') # Copy file to a temp zip

    os.mkdir(path + 'audio')
    audio_path = path + 'audio/'

    unzip(f'{path}temp.zip', path, audio_path)
    stripLabel(audio_path)

    os.system(f'''printf "file '%s'\n" {audio_path}*.m4a > {path}mylist.txt''')
    os.system(f'ffmpeg -f concat -safe 0 -i {path}mylist.txt -c copy "{path}{file_no_ext}.mp4"')
    os.remove(f'{path}temp.zip')
    os.remove(f'{path}mylist.txt')
    shutil.rmtree(audio_path)
