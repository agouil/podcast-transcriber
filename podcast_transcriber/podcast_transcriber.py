import os
import subprocess

import utilities

from transcriber import Transcriber


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


def transcribe(input_file_url):
    """
    Transcribes an audio file. The audio file format is a URL.

    Params:
        input_file_url (string): The input audio file URL
    """

    # Setting up environment
    if not utilities.check_env_vars():
        return
    utilities.create_ancillary_folders()

    # download the podcast file
    filepath = get_podcast_file(input_file_url)

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
