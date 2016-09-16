import urllib2
import subprocess
import os

"""
http://feeds.gimletmedia.com/~r/hearstartup/~5/sqn8_rZ3xTM/GLT6849433183.mp3
"""


def getURLfromUser():
    """
    Function that a URL to be passed as a parameter from the terminal.
    The URL should contain an mp3 file to be downloaded
    """

    url = raw_input(
        "Please enter the URL of the podcast you'd like to transcribe.")
    print "You just entered:", url
    return url


def DownloadMp3FromURL(url):
    """
    Once we have received the mp3 url from the user, we download and write it
    in a file, in binary. This function writes always in the same file
    """

    mp3file = urllib2.urlopen(url)
    path = '/Users/Mark/Developer/podcast-transcriber/mp3files/test.mp3'
    with open('/Users/Mark/Developer/podcast-transcriber/mp3files/test.mp3',
              'wb') as output:
        output.write(mp3file.read())
    return path


def convert_to_wav(file):
    """
    Converts files to a format that pocketsphinx can deal with
    (16khz mono 16bit wav)
    """

    new_file = file[:-4]
    print new_file
    new_file = new_file + 'hello.wav'
    if os.path.exists(new_file + '.transcription.txt') is False:
        subprocess.call(['ffmpeg', '-y', '-i', file, '-acodec', 'pcm_s16le',
                         '-ac', '1', '-ar', '16000', new_file])


def main():
    path = DownloadMp3FromURL(getURLfromUser())
    convert_to_wav(
        '/Users/Mark/Developer/podcast-transcriber/mp3files/test.mp3')


if __name__ == "__main__":
    main()
