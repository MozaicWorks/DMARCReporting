
from os import listdir
from os.path import isfile
from os.path import join
import pathlib


class FileLister():
    def list(self, input_dir):
        return sorted([
            f for f in listdir(input_dir) if self._is_zip_or_gz_file(input_dir, f)
        ])

    def _is_zip_or_gz_file(self, input_dir, file_name):
        return isfile(join(input_dir, file_name)) and pathlib.Path(file_name).suffix in [".zip", ".gz"]
