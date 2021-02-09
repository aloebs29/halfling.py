from distutils.core import setup

setup(
    name="halfling",
    version="0.0.1",
    author="Andrew Loebs",
    license="LICENSE",
    description="Minimal C/++ build system written in Python.",
    long_description=open("README.rst").read(),

    packages=["halfling"],
    scripts=["bin/halfling"],
)
