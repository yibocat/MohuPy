#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/21 下午8:25
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

__NAME = "MohuPy"
__VERSION = "0.2.2"
__AUTHOR = "Yibo Wang"
__LICENSE = "MIT"
__EMAIL = "yibocat@yeah.net"
__URI = "https://github.com/yibocat/MohuPy"
__DESCRIPTION = "MohuPy is a fuzzy set calculation library, " \
                "which contains fuzzy numbers, fuzzy measure, " \
                "fuzzy sets and fuzzy membership functions. "
about = {
    "name": __NAME,
    "version": __VERSION,
    "author": __AUTHOR,
    "license": __LICENSE,
    "email": __EMAIL,
    "url": __URI,
    "description": __DESCRIPTION
}
install_requires = [
    "numpy",
    "scipy",
    "matplotlib",
    "pandas",
    "networkx",
    'gputil'
]
