#!/usr/bin/env python3

import unittest
import os

from tests import testfunctions
from dftintegrate.fourier import readdata


class TestMakeDataJson(unittest.TestCase, testfunctions.TestFunctions):

    def setUp(self):
        print('Testing making data.json.')
        self.root = './tests/fourier/makedatajson/'
        num = len([name for name in os.listdir(self.root+'tocheck/')])
        self.cases = [str(x) for x in range(1, num+1)]

    def test_runtestcases(self):
        for case in self.cases:
            print('  Testing case '+case+'...')
            readdata.ReadData(self.root+'tocheck/test'+case)
            answer = self.readjson(case, 'answer', 'data')
            tocheck = self.readjson(case, 'tocheck', 'data')
            weights_ans = answer['weights']
            weights_tocheck = tocheck['weights']
            kmax_ans = answer['kmax']
            kmax_tocheck = tocheck['kmax']
            kgrid_ans = answer['kgrid']
            kgrid_tocheck = tocheck['kgrid']
            trans_ans = answer['trans']
            trans_tocheck = tocheck['trans']
            symops_ans = answer['symops']
            symops_tocheck = tocheck['symops']
            eigenvals_ans = answer['eigenvals']
            eigenvals_tocheck = tocheck['eigenvals']
            self.assertEqual(weights_ans, weights_tocheck,
                             msg='weights case '+case)
            self.assertEqual(kmax_ans, kmax_tocheck, msg='kmax case '+case)
            self.assertEqual(kgrid_ans, kgrid_tocheck, msg='kgrid case '+case)
            self.assertEqual(trans_ans, trans_tocheck, msg='trans case '+case)
            self.assertEqual(symops_ans, symops_tocheck,
                             msg='symops case '+case)
            self.assertEqual(eigenvals_ans, eigenvals_tocheck,
                             msg='eigenvals case '+case)

if __name__ == '__main__':
    unittest.main()
