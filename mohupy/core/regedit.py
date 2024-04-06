#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/6 下午2:35
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from collections.abc import MutableMapping


class Registry(MutableMapping):
    __slots__ = "__dict"

    def __init__(self, *args, **kwargs):
        super(Registry, self).__init__(*args, **kwargs)
        self.__dict = dict(*args, **kwargs)

    def register(self, target):
        def add_register_item(key, value):
            if not callable(value):
                raise Exception('register object must be callable, but receive:{} is not callable.'.format(type(value)))
            if key in self.__dict:
                print('waring: {} has been registered before.'.format(value.__name__))
            self[key] = value
            return value

        return add_register_item(target, target) if callable(target) else \
            lambda x: add_register_item(target, x)

    def __call__(self, *args, **kwargs):
        return self.register(*args, **kwargs)

    def __setitem__(self, key, value):
        self.__dict[key] = value

    def __getitem__(self, key):
        return self.__dict[key]

    def __contains__(self, key):
        return key in self.__dict

    def __delitem__(self, key):
        return self.__dict.__delitem__(key)

    def __len__(self):
        return self.__dict.__len__()

    def __iter__(self):
        return self.__dict.__iter__()

    def __str__(self):
        return str(self.__dict)

    def __repr__(self):
        return str(self.__dict)

    def keys(self):
        return self.__dict.keys()

    def values(self):
        return self.__dict.values()

    def items(self):
        return self.__dict.items()