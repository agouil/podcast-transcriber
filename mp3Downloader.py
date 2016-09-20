import urllib2
import subprocess
import os
import tempfile 
import shutil

"""
http://feeds.gimletmedia.com/~r/hearstartup/~5/sqn8_rZ3xTM/GLT6849433183.mp3
"""

path = '/Users/Mark/Developer/podcast-transcriber/tmp'


def cleanup(path):
    shutil.rmtree(path)


def create_ancillary_folders():
    if not os.path.exists('/Users/Mark/Developer/podcast-transcriber/output'):
        print "Output file absent. Creating output file"
        os.makedirs('/Users/Mark/Developer/podcast-transcriber/output')
    if not os.path.exists('/Users/Mark/Developer/podcast-transcriber/' + 'tmp/'):
        print "Creating tmp file for mp3 files"
        os.makedirs('/Users/Mark/Developer/podcast-transcriber/tmp/')




def get_url_from_user():
    """
    Function that a URL to be passed as a parameter from the terminal.
    The URL should contain an mp3 file to be downloaded
    """

    url = raw_input(
        "Please enter the URL of the podcast you'd like to transcribe. ")
    print "You just entered: ", url
    return url


# this function is to be called with the global path variable

def create_temporary_folder(directory):
    dirpath = tempfile.mkdtemp(dir=directory)
    print "Just created tmp dir at ", dirpath 
    return dirpath


def create_temporary_file(directory, suffix):
    fp = tempfile.NamedTemporaryFile(dir=directory, suffix=suffix)
    print "Just created tmp file at ", fp.name 
    return fp


def download_mp3_from_url(url):
    """
    Once we have received the mp3 url from the user, we download and write it
    in a file, in binary. This function writes always in the same file
    """
    dirpath = create_temporary_folder(path)

    mp3file = urllib2.urlopen(url)
    mp3_uid = url.split('/')[-1:]
    print mp3_uid
    filepath = create_temporary_file(dirpath, mp3_uid[0])
    print filepath.name, "this is the filepath"
    with open(filepath.name, 'wb') as output:
        output.write(mp3file.read())
        if not os.path.exists(filepath.name):
            print "Failed to write mp3 in ", filepath
        convert_to_wav(filepath.name)

    return filepath.name


def convert_to_wav(filepath):
    """
    Converts files to a format that pocketsphinx can deal with
    (16khz mono 16bit wav)
    """

    print filepath

    new_file = filepath[:-4]
    print new_file, "this the new filename without the .mp3 extension"
    new_file = new_file + '.wav'
    if os.path.exists(new_file + '.transcription.txt') is False:
        subprocess.call(['ffmpeg', '-y', '-i', filepath, '-acodec', 'pcm_s16le',
                         '-ac', '1', '-ar', '16000', new_file])


def main():
    create_ancillary_folders()
    newPath = download_mp3_from_url(get_url_from_user())
    #assuming here a function that does transcribe & write to output
    print "I have transcribed the podcast here. "
    print ""
    print "Proceeding to cleanup"
    print ""
    cleanup(path)
    #here I need to go and delete the temp files. 


if __name__ == "__main__":
    main()
