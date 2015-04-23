#!/usr/bin/env python3

import unittest
import numpy as np

from os import mkdir, remove
from shutil import rmtree
from json import load
from itertools import product

from dftintegrate.fourier import vaspdata, readdata, fitdata


class TestFitDataSi2x2x2(unittest.TestCase):

    def setUp(self):
        self.root = 'tests/'
        vaspdata.VASPData(self.root+'test_input/Si2x2x2/')
        readdata.ReadData(self.root+'test_input/Si2x2x2/')
        self.fit = fitdata.FitData(self.root+'test_input/Si2x2x2/',
                                   getfit=False)
        with open(self.root+'expected_output/Si2x2x2/fit.json') as inf:
            self.answer = load(inf)

    def tearDown(self):
        folder = self.root+'test_input/Si2x2x2/'
        files = ['fit.json', 'data.json', 'kmax.dat',
                 'kpts_eigenvals.dat', 'symops_trans.dat']
        for f in files:
            remove(folder+f)

    def test_gen_recips_Si2x2x2(self):
        self.fit.gen_recips()
        self.fit.serialize()
        with open(self.root+'test_input/Si2x2x2/fit.json') as inf:
            check = load(inf)
        self.assertEqual(self.answer['reciprocals'],
                         check['reciprocals'])

    # def test_gen_series_Si2x2x2(self):
    #         self.assertEqual(self.answer['series'],
    #                          self.check['series'])

    # def test_solve_coeffs_Si2x2x2(self):
    #         self.assertEqual(self.answer['coefficients'],
    #                          self.check['coefficients'])


class TestFitDataGenRecips(unittest.TestCase):

    def setUp(self):
        self.root = 'tests/'
        mkdir(self.root+'temp_out/')
        self.fit = fitdata.FitData(self.root+'temp_out/',
                                   loaddata=False, getfit=False)

    def tearDown(self):
        rmtree(self.root+'temp_out/')

    def _test_gen_recips(self):
        self.fit.set_symops(self.symops)
        self.fit.set_kmax(self.kmax)
        self.fit.gen_recips()
        self.assertEqual(self.answer, self.fit.recips, self.msg+' fail')

    def test_gen_recips_identity(self):
        self.symops = [[[1, 0, 0], [0, 1, 0], [0, 0, 1]]]
        self.kmax = 15
        self.msg = 'identity'
        self.answer = {}
        for x in product(range(0, self.kmax+1), repeat=3):
            self.answer[str(x)] = [list(x)]
        self._test_gen_recips()

    def test_gen_recips_inversion(self):
        self.symops = [[[-1, 0, 0], [0, -1, 0], [0, 0, -1]]]
        self.kmax = 15
        self.msg = 'inversion'
        self.answer = {}
        for x in product(range(0, self.kmax+1), repeat=3):
            self.answer[str(x)] = [list(x)]
            nx = [int(i) for i in np.array(x)*-1]
            self.answer[str(x)].append(nx)
        del self.answer['(0, 0, 0)'][-1]
        self._test_gen_recips()

    def test_gen_recips_mixed(self):
        self.symops = [[[1, 1, 1], [1, 1, 1], [1, 1, 1]],
                       [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                       [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
        self.kmax = 1
        self.msg = 'mixed'
        self.answer = {'(0, 0, 0)': [[0, 0, 0]],
                       '(0, 0, 1)': [[0, 0, 1], [1, 1, 1], [3, 6, 9]],
                       '(0, 1, 0)': [[0, 1, 0], [2, 5, 8]],
                       '(1, 0, 0)': [[1, 0, 0], [1, 4, 7]],
                       '(0, 1, 1)': [[0, 1, 1], [2, 2, 2], [5, 11, 17]],
                       '(1, 0, 1)': [[1, 0, 1], [4, 10, 16]],
                       '(1, 1, 0)': [[1, 1, 0], [3, 9, 15]]}
        self._test_gen_recips()


class TestFitDataGenSeries(unittest.TestCase):

    def setUp(self):
        self.root = 'tests/'
        mkdir(self.root+'temp_out/')
        self.fit = fitdata.FitData(self.root+'temp_out/',
                                   loaddata=False, getfit=False)

    def tearDown(self):
        rmtree(self.root+'temp_out/')

    def _round_series(self):
        for i, row in enumerate(self.fit.series):
            for j, elem in enumerate(row):
                self.fit.series[i][j] = round(elem, 15)

    def _test_gen_series(self):
        self.fit.set_recips(self.recips)
        self.fit.set_kgrid(self.kgrid)
        self.fit.gen_series()
        self.fit.serialize()
        self._round_series()
        for i, row in enumerate(self.answer):
            self.assertCountEqual(self.answer[i], self.fit.series[i],
                                  self.msg + ' fail')

    def test_gen_series_one(self):
        self.recips = {'(0, 0, 0)': [[0, 0, 0]]}
        self.kgrid = [[1, 1, 1]]
        self.msg = 'Gen Series One'
        self.answer = [[1]]
        self._test_gen_series()

    def test_gen_series_two(self):
        self.recips = {'(0, 0, 0)': [[0, 0, 0]],
                       '(0, 0, 1)': [[0, 0, 1],
                                     [0, 1, 0],
                                     [1, 0, 0],
                                     [0, 0, -1],
                                     [0, -1, 0],
                                     [-1, 0, 0]]}
        self.kgrid = [[1, 1, 1]]
        self.msg = 'Gen Series Two'
        self.answer = [[1, 6]]
        self._test_gen_series()

    def test_gen_series_three(self):
        self.recips = {'(0, 0, 0)': [[0, 0, 0]],
                       '(0, 0, 1)': [[0, 0, 1],
                                     [0, 1, 0],
                                     [1, 0, 0],
                                     [0, 0, -1],
                                     [0, -1, 0],
                                     [-1, 0, 0]]}
        self.kgrid = [[1/2, 1/2, 1/2], [1, 1, 1]]
        self.msg = 'Gen Series Three'
        self.answer = [[1, -6], [1, 6]]
        self._test_gen_series()


class TestFitDataSolveCoeffs(unittest.TestCase):

    def setUp(self):
        self.root = 'tests/'
        mkdir(self.root+'temp_out/')
        self.fit = fitdata.FitData(self.root+'temp_out/',
                                   loaddata=False, getfit=False,
                                   bandnum=1)

    def tearDown(self):
        rmtree(self.root+'temp_out/')

    def _test_solve_coeffs(self):
        self.fit.set_series(self.series)
        self.fit.set_eigenvals(self.eigenvals)
        self.fit.solve_coeffs()
        self.fit.serialize()
        self.assertEqual(self.answer_coeffs, self.fit.coeffs)
        # self.assertEqual(self.answer_lstsq_err, self.fit.lstsq_err,
        #                  self.msg + ' fail')

    def test_solve_coeffs_one(self):
        self.series = [[1]]
        self.eigenvals = {'1': [1]}
        self.msg = 'Solve Coeffs One'
        self.answer_coeffs = {'1': np.array([1])}
        self.answer_lstsq_err = {'1': np.array([])}
        self._test_solve_coeffs()


if __name__ == '__main__':
    unittest.main()
