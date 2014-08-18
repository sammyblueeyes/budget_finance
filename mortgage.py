#!/usr/bin/python

import string
import sys
import math


# http://agonist.org/Learning-Center/mortgage/howdoyoucalculatemortgagepayments.html
def calc_replayments(PV, i, number_of_years, compounds_per_year, payments_per_year):

    #number_of_years = 20.0
    #compounds_per_year = 12.0
    #payments_per_year = 52.0
    #i = 0.0588
    #PV = 289643.74

    r = math.pow((1 + i/compounds_per_year), (compounds_per_year/payments_per_year)) - 1
    n = number_of_years * payments_per_year
    print "PMT = %f * %f / (1 - 1/((1 + %f)^%f)) " % (PV, r, r, n)
    PMT = PV * r / (1.0 - 1.0/math.pow((1 + r),n))
    print "PMT = $ %f" % PMT


if __name__ == '__main__':
    calc_replayments(289643.74, 0.05, 10.0, 365.0, 52.0)



