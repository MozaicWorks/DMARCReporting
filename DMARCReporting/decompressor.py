import gzip
import zipfile
import zlib


class DecompressorFactory():
    def create(file_path):
        if file_path.endswith(".gz"):
            return GZipDecompressor()
        if file_path.endswith(".zip"):
            return ZipDecompressor()
        raise NotImplementedError(file_path)


class GZipDecompressor():
    def decompress(self, gzip_file_path):
        try:
            with gzip.open(gzip_file_path, 'rb') as f:
                return f.read()
        except gzip.BadGzipFile:
            return self._decompress_with_zlib(gzip_file_path)

    def _decompress_with_zlib(self, gzip_file_path):
        with open(gzip_file_path, 'rb') as f:
            do = zlib.decompressobj(wbits=31)
            data = do.decompress(f.read())
            remainder = do.unused_data
            f.seek(f.tell() - len(remainder))
            return data


class ZipDecompressor():
    def decompress(self, zip_file_path):
        with zipfile.ZipFile(zip_file_path, 'r') as zf:
            files = zf.infolist()
            with zf.open(files[0].filename) as f:
                return f.read()
