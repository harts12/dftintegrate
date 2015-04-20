"""
Classes::
  FitData -- The FitData object fits a 3D function with a fourier
    series.
"""

import numpy as np
from json import dump, load
from scipy.linalg import lstsq
from itertools import product

from customserializer import tojson


class FitData(object):
    """Fit a periodic 3D function represented by a json file created by
     the ReadData object with fourier series, repersent the fit as an
     object.

    Fit a periodic 3D function represented by a json file created by
    the ReadData object with fourier series, repersent the fit as an
    object.

    Solve A x = b where A is a matrix and x and b are column vectors.

    Variables::
      data -- Data to fit represented in data.json.

      series -- Matrix representation of the series. "A" in the equation
        to solve.

      coeffs -- Fourier Coefficients in the Fourier series. "x" in the
        equation to solve. A dictionary, the key is the band number and
        the value is the list of coefficients for that band.

      recips -- Reciprocal lattice vectors in the Fourier sum.

      lstsq_err -- Total least squares error for the fit.

    Funtions::
      set_(kgrid, eigenvals, symops, kmax) -- Set (kgrid, eigenvals,
        symops, kmax) in case loaddata is false.

      _get_fit -- Call gen_recips, gen_series, solve_coeffs, and
        serialize.

      gen_recips -- Generate the reciprocal lattice vectors.

      gen_series -- Generate the sines and cosines in the series in
        matrix form.

      solve_coeffs -- Use scipy.linalg.lstsq to solve A x = b for x.

      serialize -- Serialize the fit to a json file.

    """

    def __init__(self, name_of_directory, loaddata=True, getfit=True,
                 bandnum=4):
        """
        Arguments::
          name_of_directory -- path to directory that contains the
            output from readdata.py

        Keyword Arguments::
          loaddata -- Boolean that says to automatically load data from
            data.json. This is useful if I want to test only one function.
            Default True.

          getfit -- Boolean that says to automatically run _get_fit.
            This is useful if I want to test only one function. Also
            determines auto serialize. Default True.

          bandnum -- Number of bands to fit. Default 4.
        """
        self.name = name_of_directory
        self.bandnum = bandnum
        if loaddata:
            with open(self.name+'data.json', mode='r',
                      encoding='utf-8') as inf:
                self.data = load(inf)
            self.kgrid = self.data['kgrid']
            self.eigenvals = self.data['eigenvals']
            self.symops = self.data['symops']
            self.kmax = int(self.data['kmax'])
        if getfit:
            self._get_fit()
        else:
            # Set to None so serialize still works if needed.
            self.coeffs = None
            self.recips = None
            self.series = None
            self.lstsq_err = None

    def set_kgrid(self, kgrid):
        self.kgrid = kgrid

    def set_eigenvals(self, eigenvals):
        self.eigenvals = eigenvals

    def set_symops(self, symops):
        self.symops = symops

    def set_kmax(self, kmax):
        self.kmax = kmax

    def set_recips(self, recips):
        self.recips = recips

    def _get_fit(self):
        self.gen_recips()
        self.gen_series()
        self.solve_coeffs()
        self.serialize()

    def gen_recips(self):
        """
        In the Fourier basis representation we sum over the reciprocal
        lattice vectors; this function generates those reciprocal
        lattice vectors. Start by using itertools.product to create
        triplets in range 0 to kmax. In order to sum over the entire
        Fermi sphere we operate on the triplets with the systems
        symmetry operators given in symops. kmax and symops are
        explained in more detail in readdata.py

        Varibles::
          allList -- A list of all vectors seen. Including results of
            product and their rotated versions after being operated on
            by symops.

          recips -- A dictionary with the key being a unique vector and
            the value being a list of the symmetric versions of that
            unique vector.
        """
        allList = set()
        recips = {}
        # Loop over the positive octant in k-space.
        for v in product(range(self.kmax+1), repeat=3):
            # Tuple so it's hashable.
            v = tuple(v)

            # Check if it has been seen before, if so skip, if not add.
            if v not in allList:
                allList.add(v)
                recips[str(v)] = [list(v)]

                # Loop over all symops
                for i, matrix in enumerate(self.symops):
                    # Operate on it with the symop.
                    vRot = tuple(np.dot(matrix, v))

                    # Check if it has been seen before, if so skip, if not add.
                    if vRot not in allList:
                        vRot = tuple([int(x) for x in vRot])
                        allList.add(vRot)
                        recips[str(v)].append(list(vRot))

        self.recips = recips

    def gen_series(self):
        """
        In the equation A x = b where A is a matrix and x and b are
        column vectors, this function generates A. We use the matrix
        equation to fit the 3D function represented by kgrid and
        eigenvals. x is the coefficients to the complex exponential and
        b is the values of the function. Each entry in A is like
        exp(i2piG.r).
        """
        series = []
        i = 1j  # imaginary number
        pi = np.pi
        for kpt in self.kgrid:
            row = []
            for k, v in self.recips.items():
                # The 2pi comes from the dot product of real and reciprocal
                # space lattice vectors. v is a list of reciprocal lattice
                # vectors that are symetric and therefore need to have the same
                # coefficient so they are summed together.
                gdotr = i*2*pi*np.dot(v, kpt)
                row.append(sum(np.exp(gdotr)))
            series.append(row)
        self.series = series

    def solve_coeffs(self):
        """
        Solve A x = b with scipy.linalg.lstsq. A is a matrix, see
        gen_series for more detail. x is the column vector we are
        solving for, it is the Fourier coefficients. b is a column
        vector, it is the energy values of the bands.
        """
        # A (series), b (eigenvals)
        coeffs = {}
        lstsq_err = {}
        A = self.series
        for num in range(1, self.bandnum+1):
            num = str(num)
            b = self.eigenvals[num]
            coeffs[num], lstsq_err[num] = np.array(lstsq(A, b)[:2])
        self.coeffs = coeffs
        self.lstsq_err = lstsq_err

    def serialize(self):
        fit_dict = {'coefficients': self.coeffs, 'reciprocals': self.recips,
                    'series': self.series, 'error': self.lstsq_err}
        with open(self.name+'fit.json', mode='w', encoding='utf-8') as outf:
            dump(fit_dict, outf, indent=2, default=tojson)
