
from os.path import join
import io

from DMARCReporting.decompressor import DecompressorFactory
from DMARCReporting.parser import DMARCRuaParser
from DMARCReporting.renderer import ConsoleRenderer
from DMARCReporting.dns import DNS
from DMARCReporting.FileLister import FileLister


class CLI():
    def execute(self, input_dir):
        files = FileLister().list(input_dir)

        parser = DMARCRuaParser(DNS())
        renderer = ConsoleRenderer()

        for file in files:
            file_path = join(input_dir, file)
            report = DecompressorFactory.create(file_path).decompress(file_path)
            data = parser.parse(io.BytesIO(report))
            renderer.render(file, data)
