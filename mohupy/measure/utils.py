#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/21 下午8:25
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import re

import networkx

from matplotlib import pyplot as plt
import numpy as np


def subsets(nums):
    """
        Subsets of a set.

        This method returns a list of subsets of a fixed set.

        Parameters
        ----------
            nums : list or np.ndarray
                    The fixed set.
        Returns
        -------
            list
            The list of subsets.
    """
    ans = []
    n = 1 << len(nums)
    for i in range(n):
        res = []
        num = i
        idx = 0
        while num:
            if num & 1:
                res.append(nums[idx])
            num >>= 1
            idx += 1
        ans.append(res)
    return ans


def str_subsets(nums):
    """
        Subsets of a set in string.

        This method returns a list of subsets(string) of a fixed set.

        Parameters
        ----------
            nums : list or np.ndarray
                    The fixed set.
        Returns
        -------
            list
            The list of subsets.
    """
    ans = []
    n = 1 << len(nums)
    for i in range(n):
        res = []
        num = i
        idx = 0
        while num:
            if num & 1:
                res.append(nums[idx])
            num >>= 1
            idx += 1
        ans.append(str(res))
    return ans


def dicts(S: list, chara='C'):
    """
        Dictionary representation of a fixed set.

        This method returns a dictionary in which each key
        corresponds to an element and the value corresponds
        to the fuzzy measure of that element.

        Parameters
        ----------
            S : list
                The fixed set.
            chara : str
                The character used to represent each element.
                The default is 'C'.
        Returns
        -------
            dict
            The dictionary of the fixed set.
    """
    n = np.asarray(S).size
    attributes = []
    for i in range(n):
        attributes.append(chara+str(i+1))

    fuzzdd = dict(zip(attributes, S))
    return fuzzdd


def hasse_diagram(e: (list, np.ndarray), func, node_char='C', r=6,
                  node_size=85000, save_path=None, figsize=(18, 12),
                  fontsize=9, transparency=0.55):
    """
        The hasse diagram of a fixed set with the given fuzzy measure function.

        This method plot the hasse diagram of a fixed set with the given
        fuzzy measure function.

        Parameters
        ----------
            e : list, np.ndarray
                The fixed set.
            func : function
                The fuzzy measure function.
                Optional: dirac_meas, add_meas, sym_meas, lambda_meas
            node_char : str
                The character used to represent each element.
                The default is 'C'.
            r:  int
                The number of digits after the decimal point.
                Default to 6.
            node_size : int
                The size of the nodes.
                The default is 85000.
            save_path : str
                The path to save the figure.
                The default is None.
            figsize : tuple
                The size of the figure.
                The default is (18, 12).
            fontsize : int
                The size of the font.
                The default is 9.
            transparency : float
                The transparency of the figure.
                The default is 0.55.
        Returns
        -------
            None
    """
    def _search_subset(pattern, st):
        """
            Search for a subset in a string.

            Parameters
            ----------
                pattern : str
                        The pattern to be searched.
                st : str
                        The string to be searched.
            Returns
            -------
                bool
        """
        if re.search(pattern, st) is not None or pattern == '{}':
            return True
        else:
            return False

    from .fuzzmeas import dict_rep
    dd = dict_rep(e, func, e, chara=node_char)

    keys = []
    for i in dd.keys():
        keys.append(i)

    values = np.array([])
    for j in dd.values():
        values = np.append(values, j)

    def value(v):
        return (v/np.sum(values))*node_size

    subset_relationships = [(s1+'\n'+str(dd[s1]), s2+'\n'+str(dd[s2]))
                            for s1 in dd.keys() for s2 in dd.keys()
                            if ((s1 != s2) and _search_subset(s1, s2))]

    Graph = networkx.DiGraph()
    Graph.add_nodes_from([s+'\n'+str(dd[s]) for s in dd])
    Graph.add_edges_from(subset_relationships)
    from . import hasse as hwx
    hwx.transitivity_elimination(Graph)
    plt.figure(figsize=figsize)
    networkx.draw_networkx(Graph,
                           node_size=[value(dd[node]) for node in keys],
                           pos=hwx.layout(Graph),
                           alpha=transparency,
                           font_size=fontsize,
                           font_family='Times New Roman',
                           font_weight='bold',
                           font_color='black')

    plt.axis('off')
    if save_path is not None:
        try:
            plt.savefig(save_path, bbox_inches='tight')
            print('Saved successfully!')
        except IOError:
            print('Save failed:')
    plt.show()
