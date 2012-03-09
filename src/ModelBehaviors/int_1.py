
"""
Created on Feb 27, 2012

@author: trobinso

Plugin IModelBehavior that implements the int operator.

"""

from fakeDataGenerator.model import IModelBehavior

class IntCoerce(IModelBehavior):
    arity=(1,1)
    isNoise = False
    def calculate(self, value):
        return int(value)
    def generate_name(self, name):
        return 'int(%s)' % name

