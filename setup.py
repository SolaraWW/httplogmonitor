import os
from setuptools import setup
from setuptools import find_packages

import versioneer

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def read_file(filename):
    filepath = os.path.join(BASE_DIR, filename)
    with  open(filepath) as f:
        return f.read()

REQUIREMENTS = read_file("requirements.txt").splitlines()


setup(
    name="httpmonitor",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="An HTTP log monitor",
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/danielfrg/httpmonitor",
    maintainer="Daniel Rodriguez",
    maintainer_email="df.rodriguez143@gmail.com",
    license="Apache 2.0",
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    zip_safe=False,
)
