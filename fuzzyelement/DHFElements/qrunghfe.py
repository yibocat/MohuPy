#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/1 下午5:37
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzyKit

import numpy as np
from .DHFuzzy import DhFuzzy


class qrunghfe(DhFuzzy):
    # noinspection PyUnresolvedReferences
    """
        qrunghfe is a class representing the Q-Rung hesitant fuzzy sets model. It is inherited from the DHFuzzy class.

        Attributes
        ----------
            md : numpy.ndarray, shape = (n_numbers), indicates the number of membership degrees
            nmd : numpy.ndarray, shape = (n_numbers), indicates the number of non-membership degrees
            qrung : numpy.ndarray, shape = (n_numbers), indicates the Q rung of the elements

        Function
        ---------
            __init__(self, md, nmd): Initializes a Q-Rung dual hesitant fuzzy element
            __repr__(self): Returns a string representation of the Q-Rung dual hesitant fuzzy element
        """

    def __init__(self, qrung, md, nmd):
        super().__init__()
        md = np.asarray(md)
        nmd = np.asarray(nmd)
        self.qrung = qrung
        assert (md.size == 0 or nmd.size == 0) or (
                max(md) <= 1 and max(nmd) <= 1 and min(md) >= 0 and min(nmd) >= 0) and (
                       0 <= max(md) ** self.qrung + max(nmd) ** self.qrung <= 1), \
            "ERROR:Construction failed! max(MD)^q+max(NMD)^q and min(MD)^q+min(NMD)^q must be in interval[0,1]!"
        self.md = md
        self.nmd = nmd

    def __repr__(self):
        if len(self.md) > 50 or len(self.nmd) > 50:
            return 'QRungHFE(Q=%d)[%d,%d]:{' % (self.qrung, len(self.md), len(self.nmd)) + \
                '\n md :' + str(np.round(self.md, 4)[:50]) + \
                ',\n nmd:' + str(np.round(self.nmd, 4)[:50]) + ' }\n'
        else:
            return 'QRungHFE(Q=%d)[%d,%d]:{' % (self.qrung, len(self.md), len(self.nmd)) + \
                '\n md :' + str(np.round(self.md, 4)) + \
                ',\n nmd:' + str(np.round(self.nmd, 4)) + ' }\n'

    @property
    def parent(self):
        for base in self.__class__.__bases__:
            return base.__name__

    def isLegal(self):
        """
            Checks if the Q-Rung hesitant fuzzy element is legal.
        """
        if (self.md.size == 0 or self.nmd.size == 0) or \
                (max(self.md) <= 1 and max(self.nmd) <= 1 and min(self.md) >= 0 and min(self.nmd) >= 0) \
                and (0 <= max(self.md) ** self.qrung + max(self.nmd) ** self.qrung <= 1):
            return True
        else:
            # print('ERROR: Illegal Q-rung hesitant fuzzy element!')
            return False
