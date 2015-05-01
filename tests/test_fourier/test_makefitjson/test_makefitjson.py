#!/usr/bin/env python3

import unittest
import json

from dftintegrate.fourier import fitdata
from dftintegrate import customserializer as cs


class TestCreateFitJson(unittest.TestCase):

    def setUp(self):
        self.cases = [str(x) for x in range(1, 2)]
        self.root = './tests/test_fourier/test_makefitjson/'

    def readfile(self, case, check_or_ans, filename):
        with open(self.root+check_or_ans+'/test'+case+'/'+filename+'.json',
                  'r', encoding='utf-8') as inf:
            return json.load(inf, object_hook=cs.fromjson)

    def assertCloseEnough_ListofComplex(self, answer, tocheck, case, test):
        for i in range(len(answer)):
                    self.assertEqual(round(answer[i].real, 14),
                                     round(tocheck[i].real, 14),
                                     msg=test+' case '+case)
                    self.assertEqual(round(answer[i].imag, 14),
                                     round(tocheck[i].imag, 14),
                                     msg=test+' case '+case)

    def test_runtestcases(self):
        for case in self.cases:
            fitdata.FitData(self.root+'tocheck/test'+case)
            answer = self.readfile(case, 'answer', 'fit')
            tocheck = self.readfile(case, 'tocheck', 'fit')
            recips_ans = answer['reciprocals']
            recips_tocheck = tocheck['reciprocals']
            series_ans = answer['series']
            series_tocheck = tocheck['series']
            coeffs_ans = answer['coefficients']
            coeffs_tocheck = answer['coefficients']

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
                        print('\nseries row not the same length case '+case)
            else:
                print('\nseries not the same length case '+case)

            if len(coeffs_ans) == len(coeffs_tocheck):
                self.assertCloseEnough_ListofComplex(coeffs_ans,
                                                     coeffs_tocheck,
                                                     case,
                                                     'coeffs')
            else:
                print('\ncoeffs not same length case '+case)
