import numpy as np

from .IVFuzzyNums import IVFuzzynum


class qrungivfn(IVFuzzynum):
    def __init__(self, qrung, mdl, mdu, nmdl, nmdu):
        super().__init__()
        mdl = np.asarray(mdl)
        mdu = np.asarray(mdu)
        nmdl = np.asarray(nmdl)
        nmdu = np.asarray(nmdu)

        assert mdl <= mdu and nmdl <= nmdu, \
            'ERROR: The upper limit of membership degree is greater than the lower limit.'
        assert 0 <= mdl <= 1 and 0 <= mdu <= 1 and 0 <= nmdl <= 1 and 0 <= nmdu <= 1, \
            'ERROR: The membership degree and non-membership degree must be in the interval[0,1]'
        assert 0 <= mdl ** qrung + nmdl ** qrung <= 1 and 0 <= mdu ** qrung + nmdu ** qrung <= 1, \
            'ERROR: The sum of membership degree and non-membership degree must be in the interval[0,1]'

        self.mdl = mdl
        self.mdu = mdu
        self.nmdl = nmdl
        self.nmdu = nmdu
        self.qrung = qrung

    def __repr__(self):
        return 'QRungIVFN(Q=%d):' % self.qrung + \
            '(\n MD: [' + str(np.around(self.mdl, 4)) + ',' + str(np.around(self.mdu, 4)) + ']\n NMD:[' + str(
                np.around(self.nmdl, 4)) + ',' + str(np.around(self.nmdu, 4)) + '])'

    def isLegal(self):
        """
            Check if the Q-rung interval-valued fuzzy number is legal.
        """
        assert self.mdl <= self.mdu and self.nmdl <= self.nmdu, \
            'ERROR: Illegal Q-rung interval-valued fuzzy number! ' \
            'The upper limit of membership degree is greater than the lower limit.'
        assert 0 <= self.mdl <= 1 and 0 <= self.mdu <= 1 and 0 <= self.nmdl <= 1 and 0 <= self.nmdu <= 1, \
            'ERROR: Illegal Q-rung interval-valued fuzzy number! ' \
            'The membership degree and non-membership degree must be in the interval[0,1]'
        assert 0 <= self.mdl ** self.qrung + self.nmdl ** self.qrung <= 1 and 0 <= self.mdu ** self.qrung + self.nmdu ** self.qrung <= 1, \
            'ERROR: Illegal Q-rung interval-valued fuzzy number! ' \
            'The sum of membership degree and non-membership degree must be in the interval[0,1]'
