#!/usr/bin/env python3

import unittest
import numpy as np

from os import mkdir
from shutil import rmtree
from json import load

from dftintegrate.fourier import integratedata
from dftintegrate import customserializer as cs


class TestIntegrateDataRectangles(unittest.TestCase):

    def setUp(self):
        self.root = 'tests/'
        mkdir(self.root+'temp_out/')
        self.integral = integratedata.IntegrateData(self.root+'temp_out/',
                                                    1,
                                                    loaddata=False,
                                                    integrate=False)

    def tearDown(self):
        rmtree(self.root+'temp_out/')

    def _round_integrals(self):
        for i, val in enumerate(self.check['rectangleintegrals']):
            self.check['rectangleintegrals'][i] = round(val, 14)
        for i, val in enumerate(self.check['gaussintegrals']):
            self.check['gaussintegrals'][i] = round(val, 14)
        self.check['totalrectangleintegral'] = \
            round(self.check['totalrectangleintegral'], 14)
        self.check['totalgaussintegral'] = \
            round(self.check['totalgaussintegral'], 14)

    def _test_rectangles(self):
        self.integral.serialize()
        with open(self.name) as inf:
            answer = load(inf, object_hook=cs.fromjson)
        with open(self.root+'temp_out/integral.json') as inf:
            self.check = load(inf, object_hook=cs.fromjson)
        self._round_integrals()
        check = self.check
        self.assertEqual(answer['rectangleintegrals'],
                         check['rectangleintegrals'])
        self.assertEqual(answer['totalrectangleintegral'],
                         check['totalrectangleintegral'])

    def _test_gauss(self):
        self.integral.serialize()
        with open(self.name) as inf:
            answer = load(inf, object_hook=cs.fromjson)
        with open(self.root+'temp_out/integral.json') as inf:
            self.check = load(inf, object_hook=cs.fromjson)
        self._round_integrals()
        check = self.check
        self.assertEqual(answer['gaussintegrals'],
                         check['gaussintegrals'])
        self.assertEqual(answer['totalgaussintegral'],
                         check['totalgaussintegral'])

    def test_rectangleintegral_one(self):
        self.b = [1]
        self.name = self.root+'expected_output/_rectangleintegral/one.json'
        self.integral._rectangleintegral(b=np.array(self.b))
        self._test_rectangles()

    def test_rectangleintegral_two(self):
        self.b = [1, 1, 1, 1, 1]
        self.name = self.root+'expected_output/_rectangleintegral/two.json'
        self.integral._rectangleintegral(b=np.array(self.b))
        self._test_rectangles()

    def test_rectangleintegral_three(self):
        self.b = [-3, -2, -1, 0, 1, 2, 3]
        self.name = self.root+'expected_output/_rectangleintegral/three.json'
        self.integral._rectangleintegral(b=np.array(self.b))
        self._test_rectangles()

    def test_evaluatefit_one(self):
        self.integral.set_coeffs({'1': [1]})
        self.integral.set_num('1')
        b = self.integral._evaluatefit(A=[[1]])
        self.assertEqual(1, b)

    def test_rectangles_one(self):
        self.integral.set_recips({"(0, 0, 0)": [[0, 0, 0]]})
        self.integral.set_coeffs({'1': [1], '2': [1]})
        self.integral.rectangles()
        self.name = self.root+'expected_output/rectangles/one.json'
        self._test_rectangles()

#     I think this test in erroneous, I can't set recips to whatever.
#     def test_rectangles_two(self):
#         self.integral.set_recips({"(1, 1, 1)": [[1, 1, 1]]})
#         self.integral.set_coeffs({'1': [1], '2': [1]})
#         self.integral.rectangles()
#         self.name = self.root+'expected_output/rectangles/two.json'
#         self._test_rectangles()

    def test_rectangles_three(self):
        self.integral.set_recips({"(0, 0, 0)": [[0, 0, 0]]})
        self.integral.set_coeffs({'1': [1], '2': [1]})
        self.integral.set_points(10)
        self.integral.rectangles()
        self.name = self.root+'expected_output/rectangles/three.json'
        self._test_rectangles()

    def test_rectangles_four(self):
        self.integral.set_recips({"(0, 0, 0)": [[0, 0, 0]]})
        self.integral.set_coeffs({'1': [1], '2': [1]})
        self.integral.set_bandnum(1)
        self.integral.rectangles()
        self.name = self.root+'expected_output/rectangles/four.json'
        self._test_rectangles()

    def test_gauss_one(self):
        self.integral.set_recips({"(0, 0, 0)": [[0, 0, 0]]})
        self.integral.set_coeffs({'1': [1], '2': [1]})
        self.integral.gauss()
        self.name = self.root+'expected_output/gauss/one.json'
        self._test_gauss()

#     I think this test is erroneous, I can't set recips to whatever.
#     def test_gauss_two(self):
#         self.integral.set_recips({"(1, 1, 1)": [[1, 1, 1]]})
#         self.integral.set_coeffs({'1': [1], '2': [1]})
#         self.integral.gauss()
#         self.name = self.root+'expected_output/gauss/two.json'
#         self._test_gauss()

    def test_gauss_three(self):
        self.integral.set_recips({"(0, 0, 0)": [[0, 0, 0]]})
        self.integral.set_coeffs({'1': [1], '2': [1]})
        self.integral.set_points(10)
        self.integral.gauss()
        self.name = self.root+'expected_output/gauss/three.json'
        self._test_gauss()

    def test_gauss_four(self):
        self.integral.set_recips({"(0, 0, 0)": [[0, 0, 0]]})
        self.integral.set_coeffs({'1': [1], '2': [1]})
        self.integral.set_bandnum(1)
        self.integral.gauss()
        self.name = self.root+'expected_output/gauss/four.json'
        self._test_gauss()


if __name__ == '__main__':
    unittest.main()
