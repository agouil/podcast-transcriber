import urllib2
import subprocess
import os
import tempfile
import shutil

"""
http://feeds.gimletmedia.com/~r/hearstartup/~5/sqn8_rZ3xTM/GLT6849433183.mp3
"""

TEMP_DIR = './tmp'
OUTPUT_DIR = './output'


def cleanup():
    shutil.rmtree(TEMP_DIR)


def create_ancillary_folders():
    if not os.path.exists(OUTPUT_DIR):
        print "Output directory absent. Creating output directory..."
        os.makedirs(OUTPUT_DIR)
    if not os.path.exists(TEMP_DIR):
        print "Creating tmp directory..."
        os.makedirs(TEMP_DIR)


def get_url_from_user():
    """
    Function that a URL to be passed as a parameter from the terminal.
    The URL should contain an mp3 file to be downloaded
    """

    url = raw_input(
        "Please enter the URL of the podcast you'd like to transcribe. ")
    print "You just entered: ", url
    return url


def create_temporary_folder():
    dirpath = tempfile.mkdtemp(dir=TEMP_DIR)
    print "Just created tmp dir at ", dirpath
    return dirpath


def create_temporary_file(directory, suffix):
    fp = tempfile.NamedTemporaryFile(dir=directory, suffix=suffix)
    print "Just created tmp file at ", fp.name
    return fp


def download_remote_file(url, dest):
    """
    Downloads a remote file to the specified location.

    Params:
        url  (string): The url of the remote file
        dest (string): The download destination
    """

    remote_file = urllib2.urlopen(url)
    meta_info = remote_file.info()
    file_size = int(meta_info.getheaders("Content-Length")[0])

    print "Downloading: %s \n Bytes: %s" % (url.split('/')[-1], file_size)

    file_size_dl = 0
    block_sz = 8192

    with open(dest, 'wb') as local_file:
        while True:
            buf = remote_file.read(block_sz)
            if not buf:
                break

            file_size_dl += len(buf)
            local_file.write(buf)

            status = r"%10d  [%3.2f%%]" % (
                file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8) * (len(status) + 1)
            print status,


def get_podcast_file(url):
    """
    Returns the podcast file to process in the right format. First, we download
    the podcast from the remote location and then we convert the file to the
    right format for the transcriber.

    Params:
        url (string): The url of the remote file
    """

    # create the download destination
    dirpath = create_temporary_folder()

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
        subprocess.call(['ffmpeg', '-y', '-i', filepath, '-acodec',
                         'pcm_s16le', '-ac', '1', '-ar', '16000', new_file])


def main():
    create_ancillary_folders()
    new_path = download_mp3_from_url(get_url_from_user())
    # assuming here a function that does transcribe & write to output
    print "I have transcribed the podcast here. "
    print ""
    print "Proceeding to cleanup"
    print ""
    cleanup()
    # here I need to go and delete the temp files.


if __name__ == "__main__":
    main()
