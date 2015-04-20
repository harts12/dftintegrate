# dftintegrate
### Basic Overview
Let's say you have a folder with VASP output and you want to get a Fourier
representation of the electron bands. You would simply type in the
command line, `dftintegrate -vasp -fit`. If the files it needs are not there
it will try to generate them.

One may also look at the code to see how to use it and import the modules to
write their own main.

### Note on kmax and KPOINTS
Because we are creating a fit out of data points we run up against the
Nyquist frequency, meaning we can only have so high of a frequency based on
how many data points. For this this reason the kmax variable exists. It is
pulled from the KPOINTS file. The problem is the VASP user has a few ways of
formatting their KPOINTS file. If the fourth line is the specification of the
size of kgrid ie 12 12 12 then everything will work fine. If not the user will
need to make their KPOINTS file look like that or they can make kmax.dat. If
12 12 12 was the grid than kmax = ceil(12/(2*sqrt(3))). dftintegrate automatically
uses files if they exist so creating it will work.
