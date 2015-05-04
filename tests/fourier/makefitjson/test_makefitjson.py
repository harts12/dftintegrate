#!/usr/bin/env python3

import unittest
import os

from tests import testfunctions
from dftintegrate.fourier import fitdata


class TestMakeFitJson(unittest.TestCase, testfunctions.TestFunctions):

    def setUp(self):
        print('Testing the creation of fit.json.')
        self.root = './tests/fourier/makefitjson/'
        num = len([name for name in os.listdir(self.root+'tocheck/')])
        self.cases = [str(x) for x in range(1, num+1)]

    def test_runtestcases(self):
        for case in self.cases:
            print('  Testing case '+case+'...')
            fitdata.FitData(self.root+'tocheck/test'+case)
            answer = self.readjson(case, 'answer', 'fit')
            tocheck = self.readjson(case, 'tocheck', 'fit')
            recips_ans = answer['reciprocals']
            recips_tocheck = tocheck['reciprocals']
            series_ans = answer['series']
            series_tocheck = tocheck['series']
            coeffs_ans = answer['coefficients']
            coeffs_tocheck = tocheck['coefficients']

            self.assertEqual(recips_ans, recips_tocheck,
                             msg='recips case '+case)

            if len(series_ans) == len(series_tocheck):
                for i in range(len(series_ans)):
                    if len(series_ans[i]) == len(series_tocheck[i]):
                        self.assertCloseEnough_ListofComplex(series_ans[i],
                                                             series_tocheck[i],
                                                             case,
                                                             'series')
                    else:
                        self.assertEqual(len(series_ans[i]),
                                         len(series_tocheck[i]),
                                         msg="series row not the same"
                                             " length case "+case)
            else:
                self.assertEqual(len(series_ans), len(series_tocheck),
                                 msg='series not the same length case '+case)

            if len(coeffs_ans) == len(coeffs_tocheck):
                for i in range(1, len(coeffs_ans.keys())+1):
                    i = str(i)
                    if len(coeffs_ans[i]) == len(coeffs_tocheck[i]):
                        self.assertCloseEnough_ListofComplex(coeffs_ans[i],
                                                             coeffs_tocheck[i],
                                                             case,
                                                             'coeffs')
                    else:
                        self.assertEqual(len(coeffs_ans[i]),
                                         len(coeffs_tocheck[i]),
                                         msg='coeffs for band '+i+' not same'
                                         ' length case '+case)
            else:
                self.assertEqual(len(coeffs_ans), len(coeffs_tocheck),
                                 msg='coeffs not same number of bands'
                                     ' case '+case)

if __name__ == '__main__':
    unittest.main()
