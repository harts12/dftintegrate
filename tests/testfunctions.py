"""
Some support functionality for tests. Inherited along with
unittest.TestCase.
"""

import json

from dftintegrate import customserializer as cs


class TestFunctions():

    def __init__():
        pass

    def readfile(self, case, check_or_ans, filename):
        with open(self.root+check_or_ans+'/test'+case+'/'+filename+'.dat',
                  'r') as inf:
            return inf.read()

    def readjson(self, case, check_or_ans, filename):
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
