import os
import unittest

from mock import patch

from podcast_transcriber.utilities import (
    check_env_vars,
    create_temporary_file_name,
    create_temporary_folder
)


class UtilitiesTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch("tempfile.mkdtemp")
    def test_create_temporary_folder_correct(self, mock_mkdtemp):
        mock_mkdtemp.return_value = '/path/to/tmp/dir'
        return_dirpath = "/path/to/tmp/dir"
        self.assertEqual(return_dirpath, create_temporary_folder())

    @patch("tempfile.mkdtemp")
    def test_create_temporary_folder_incorrect(self, mock_mkdtemp):
        mock_mkdtemp.return_value = '/path/to/tmp/wrong_dir'
        return_dirpath = "/path/to/tmp/dir"
        self.assertNotEqual(return_dirpath, create_temporary_folder())

    def test_create_temporary_file_name_correct(self):
        temp_file_result = "/path/to/tmp/file.txt"
        temp_file_dir = "/path/to/tmp"
        temp_file_name = "file.txt"
        self.assertEqual(
            temp_file_result, create_temporary_file_name(
                temp_file_dir, temp_file_name))

    def test_create_temporary_file_name_incorrect(self):
        temp_file_result = "/path/to/tmp/file.txt"
        temp_file_dir = "/path/to/tmp"
        temp_file_name = "wrong_file.txt"
        self.assertNotEqual(
            temp_file_result, create_temporary_file_name(
                temp_file_dir, temp_file_name))

    def test_check_env_vars_true(self):
        os.environ["GOOGLE_API_KEY"] = "test"
        self.assertEqual(True, check_env_vars())

    def test_check_env_vars_false(self):
        if "GOOGLE_API_KEY" in os.environ:
            del os.environ["GOOGLE_API_KEY"]
        self.assertEqual(False, check_env_vars())
