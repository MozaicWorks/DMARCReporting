
from os.path import join
import io

from DMARCReporting.decompressor import DecompressorFactory
from DMARCReporting.parser import DMARCRuaParser
from DMARCReporting.renderer import ConsoleRenderer, CSVRenderer
from DMARCReporting.dns import DNS
from DMARCReporting.FileLister import FileLister


class CLI():
    def execute(self, input_dir, csv_output_file=None, show_all=False):
        files = FileLister().list(input_dir)

        parser = DMARCRuaParser(DNS())
        renderer = ConsoleRenderer()
        all_data = []

        for file in files:
            file_path = join(input_dir, file)
            report = DecompressorFactory.create(file_path).decompress(file_path)
            data = parser.parse(io.BytesIO(report), include_all=show_all)
            all_data += [[*row, file] for row in data]
        renderer.render("All", all_data)

        if csv_output_file:
            renderer = CSVRenderer()
            renderer.render(csv_output_file, all_data)
