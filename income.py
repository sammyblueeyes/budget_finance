#!/usr/bin/python
#
# Script to try to understand the Australian Income tax system.
#

import string
import sys
import math
import subprocess


class Tax:
    def __init__(self, yearly_gross_income, offset = 0.0):
        self.yearly_gross_income = yearly_gross_income
        self.effective_yearly_gross_income = yearly_gross_income - offset
        self.payable = True

        # From http://www.ato.gov.au/Rates/Individual-income-tax-rates/
        if (self.effective_yearly_gross_income <= 18200):
            self.payable = False
            self.base_tax = 0.0
            self.tax_free_threshold = 0.0
            self.rate = 0.0
        elif (self.effective_yearly_gross_income <= 37000):
            self.base_tax = 0.0
            self.tax_free_threshold = 18200.0
            self.rate = 0.19
        elif (self.effective_yearly_gross_income <= 80000):
            self.base_tax = 3572.0
            self.tax_free_threshold = 37000.0
            self.rate = 0.325
        elif (self.effective_yearly_gross_income <= 180000):
            self.base_tax = 17547.0
            self.tax_free_threshold = 80000.0
            self.rate = 0.37
        else:
            self.base_tax = 54547.0
            self.tax_free_threshold = 180000.0
            self.rate = 0.45

    def tax_payable(self):
        if not self.payable:
            return 0.0
        return (self.base_tax + ((self.effective_yearly_gross_income - self.tax_free_threshold) * self.rate))
        
    def net_income(self):
        return self.yearly_gross_income - self.tax_payable()


# Graph the net income for tax with a range of offset amounts, 
# over a range of Gross income values.
def compare_net_income_with_offset():
    proc = subprocess.Popen(['gnuplot','-p'], 
                            shell=False,
                            stdin=subprocess.PIPE)
    commands = []
    data = []
    for j in range (80000, 120000, 5000):
        income = j
        commands.append('"-" using 1:3 with lines title "Net income with offset (base $%d)"' % income)

        for i in range(0,10000, 100):
            tax1 = Tax(float(income)) 
            tax2 = Tax(float(income), float(i))
            #proc.stdin.write("%d %f %f\n" % (i, tax1.net_income(), tax2.net_income()))
            data.append("%d %f %f" % (i, tax1.net_income(), tax2.net_income()))
        data.append("e\n")
    proc.stdin.write("plot " + ",".join(commands) + "\n")
    proc.stdin.write("\n".join(data))


# Graph the net income for basic tax over a range of Gross income
# values.
def compare_net_income(low, high):
    proc = subprocess.Popen(['gnuplot','-p'], 
                            shell=False,
                            stdin=subprocess.PIPE)
    command = 'plot "-" using 1:2 with lines title "Net income"\n'
    data = []
    for i in range (low, high):

        tax1 = Tax(float(i))
        data.append("%d %f" % (i, tax1.net_income()))
    data.append("e\n")

    proc.stdin.write(command)
    proc.stdin.write("\n".join(data))


if __name__ == '__main__':
    compare_net_income(5000, 250000)
    compare_net_income_with_offset()



