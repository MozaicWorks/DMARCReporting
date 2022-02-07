from .context import DMARCReporting  # noqa F401
from DMARCReporting.decompressor import GZipDecompressor


def test_decompress_gzip():
    sut = GZipDecompressor()
    actual = sut.decompress("./tests/data/sample.txt.gz")

    assert "Hello world!" == actual.decode("utf-8")
