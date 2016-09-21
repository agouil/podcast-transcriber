import os
import subprocess

import utilities

from transcriber import Transcriber


"""
http://feeds.gimletmedia.com/~r/hearstartup/~5/sqn8_rZ3xTM/GLT6849433183.mp3
"""


def get_url_from_user():
    """
    Function that a URL to be passed as a parameter from the terminal.
    The URL should contain an mp3 file to be downloaded
    """

    url = raw_input(
        "Please enter the URL of the podcast you'd like to transcribe. ")
    print "You just entered: ", url
    return url


def get_podcast_file(url):
    """
    Returns the podcast file to process in the right format. First, we download
    the podcast from the remote location and then we convert the file to the
    right format for the transcriber.

    Params:
        url (string): The url of the remote file
    """

    # create the download destination
    dirpath = utilities.create_temporary_folder()
    mp3_uid = url.split('/')[-1:]
    filepath = utilities.create_temporary_file_name(dirpath, mp3_uid[0])

    # get the podcast file
    utilities.download_remote_file(url, filepath)

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
    file_dir = os.path.split(filepath)[0]

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
    # Setting up environment
    if not utilities.check_env_vars():
        return
    utilities.create_ancillary_folders()

    # download the podcast file
    filepath = get_podcast_file(get_url_from_user())

    # convert file to raw audio chunks
    chunks = convert_to_raw_audio_chunks(filepath)

    # transcribe chunks
    transcriber = Transcriber(os.environ['GOOGLE_API_KEY'])
    transcript = transcriber.transcribe_many(chunks)

    # write to the output file
    output_file_name = os.path.split(filepath)[-1]
    utilities.write_output_file(output_file_name, transcript)

    print "Cleaning up...\n"
    utilities.cleanup()


if __name__ == "__main__":
    main()
