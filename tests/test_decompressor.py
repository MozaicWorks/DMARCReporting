import pytest

from .context import DMARCReporting  # noqa F401
from DMARCReporting.decompressor import DecompressorFactory
from DMARCReporting.decompressor import GZipDecompressor
from DMARCReporting.decompressor import ZipDecompressor


def test_factory_return_gzip_decompressor():
    sut = DecompressorFactory
    actual = sut.create("./tests/data/sample.txt.gz")

    assert "GZipDecompressor" == type(actual).__name__


def test_factory_return_zip_decompressor():
    sut = DecompressorFactory
    actual = sut.create("./tests/data/sample.txt.zip")

    assert "ZipDecompressor" == type(actual).__name__


def test_factory_raises_not_implemented():
    sut = DecompressorFactory

    with pytest.raises(NotImplementedError):
        sut.create("./tests/data/sample.txt")


def test_decompress_gzip():
    sut = GZipDecompressor()
    actual = sut.decompress("./tests/data/sample.txt.gz")

    assert "Hello world, gzip!" == actual.decode("utf-8")


def test_decompress_zip():
    sut = ZipDecompressor()
    actual = sut.decompress("./tests/data/sample.txt.zip")

    assert "Hello world, zip!" == actual.decode("utf-8")
