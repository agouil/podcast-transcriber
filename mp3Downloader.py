import urllib2 
import sys 
import subprocess 
import os 

"""http://feeds.gimletmedia.com/~r/hearstartup/~5/sqn8_rZ3xTM/GLT6849433183.mp3"""

""" this function allows a URL to be passed as a parameter from the terminal. 
The URL should contain an mp3 file to be downloaded""" 
def getURLfromUser():
	URL = raw_input("Please enter the URL of the podcast you'd like to transcribe.")
	print "You just entered:", URL 
	return URL

"""Once we have received the mp3 url from the user, we download and write it in a file, in binary. This function writes always in the same file"""
def DownloadMp3FromURL(url):
	mp3file = urllib2.urlopen(url)
	path = '/Users/Mark/Developer/podcast-transcriber/mp3files/test.mp3'
	with open('/Users/Mark/Developer/podcast-transcriber/mp3files/test.mp3','wb') as output:
 		output.write(mp3file.read())
 	return path

"""the file is a file with an extension in a directory, in our case an mp3"""
def convert_to_wav(file):
    '''Converts files to a format that pocketsphinx can deal wtih (16khz mono 16bit wav)'''
    new_file = file[:-4] 
    print new_file
    new_file = new_file + 'hello.wav'
    if os.path.exists(new_file + '.transcription.txt') is False:
        subprocess.call(['ffmpeg', '-y', '-i', file, '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000', new_file])

def main():
	
	Path = DownloadMp3FromURL(getURLfromUser())
	convert_to_wav('/Users/Mark/Developer/podcast-transcriber/mp3files/test.mp3')
	

if __name__ == "__main__":
   main()
