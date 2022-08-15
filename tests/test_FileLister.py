
import unittest
from .context import DMARCReporting  # noqa F401
from DMARCReporting.FileLister import FileLister
import tempfile
import os
from parameterized import parameterized


class TestFileLister(unittest.TestCase):
    @parameterized.expand([
           ("single_zip_file", ["1.zip"], ["1.zip"]),
           ("two_zip_files", ["1.zip", "2.zip"], ["1.zip", "2.zip"]),
           ("single_gzip_file", ["1.gz"], ["1.gz"]),
           ("two_gzip_files", ["1.gz", "2.gz"], ["1.gz", "2.gz"]),
           ("two_tar_gz_files", ["1.tar.gz", "2.tar.gz"], ["1.tar.gz", "2.tar.gz"]),
           ("sort_files", ["2.gz", "z.zip", "1.gz", "a.zip"], ["1.gz", "2.gz", "a.zip", "z.zip"]),
           ("only_gz_and_zip_files", ["z.zip", "1.gz", "3.txt", "ttt.jpg"], ["1.gz", "z.zip"]),
       ])
    def test_file_lister(self, name, filesList, expected):
        def listerFunction(dirName): return FileLister().list(dirName)

        actual = self.list_files_with_function(filesList, listerFunction)

        self.assertListEqual(expected, actual)

    def create_test_file(self, path, filename):
        with open(os.path.join(path, filename), 'w'):
            pass

    def list_files_with_function(self, filesList, listerFunction):
        ''' Create temporary directory, temporary files, list them with the lister function, and delete them'''
        with tempfile.TemporaryDirectory() as testDir:
            [self.create_test_file(testDir, fileName) for fileName in filesList]
            return listerFunction(testDir)
