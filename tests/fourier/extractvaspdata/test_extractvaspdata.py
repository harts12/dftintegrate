#!/usr/bin/env python3

import unittest

from tests import testfunctions
from dftintegrate.fourier import vaspdata


class TestExtractingVASPDataToDatFiles(unittest.TestCase,
                                       testfunctions.TestFunctions):

    def setUp(self):
        print('Testing extracting VASP data to .dat files...')
        self.cases = [str(x) for x in range(1, 3)]
        self.root = './tests/fourier/extractvaspdata/'

    def test_runtestcases(self):
        for case in self.cases:
            print('  Testing case '+case+'...')
            vaspdata.VASPData(self.root+'tocheck/test'+case)
            kpts_eigenvals_ans = self.readfile(case, 'answer',
                                               'kpts_eigenvals')
            kpts_eigenvals_tocheck = self.readfile(case, 'tocheck',
                                                   'kpts_eigenvals')
            self.assertEqual(kpts_eigenvals_ans, kpts_eigenvals_tocheck,
                             msg='kpts_eigenvals case '+case)

            symops_trans_ans = self.readfile(case, 'answer',
                                             'symops_trans')
            symops_trans_tocheck = self.readfile(case, 'tocheck',
                                                 'symops_trans')
            self.assertEqual(symops_trans_ans, symops_trans_tocheck,
                             msg='symops_trans case '+case)

            kmax_ans = self.readfile(case, 'answer', 'kmax')
            kmax_tocheck = self.readfile(case, 'tocheck', 'kmax')
            self.assertEqual(kmax_ans, kmax_tocheck, msg='kmax case '+case)
