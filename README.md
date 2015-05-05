# dftintegrate

### Installation
Python3 support only. The way I do it that is easiest for me is to use a
virtual environment. If this is unfamiliar to you follow
[this link](http://docs.python-guide.org/en/latest/dev/virtualenvs/).
At the command line I type: 
`mkvirtualenv --python=/usr/local/bin/python3 nameOfEnvironment`.
This is assuming you followed the virtualenvwrapper part of the link above.
the path to the python3 executable might be different for you. You can find out
what yours is by typing `which python3` at the command line. Doing all of this
creates an environment where python3 is default, so if I type python it launches
python 3.4.x. Now that I have and am working in this environment I type
`pip install dftintegrate` and I'm done!

### basic Overview
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
