import os
import tempfile
import subprocess
import shutil
import urllib2

from transcriber import Transcriber


"""
http://feeds.gimletmedia.com/~r/hearstartup/~5/sqn8_rZ3xTM/GLT6849433183.mp3
"""

TEMP_DIR = './tmp'
OUTPUT_DIR = './output'


def check_env_vars():
    """
    Checks if all necessary ENV variables are set. If not, prints
    an error message.
    """

    if 'GOOGLE_API_KEY' not in os.environ:
        print "Google API key is missing.\n" \
            + "To add run `export GOOGLE_API_KEY=<your-api-key>"
        return False
    return True


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
    print "Created tmp dir at ", dirpath
    return dirpath


def create_temporary_file_name(directory, suffix):
    #
    # TODO: use OS-specific path separator
    #
    return directory + '/' + suffix


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

    print "Downloading: %s" % url.split('/')[-1]

    file_size_dl = 0
    block_sz = 8192

    with open(dest, 'wb') as local_file:
        while True:
            buf = remote_file.read(block_sz)
            if not buf:
                break

            file_size_dl += len(buf)
            local_file.write(buf)

            status = r"Progress: %10d / %10d    [%3.2f%%]" % (
                file_size_dl, file_size, file_size_dl * 100. / file_size)
            status = status + chr(8) * (len(status) + 1)
            print status,
    print "\nFile downloaded to: %s" % dest


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
    mp3_uid = url.split('/')[-1:]
    filepath = create_temporary_file_name(dirpath, mp3_uid[0])

    # get the podcast file
    download_remote_file(url, filepath)

    return filepath


def convert_to_raw_audio_chunks(filepath):
    """
    Converts an mp3 file to raw binary audio files (16khz mono 16bit) of
    40 seconds.

    Params:
        filepath (string): The path of the input file
    """

    print "Converting to raw audio format..."

    file_prefix = filepath[:-4]
    file_dir = '/'.join(filepath.split('/')[:-1])

    # convert to raw format
    subprocess.call(['sox', filepath, '--rate', '16k', '--bits', '16',
                     '--endian', 'little', '--encoding', 'signed-integer',
                     '--channels', '1', file_prefix + '.raw',
                     'trim', '0', '40', ':', 'newfile', ':', 'restart'])

    # grab the new filepaths
    chunks = [os.path.join(file_dir, f)
              for f in os.listdir(file_dir) if '.raw' in f]

    return chunks


def main():
    create_ancillary_folders()
    filepath = get_podcast_file(get_url_from_user())

    # convert file to raw audio chunks
    chunks = convert_to_raw_audio_chunks(filepath)

    # transcribe chunks
    transcriber = Transcriber()
    transcript = transcriber.transcribe_many(chunks)

    with open(OUTPUT_DIR + 'transcript.txt', 'w') as output_file:
        output_file.write(transcript)

    print "Cleaning up...\n"
    cleanup()


if __name__ == "__main__":
    main()
