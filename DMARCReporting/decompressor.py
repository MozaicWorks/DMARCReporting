import gzip


class DecompressorFactory():
    def create(file_path):
        if file_path.endswith(".gz"):
            return GZipDecompressor()


class GZipDecompressor():
    def decompress(self, gzip_file_path):
        with gzip.open(gzip_file_path, 'rb') as f:
            return f.read()
