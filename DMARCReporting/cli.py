
from os import listdir
from os.path import isfile
from os.path import join

from DMARCReporting.parser import DMARCRuaParser
from DMARCReporting.renderer import ConsoleRenderer


class CLI():
    def execute(self, input_dir):
        reports = [f for f in listdir(
            input_dir) if isfile(join(input_dir, f))]

        parser = DMARCRuaParser()
        renderer = ConsoleRenderer()

        for report in reports:
            data = parser.parse(join(input_dir, report))
            renderer.render(data)
