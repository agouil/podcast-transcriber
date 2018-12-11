import base64

from googleapiclient import discovery


class Transcriber(object):

    # the transcript chunks
    transcript_chunks = []

    def __init__(self, api_key):
        self.api_key = api_key

    def get_speech_service(self):
        """
        Get the Google Speech service.
        """

        return discovery.build('speech', 'v1', developerKey=self.api_key)

    def transcribe(self, filepath):
        """
        Transcribe the given audio file.

        Params:
            filepath (string): The name of the audio file.
        """

        with open(filepath, 'rb') as speech:
            # Base64 encode the binary audio file for inclusion in the JSON
            # request.
            speech_content = base64.b64encode(speech.read())

        service = self.get_speech_service()
        service_request = service.speech().recognize(
            body={
                'config': {
                    'encoding': 'LINEAR16',  # raw 16-bit signed LE samples
                    'sampleRateHertz': 16000,  # 16 khz
                    'languageCode': 'en-US',  # a BCP-47 language tag
                    'enableAutomaticPunctuation': 'true',
                },
                'audio': {
                    'content': speech_content.decode('UTF-8')
                }
            })
        response = service_request.execute()
        return response

    def transcribe_many(self, filepaths):
        """
        Transcribe the given list of audio files.

        Params:
            filepaths (list[string]): The list of audio files.
        """

        items = len(filepaths)

        # loop through the files and transcribe them
        for i, f in enumerate(filepaths, start=1):
            print "Transcribing [ %d / %d ] %s ..." % (i, items, f)
            response = self.transcribe(f)

            # read the response and extract the transcript
            for alternatives in response['results']:
                self.transcript_chunks.append(
                    alternatives['alternatives'][0]['transcript'])

        return self.get_transcript_str()

    def get_transcript_str(self, glue=""):
        """
        Returns a string representation of the transcript chunks.

        Params:
            glue (string): The glue to join the chunks. Default value is the
                           newline character (\n)
        """
        if not glue:
            glue = "\n"
        return glue.join(self.transcript_chunks)
