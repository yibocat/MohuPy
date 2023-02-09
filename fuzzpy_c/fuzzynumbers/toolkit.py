from .qrungdhfe import qrungdhfe
from .qrungifn import qrungifn


def dh_fn_max(dhf: qrungdhfe):
    newfn = qrungifn(dhf.qrung, 0, 0)
    newfn.md = dhf.md.max()
    newfn.nmd = dhf.nmd.max()
    return newfn


def dh_fn_min(dhf: qrungdhfe):
    newfn = qrungifn(dhf.qrung, 0, 0)
    newfn.md = dhf.md.min()
    newfn.nmd = dhf.nmd.min()
    return newfn


def dh_fn_mean(dhf: qrungdhfe):
    newfn = qrungifn(dhf.qrung, 0, 0)
    newfn.md = dhf.md.mean()
    newfn.nmd = dhf.nmd.mean()
    return newfn