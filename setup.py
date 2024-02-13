#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/21 下午8:25
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from setuptools import setup, find_packages
from information import *

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=about['name'],
    packages=find_packages(),
    description=about['description'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=about['version'],
    author=about['author'],
    author_email=about['email'],
    url=about['url'],
    license=about['license'],
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.10',
    install_requires=install_requires,
)
