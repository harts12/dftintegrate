#!/usr/bin/env python3
"""
The purpose of this script is to generate answers for unit tests. I can
type in the answer I expect and it puts it in json form so I can
compare it to the dftintegrate's outputed json.
"""
import json
from dftintegrate import customserializer as cs


def serialize(dict_, filename):
    with open(filename, 'w', encoding='utf-8') as out:
        json.dump(dict_, out, indent=2, default=cs.tojson)


if __name__ == '__main__':
    dict_ = {
        "coefficients": [2.5, 0.0, -0.16666667, 0.166666667j, -0.16666667,
                         0, -0.5, -0.5j],
        "reciprocals": {"(0, 0, 0)": [[0, 0, 0]],
                        "(0, 0, 1)": [[0, 0, 1], [1, 0, 0], [0, 1, 0]],
                        "(0, 1, 1)": [[0, 1, 1], [1, 0, 1], [1, 1, 0]],
                        "(1, 1, 1)": [[1, 1, 1]]},
        "series": [[(1+0j), (3+0j), (3+0j), (1+0j)],
                   [(1+0j), (0+3j), (-3+0j), (0-1j)],
                   [(1+0j), (-3+0j), (3+0j), (-1+0j)],
                   [(1+0j), (0-3j), (-3+0j), (0+1j)]]
    }
    filename = "/Users/matt/codes/projects/dftintegrate/tests/fourier/makefitjson/answer/test1/fit.json"
    serialize(dict_, filename)
