#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/30 下午5:49
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from .regedit import Register
from .core.interface import mohuParent

# Fuzzy number type registry
fuzzType = Register()

# Initialize fuzzy parent class, also indicates the currently used fuzzy number type
# It is worth noting: fuzzyParent is a dictionary whose keys represent parent classes
# and values represent subclasses.
fuzzParent = mohuParent.memo
