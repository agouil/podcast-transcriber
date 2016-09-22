import unittest

from podcast_transcriber.transcriber import Transcriber


class TranscriberTest(unittest.TestCase):

    def setUp(self):
        self.transc = Transcriber("")

    def tearDown(self):
        self.transc = None

    def test_transcript_str_wrong_input(self):
        with self.assertRaises(AttributeError):
            self.transc.get_transcript_str(int(1))

    def test_transcript_str_empty_chunks(self):
        self.transc.transcript_chunks = []
        self.assertEqual("", self.transc.get_transcript_str())

    def test_transcript_str_correct_no_arg(self):
        self.transc.transcript_chunks = [
            "correctly", "join", "chunks", "together"]
        self.assertEqual(
            "correctly\njoin\nchunks\ntogether",
            self.transc.get_transcript_str())

    def test_transcript_str_correct_other_arg(self):
        self.transc.transcript_chunks = [
            "correctly", "join", "chunks", "together"]
        self.assertEqual(
            "correctly join chunks together",
            self.transc.get_transcript_str(" "))
