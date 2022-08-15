
from os import listdir
from os.path import isfile
from os.path import join


class FileLister():
    def list(self, input_dir):
        files = sorted([
            f for f in listdir(input_dir) if isfile(join(input_dir, f))
        ])
        return files
