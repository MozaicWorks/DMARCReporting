
from os import listdir
from os.path import isfile
from os.path import join
import io

from DMARCReporting.decompressor import GZipDecompressor
from DMARCReporting.parser import DMARCRuaParser
from DMARCReporting.renderer import ConsoleRenderer
from DMARCReporting.dns import DNS


class CLI():
    def execute(self, input_dir):
        files = [
            f for f in listdir(input_dir) if isfile(join(input_dir, f))
        ]

        decompresser = GZipDecompressor()
        parser = DMARCRuaParser(DNS())
        renderer = ConsoleRenderer()

        for file in files:
            report = decompresser.decompress(join(input_dir, file))
            data = parser.parse(io.BytesIO(report))
            renderer.render(file, data)
