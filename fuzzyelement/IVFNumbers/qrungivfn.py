import numpy as np

from .IVFuzzyNums import IVFuzzynum


class qrungivfn(IVFuzzynum):
    def __init__(self, qrung, md, nmd):
        super().__init__()
        md = np.array(md)
        nmd = np.array(nmd)

        assert md[0] <= md[1] and nmd[0] <= nmd[1], \
            'ERROR: The upper limit of membership degree is greater than the lower limit.'
        assert 0 <= md[0] <= 1 and 0 <= md[1] <= 1 and 0 <= nmd[0] <= 1 and 0 <= nmd[1] <= 1, \
            'ERROR: The membership degree and non-membership degree must be in the interval[0,1]'
        assert 0 <= md[0] ** qrung + nmd[0] ** qrung <= 1 and 0 <= md[1] ** qrung + nmd[1] ** qrung <= 1, \
            'ERROR: The sum of membership degree and non-membership degree must be in the interval[0,1]'

        self.md = md
        self.nmd = nmd
        self.qrung = qrung

    def __repr__(self):
        return 'QRungIVFN(Q=%d):' % self.qrung + \
            '(\n MD: [' + str(np.around(self.md[0], 4)) + ',' + str(np.around(self.md[1], 4)) + ']\n NMD:[' + str(
                np.around(self.nmd[0], 4)) + ',' + str(np.around(self.nmd[1], 4)) + '])'

    def isLegal(self):
        """
            Check if the Q-rung interval-valued fuzzy number is legal.
        """
        if not (len(self.md) == 2 and len(self.nmd) == 2):
            return False
        elif not (self.md[0] <= self.md[1] and self.nmd[0] <= self.nmd[1]):
            # print('ERROR: Illegal Q-rung interval-valued fuzzy number! ' +
            #       'The upper limit of membership degree is greater than the lower limit.')
            return False
        elif not (0 <= self.md[0] <= 1 and 0 <= self.md[1] <= 1 and
                  0 <= self.nmd[0] <= 1 and 0 <= self.nmd[1] <= 1):
            # print('ERROR: Illegal Q-rung interval-valued fuzzy number! ' +
            #       'The membership degree and non-membership degree must be in the interval[0,1]')
            return False
        elif not (0 <= self.md[0] ** self.qrung + self.nmd[0] ** self.qrung <= 1 and
                  0 <= self.md[1] ** self.qrung + self.nmd[1] ** self.qrung <= 1):
            # print('ERROR: Illegal Q-rung interval-valued fuzzy number!'+
            #       'The sum of membership degree and non-membership degree must be in the interval[0,1]')
            return False
        else:
            return True
