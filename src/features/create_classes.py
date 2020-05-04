"""
practice creating vehicle class
can these be passed between modules?
"""
import os
os.chdir('/home/joemcormier/github/pycrash/src/features')

class Vehicle:
    """docstring for Vehicle."""

    def __init__(self, year, make, model, vin, weight):
        self.year = year
        self.make = make
        self.model = model
        self.vin = vin
        self.weight = weight

veh1 = Vehicle(2016, 'Subaru', 'WRX STi', '000001', 3500)

veh1.year
veh1.weight

from import_practice import Vehicle
