# podcast-transcriber
A simple audio file transcriber that uses the [Google Cloud Speech API](https://cloud.google.com/speech/) for transcription.
## Installation
Install this package with `pip`:
```
pip install git+https://github.com/agouil/podcast-transcriber.git
```

### Dependencies
Install [SoX - Sound eXchange](http://sox.sourceforge.net/). If you're using Mac you can install through [Homebrew](http://brew.sh/):
```
brew install sox
```
If you're using Windows or Linux, download the binaries and installer from [here](https://sourceforge.net/projects/sox/files/sox/).

### Requirements
You will need to have a Google API Key in order transcript audio. If you don't have one, then you need to sign up for the [Google Cloud Speech API](https://cloud.google.com/speech/). 

## How to use it
Set the Google API Key as an enviroment variable. You can simply run,

For UNIX:
```
export GOOGLE_API_KEY=<your-api-key>
```
For WINDOWS:
```
SET GOOGLE_API_KEY=<your-api-key>
```

Copy the example script below to a file named `example.py`.
```python
import argparse
import podcast_transcriber

# parse the CLI arguments
parser = argparse.ArgumentParser(prog="python podcast_transcriber.py")
parser.add_argument("input_file", help="input audio file")
args = parser.parse_args()

podcast_transcriber.transcribe(args.input_file)
```

Run the script with:
```
python example.py input_file
```
The argument `input_file` is the input audio file URL. E.g. For a podcast, you can provide the MP3 file found in a podcast's RSS Feed.

Then the script downloads the file and converts it to smaller files of 40 seconds length each of raw audio bytes through SoX. This is the format the Google Speech API requires - 16-bit 16KHz Linear PCM.

For each file, the script gets the transcript from the Google Speech API. In the end, it concatenates the transcript chunks to a final output file inside the `output` directory.

### Example Audio File
For testing the script you can use this small audio file - https://archive.org/download/testmp3testfile/mpthreetest.mp3

## Contributing
Fork the repository, make necessary changes, run tests and submit a pull request.

### Testing
Before running tests, install the necessary requirements with:
```
pip install -r requirements_tests.txt
```

Run tests with `nosetests` command.


## Issues
To submit any issues, raise an issue through the [Issues Page](https://github.com/agouil/podcast-transcriber/issues)

## License
[MIT](LICENSE)
