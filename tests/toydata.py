#!/usr/bin/env python3
"""Produce kpts_egienvals.dat and kmax.dat for some toy functions for
testing. symops_trans.dat is simply pasted in the right directory
by the user.

Classes:
  ToyFunction -- Parent class to facilitate specific cases below.

  Cubic -- Represent exp(cos(2pix)+cos(2piy)+cos(2piz))

  FCC -- Represent exp(cos(2pi(x+y+z))+cos(2pi(-x+y+z))+
                       cos(2pi(x-y+z))+cos(2pi(x+y-z)))

  BCC -- Represent exp(cos(2pi(x+y))+cos(2pi(y+z))+cos(2pi(x+z))+
                       cos(2pi(x-y))+cos(2pi(y-z))+cos(2pi(x-z)))

  CBF -- Combine cubic, fcc, and bcc to make a function with three
    energy bands.

  ToyData -- Call the toy function classes to generate .dat (txt) files
    from analytic test functions for readata.py to use.

"""
import numpy as np
from itertools import product


class toyFunction(object):

    def __init__(self, points=10):
        self.kgrid = [k for k in product([i/points for i in range(points)],
                                         repeat=3)]
        self.kmax = np.ceil(points/(2*np.sqrt(3)))
        self.eigenvals = {}

    def tofile(self):
        root = 'tests/test_input/'+self.name+'/'
        with open(root+'kmax.dat', 'w') as outf:
            outf.write(str(self.kmax))
        with open(root+'kpts_eigenvals.dat', 'w') as outf:
            for i, k in enumerate(self.kgrid):
                outf.write(' '.join(str(x) for x in k)+'\n')
                for key, value in sorted(self.eigenvals.items()):
                    outf.write(key+'    '+str(value[i])+'\n')
                outf.write('\n')


class bcc(toyFunction):

    def __init__(self, points=10):
        toyFunction.__init__(self, points)
        self.name = 'bcc'
        self.eigenvals['1'] = [np.exp(np.cos(2*np.pi*(k[0] + k[1])) +
                                      np.cos(2*np.pi*(k[1] + k[2])) +
                                      np.cos(2*np.pi*(k[0] + k[2])) +
                                      np.cos(2*np.pi*(k[0] - k[1])) +
                                      np.cos(2*np.pi*(k[1] - k[2])) +
                                      np.cos(2*np.pi*(k[0] - k[2])))
                               for k in self.kgrid]
        toyFunction.tofile(self)


class fcc(toyFunction):

    def __init__(self, points=10):
        toyFunction.__init__(self, points)
        self.name = 'fcc'
        self.eigenvals['1'] = [np.exp(np.cos(2*np.pi*(k[0] + k[1] + k[2])) +
                                      np.cos(2*np.pi*(k[1] - k[0] + k[2])) +
                                      np.cos(2*np.pi*(k[0] - k[1] + k[2])) +
                                      np.cos(2*np.pi*(k[0] - k[2] + k[1])))
                               for k in self.kgrid]
        toyFunction.tofile(self)


class cubic(toyFunction):

    def __init__(self, points=10):
        toyFunction.__init__(self, points)
        self.name = 'cubic'
        self.eigenvals['1'] = [np.exp(np.cos(2*np.pi*k[0]) +
                                      np.cos(2*np.pi*k[1]) +
                                      np.cos(2*np.pi*k[2]))
                               for k in self.kgrid]
        toyFunction.tofile(self)


class cbf(toyFunction):

    def __init__(self, points=10):
        toyFunction.__init__(self, points)
        self.name = 'cbf'
        self.eigenvals['1'] = [np.exp(np.cos(2*np.pi*k[0]) +
                                      np.cos(2*np.pi*k[1]) +
                                      np.cos(2*np.pi*k[2]))
                               for k in self.kgrid]
        self.eigenvals['2'] = [np.exp(np.cos(2*np.pi*(k[0] + k[1] + k[2])) +
                                      np.cos(2*np.pi*(k[1] - k[0] + k[2])) +
                                      np.cos(2*np.pi*(k[0] - k[1] + k[2])) +
                                      np.cos(2*np.pi*(k[0] - k[2] + k[1])))
                               for k in self.kgrid]
        self.eigenvals['3'] = [np.exp(np.cos(2*np.pi*(k[0] + k[1])) +
                                      np.cos(2*np.pi*(k[1] + k[2])) +
                                      np.cos(2*np.pi*(k[0] + k[2])) +
                                      np.cos(2*np.pi*(k[0] - k[1])) +
                                      np.cos(2*np.pi*(k[1] - k[2])) +
                                      np.cos(2*np.pi*(k[0] - k[2])))
                               for k in self.kgrid]
        toyFunction.tofile(self)

if __name__ == '__main__':
    cubic()
    bcc()
    fcc()
    cbf()
