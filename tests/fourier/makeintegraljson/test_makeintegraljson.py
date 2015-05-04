#!/usr/bin/env python3

import unittest
import os

from tests import testfunctions
from dftintegrate.fourier import integratedata


class TestMakeIntegralJson(unittest.TestCase, testfunctions.TestFunctions):

    def setUp(self):
        print('Testing making integral.json.')
        self.root = './tests/fourier/makeintegraljson/'
        num = len([name for name in os.listdir(self.root+'tocheck/')])
        self.cases = [str(x) for x in range(1, num+1)]

    def test_runtestcases(self):
        for case in self.cases:
            for points in range(1, 3):
                integratedata.IntegrateData(self.root+'tocheck/test'+case,
                                            points)
                answer = self.readjson(case, 'answer', 'integral')
                tocheck = self.readjson(case, 'tocheck', 'integral')
                recint_ans = answer['rectangleintegrals']
                recint_tocheck = tocheck['rectangleintegrals']
                totrecint_ans = answer['totalrectangleintegral']
                totrecint_tocheck = tocheck['totalrectangelintegral']
                gaussint_ans = answer['gaussintegrals']
                gaussint_tocheck = tocheck['gaussintegrals']
                totgaussint_ans = answer['totalgaussintegral']
                totgaussint_tocheck = tocheck['totalgaussintegral']
                self.assertEqual(1, 2, msg='Failed b/c test not written')


if __name__ == '__main__':
    unittest.main()
