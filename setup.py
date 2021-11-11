from logging import INFO
from setuptools import PackageFinder, setup
from setuptools import find_packages
import os



BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VERSION = '1.0.0'
PACKAGES = find_packages()
NAME = 'Encrypt-py'

INSTALL_REQUIRES = [
    'Cython==0.29.24',
    'PyYAML==5.4.1'
]


setup(
    name=NAME,  # package name
    version=VERSION,  # package version
    author="sk",
    author_email="ldu_sunkaixuan@163.com",
    description='python Encryption program',  # package description
    license="MIT",
    install_requires=INSTALL_REQUIRES,
    entry_points={"console_scripts": ["encrypt = encryptpy.cmdline:execute"]},
    packages=find_packages(),
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3"],
)