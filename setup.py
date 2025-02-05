#!/usr/bin/env python

import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="Avlos",
    version="0.3.0",
    description="Avlos Remote Object Templating System",
    author="Yannis Chatzikonstantinou",
    author_email="yannis@tinymovr.com",
    url="https://www.tinymovr.com",
    packages=find_packages(include=["avlos", "avlos.*"]),
    python_requires=">=3.6",
    install_requires=["marshmallow", "pyyaml", "pint", "docopt", "jinja2", "rstcheck"],
    entry_points={"console_scripts": ["avlos=avlos.cli:run_cli"]}
)
