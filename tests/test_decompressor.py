from .context import DMARCReporting  # noqa F401
from DMARCReporting.decompressor import DecompressorFactory
from DMARCReporting.decompressor import GZipDecompressor


def test_factory_return_gzip_decompressor():
    sut = DecompressorFactory
    actual = sut.create("./tests/data/sample.txt.gz")

    assert "GZipDecompressor" == type(actual).__name__


def test_decompress_gzip():
    sut = GZipDecompressor()
    actual = sut.decompress("./tests/data/sample.txt.gz")

    assert "Hello world!" == actual.decode("utf-8")
