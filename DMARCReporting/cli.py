
from os import listdir
from os.path import isfile
from os.path import join
import io

from DMARCReporting.decompressor import DecompressorFactory
from DMARCReporting.parser import DMARCRuaParser
from DMARCReporting.renderer import ConsoleRenderer
from DMARCReporting.dns import DNS


class CLI():
    def execute(self, input_dir):
        files = sorted([
            f for f in listdir(input_dir) if isfile(join(input_dir, f))
        ])

        parser = DMARCRuaParser(DNS())
        renderer = ConsoleRenderer()

        for file in files:
            file_path = join(input_dir, file)
            report = DecompressorFactory.create(file_path).decompress(file_path)
            data = parser.parse(io.BytesIO(report))
            renderer.render(file, data)
