import gzip


class GZipDecompressor():
    def decompress(self, gzip_file):
        with gzip.open(gzip_file, 'rb') as f:
            return f.read()
