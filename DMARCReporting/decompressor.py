import gzip
import zipfile


class DecompressorFactory():
    def create(file_path):
        if file_path.endswith(".gz"):
            return GZipDecompressor()
        if file_path.endswith(".zip"):
            return ZipDecompressor()
        raise NotImplementedError(file_path)


class GZipDecompressor():
    def decompress(self, gzip_file_path):
        with gzip.open(gzip_file_path, 'rb') as f:
            return f.read()


class ZipDecompressor():
    def decompress(self, zip_file_path):
        with zipfile.ZipFile(zip_file_path, 'r') as zf:
            files = zf.infolist()
            with zf.open(files[0].filename) as f:
                return f.read()
