from setuptools import  setup
from setuptools import find_packages

VERSION = '1.0.0'
PACKAGES = find_packages()
NAME = 'Encrypt-py'

INSTALL_REQUIRES = [
    'Cython==0.29.24',
    'PyYAML==5.4.1'
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=NAME,  # package name
    version=VERSION,  # package version
    author="sk",
    author_email="ldu_sunkaixuan@163.com",
    description='python Encryption program',  # package description
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    install_requires=INSTALL_REQUIRES,
    entry_points={"console_scripts": ["encrypt = encryptpy.cmdline:execute"]},
    packages=find_packages(),
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3",
                 "Programming Language :: Python :: Implementation :: CPython"],
)