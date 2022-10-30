import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="DMARCReporting",
    version="0.2.0",
    description="Simple tool to extract error reports from DMARC files",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/MozaicWorks/DMARCReporting",
    author="Mozaic Works",
    author_email="alex.bolboaca@mozaicworks.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    packages=find_packages(exclude=("tests",)),
    install_requires=["lxml", "tabulate"],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'DMARCReporting=DMARCReporting:main',
        ],
    },
)
