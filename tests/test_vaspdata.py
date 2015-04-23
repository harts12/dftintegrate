#!/usr/bin/env python3

import unittest

from os import remove
from dftintegrate.fourier import vaspdata


class TestVASPDataSiMedium(unittest.TestCase):

    def setUp(self):
        self.root_folder = 'tests'
        self.data = vaspdata.VASPData(self.root_folder +
                                      '/test_input/Si_medium')
        with open(self.root_folder +
                  '/expected_output/Si_medium/kpts_eigenvals.dat', 'r') as inf:
            self.kpts_eigenvals = inf.read()
        with open(self.root_folder +
                  '/expected_output/Si_medium/symops_trans.dat', 'r') as inf:
            self.symops_trans = inf.read()
        with open(self.root_folder +
                  '/expected_output/Si_medium/kmax.dat', 'r') as inf:
            self.kmax = inf.read()

    def tearDown(self):
        folder = self.root_folder+'/test_input/Si_medium/'
        files = ['kpts_eigenvals.dat', 'symops_trans.dat', 'kmax.dat']
        for f in files:
            remove(folder+f)

    def test_extract_symops_trans_Si_medium(self):
        with open(self.root_folder +
                  '/test_input/Si_medium/symops_trans.dat', 'r') as inf:
            result = inf.read()
        self.assertEqual(self.symops_trans, result)

    def test_extract_kpts_eigenvals_Si_medium(self):
        with open(self.root_folder +
                  '/test_input/Si_medium/kpts_eigenvals.dat', 'r') as inf:
            result = inf.read()
        self.assertEqual(self.kpts_eigenvals, result)

    def test_extract_kmax_Si_medium(self):
        with open(self.root_folder +
                  '/test_input/Si_medium/kmax.dat', 'r') as inf:
            result = inf.read()
        self.assertEqual(self.kmax, result)


class TestVASPDataSi2x2x2(unittest.TestCase):

    def setUp(self):
        self.root_folder = 'tests'
        self.maxDiff = None
        self.data = vaspdata.VASPData(self.root_folder +
                                      '/test_input/Si2x2x2')
        with open(self.root_folder +
                  '/expected_output/Si2x2x2/kpts_eigenvals.dat', 'r') as inf:
            self.kpts_eigenvals = inf.read()
        with open(self.root_folder +
                  '/expected_output/Si2x2x2/symops_trans.dat', 'r') as inf:
            self.symops_trans = inf.read()
        with open(self.root_folder +
                  '/expected_output/Si2x2x2/kmax.dat', 'r') as inf:
            self.kmax = inf.read()

    def tearDown(self):
        folder = self.root_folder+'/test_input/Si2x2x2/'
        files = ['kpts_eigenvals.dat', 'symops_trans.dat', 'kmax.dat']
        for f in files:
            remove(folder+f)

    def test_extract_symops_trans_Si2x2x2(self):
        with open(self.root_folder +
                  '/test_input/Si2x2x2/symops_trans.dat', 'r') as inf:
            result = inf.read()
        self.assertEqual(self.symops_trans, result)

    def test_extract_kpts_eigenvals_Si2x2x2(self):
        with open(self.root_folder +
                  '/test_input/Si2x2x2/kpts_eigenvals.dat', 'r') as inf:
            result = inf.read()
        self.assertEqual(self.kpts_eigenvals, result)

    def test_extract_kmax_Si2x2x2(self):
        with open(self.root_folder +
                  '/test_input/Si2x2x2/kmax.dat', 'r') as inf:
            result = inf.read()
        self.assertEqual(self.kmax, result)


if __name__ == '__main__':
    unittest.main()
