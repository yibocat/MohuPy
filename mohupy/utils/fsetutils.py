#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/21 下午8:25
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from ..config import import_cupy_lib, import_cudf_lib

from ..mohunums import mohunum
from ..mohusets import mohuset
from .fnumutils import str_to_mohunum

np = import_cupy_lib()
pd = import_cudf_lib()


def asmohuset(x, copy=False):
    """
        Convert a fuzzy numpy array to a fuzzy set.

        Parameters
        ----------
            x:  numpy.ndarray or list
                The fuzzy numpy array.
            copy:  bool
                Whether to copy the array.
        Returns
        -------
            fuzzyset
                A fuzzy set.
    """
    if copy:
        xt = np.copy(x)
    else:
        xt = x

    fl = np.asarray(xt)
    shape = fl.shape
    y = fl.ravel()

    newset = mohuset(y[0].qrung, y[0].__class__.__name__)
    for num in y:
        newset.append(num)
    newset.reshape(shape)
    return newset


def rand_set(qrung=None, mtype=None, *n):
    """
        Generate a random fuzzy set.

        Parameters
        ----------
            mtype:  str
                The type of the set.
                Optional: 'fn' or 'ivfn'.
            qrung:  int
                The number of elements in the set.
            *n:  int
                The shape of the random fuzzy set.
        Returns
        -------
            fuzzyset
                A fuzzy set.
    """
    r = mohuset(qrung, mtype)
    return r.random(*n)


def savez(mohu: mohuset, path: str):
    """
        Save a fuzzy set to a file.

        This method not only saves the fuzzy set, but also saves the relevant
        information of the fuzzy set.
        Specific storage content:
            1. The set of the fuzzy set
            2. The qrung of the fuzzy set
            3. The shape of the fuzzy set
            4. The type of the fuzzy set

        Parameters
        ----------
            mohu:  mohuset
                The fuzzy set.
            path:  str
                The path to the file.

        Returns
        -------
            Boolean

        Notes
        -----
            This method saves the fuzzy set to a .npz file.
    """
    try:
        mohu.savez(path)
        return True
    except Exception as e:
        print(e, 'Save failed.')
        return False


def loadz(path: str):
    """
        Load a fuzzy set from a .npz file.

        This method not only loads the fuzzy set, but also loads the relevant
        information of the fuzzy set.
        Specific storage content:
            1. The set of the fuzzy set
            2. The qrung of the fuzzy set
            3. The shape of the fuzzy set
            4. The type of the fuzzy set

        Parameters
        ----------
            path:  str
                The path to the file.

        Returns
        -------
            mohuset
                The fuzzy set.

        Notes
        -----
            This method loads the fuzzy set from a.npz file.
    """
    newset = mohuset()
    try:
        newset.loadz(path)
        return newset
    except Exception as e:
        print(e, 'Load failed.')


def to_csv(mohu: mohuset, path: str):
    """
        Save a fuzzy set to a .csv file.

        This method only saves the fuzzy set, and does not save the related
        information of the set.

        Parameters
        ----------
            mohu:  mohuset
                The fuzzy set.
            path:  str
                The path to the file.

        Returns
        -------
            Boolean

        Notes
        -----
            This method saves the fuzzy set to a.csv file.
    """
    try:
        mohu.mat.to_csv(path)
        return True
    except Exception as e:
        print(e, 'Save failed.')
        return False


def load_csv(path: str, q: int, mtype='fn'):
    """
        Load a fuzzy set from a.csv file.

        This method is used to load a fuzzy set table with unknown information. It
        is necessary to judge the content of the fuzzy table during loading. When
        initializing a fuzzy set, Q-rung and fuzzy set type are given, so it is necessary
        to judge whether a fuzzy set meets these two conditions. This method will only
        load when the fuzzy set table is equal to or satisfied with the initial fuzzy set
        condition.

        Parameters
        ----------
            path:  str
                The path to the file.
            q:  int
                The q rung of the fuzzy set.
            mtype:  str
                The type of the fuzzy set.

        Returns
        -------
            mohuset
                The fuzzy set.

        Notes
        -----
            This method loads the fuzzy set from a.csv file.
    """
    try:
        m = np.asarray(pd.read_csv(path, index_col=0))
        vect_func = np.vectorize(str_to_mohunum)
        fset = vect_func(m, q, mtype)

        newset = mohuset(q, mtype)
        newset.setter(fset, m.shape, m.ndim, m.size)
        return newset
    except Exception as e:
        print(e, 'Load failed.')


def func4num(func, mohu: mohuset, *args):
    """
        Apply a function to a fuzzy set.

        Parameters
        ----------
            func:  function
                The function to apply to the all num of fuzzy set
            mohu:  mohuset
                The fuzzy set.
            *args:  list
                The arguments of the function.
        Returns
        -------
            mohuset
    """
    vec_func = np.vectorize(func)
    newset = mohuset(mohu.qrung, mohu.mtype)
    newset.setter(vec_func(mohu.set, *args),
                  mohu.set.shape,
                  mohu.set.ndim,
                  mohu.set.size)
    return newset


def rand_choice(f: mohuset) -> mohunum:
    """
        Randomly select a fuzzy number

        Parameters
        ----------
            f:  mohuset
                The fuzzy set.

        Returns
        -------
            mohunum
    """
    return np.random.choice(f.set.flatten())


















