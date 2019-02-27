# Alexandre Erich Sebastien Georges 111079942
# Stony Brook University

from matplotlib import pyplot as plt
import numpy as np
import math
from scipy.interpolate import griddata
from matplotlib.ticker import FormatStrFormatter


class Soil:
    def __init__(self, id, no4, no10, no40, no200, LL, PL, organic):
        self.id = id
        self.no4 = no4
        self.no10 = no10
        self.no40 = no40
        self.no200 = no200
        self.LL = LL
        self.PL = PL
        self.PI = 0
        self.organic = organic
        self.silt = False
        self.clay = False
        self.Cu = 0
        self.Cc = 0
        self.symbol = ""
        self.name = ""
        self.x = np.array([4.75, 2, 0.425, 0.075])
        self.y = np.array([self.no4, self.no10, self.no40, self.no200])

    def PI_calculate(self):
        self.PI = self.LL - self.PL

    def coefficients(self):
        # Getting D30, D10 and D60
        # d60 = ((60 - self.no10) * (4.75 - 2)) / (self.no4 - self.no10) + 2
        # d30 = ((30 - self.no40) * (2 - 0.425)) / (self.no10 - self.no40) + 0.425
        # d10 = ((10 - self.no200) * (0.425 - 0.075)) / (self.no40 - self.no200) + 0.075
        temp10 = griddata(self.y, self.x, 10)
        temp30 = griddata(self.y, self.x, 30)
        temp60 = griddata(self.y, self.x, 60)
        if math.isnan(temp60):
            temp60 = ((60 - self.no10) * (4.75 - 2)) / (self.no4 - self.no10) + 2
        d10 = float(format(temp10, '.2f'))
        d30 = float(format(temp30, '.2f'))
        d60 = float(format(temp60, '.2f'))
        print("d10=", d10, " , d30=", d30, " , d60=", d60)
        self.Cu = d60 / d10
        self.Cc = math.pow(d30, 2) / (d10 * d60)

    def gravel_sand(self):
        fine = self.no200
        pass4 = ((100-self.no4) * 100) / (100-fine)
        # Gravels
        if pass4 >= 50:
            print("No. 4 retains ", pass4, " of coarse material and we have Gravel")
            if fine < 5:
                print("Fine < 5 (Clean Sand)")
                print("Cu =", self.Cu, ", Cc =", self.Cc)
                if self.Cu >= 4 and (1 < self.Cc < 3):
                    self.symbol = "GW"
                    self.name = "Well Graded Gravel"
                elif self.Cu < 4 or (self.Cc < 1 or self.Cc > 3):
                    self.symbol = "GP"
                    self.name = "Poorly Graded Gravel"
            elif fine > 12:
                print("Fine > 12 (Sand with Fines)")
                self.silt_clay()
                if self.silt is True:
                    self.symbol = "GM"
                    self.name = "Silty Gravel"
                elif self.clay is True:
                    self.symbol = "GC"
                    self.name = "Clayey Gravel"
                else:
                    self.symbol = "G " + self.symbol
                    self.name = "Silty-clay Gravel"
            else:
                # calculations with Cu and Cc
                self.coefficients()
                print("Cu =", self.Cu, ", Cc =", self.Cc)
                if self.Cu > 6 and (1 < self.Cc < 3):
                    self.silt_clay()
                    if self.clay is True:
                        self.symbol = "GW-GC"
                        self.name = "Well Graded Gravel with Clay"
                    elif self.silt is True:
                        self.symbol = "GW-GM"
                        self.name = "Well Graded Gravel with Silt"
                    else:
                        self.symbol = "GW " + self.symbol
                        self.name = "Well Graded Gravel with Silty-Clay"
                elif self.Cu < 6 or (self.Cc < 1 or self.Cc > 3):
                    self.silt_clay()
                    if self.clay is True:
                        self.symbol = "GP-GC"
                        self.name = "Poorly Graded Gravel with Clay"
                    elif self.silt is True:
                        self.symbol = "GP-GM"
                        self.name = "Poorly Graded Gravel with Silt"
                    else:
                        self.symbol = "GP " + self.symbol
                        self.name = "Poorly Graded Gravel with Silty-Clay"
        # Sand
        else:
            print("No. 4 retains ", pass4, " of coarse material and we have Sand")
            if fine < 5:
                print("Fine < 5 (Clean Sand)")
                self.coefficients()
                print("Cu =", self.Cu, ", Cc =", self.Cc)
                if self.Cu >= 6 and (1 < self.Cc < 3):
                    self.symbol = "SW"
                    self.name = "Well Graded Sand"
                elif self.Cu < 6 or (self.Cc < 1 or self.Cc > 3):
                    self.symbol = "SP"
                    self.name = "Poorly Graded Sand"
            elif fine > 12:
                print("Fine > 12 (Sand with Fines)")
                self.silt_clay()
                if self.silt is True:
                    self.symbol = "SM"
                    self.name = "Silty Sand"
                elif self.clay is True:
                    self.symbol = "SC"
                    self.name = "Clayey Sand"
                else:
                    self.symbol = "S " + self.symbol
                    self.name = "Silty-Clay Sand"
            else:
                self.coefficients()
                print("Cu =", self.Cu, ", Cc =", self.Cc)
                if self.Cu > 6 and (1 < self.Cc < 3):
                    self.silt_clay()
                    if self.clay is True:
                        self.symbol = "SW-SC"
                        self.name = "Well Graded sand with clay"
                    elif self.silt is True:
                        self.symbol = "SW-SM"
                        self.name = "Well Graded sand with silt"
                    else:
                        self.symbol = "SW " + self.symbol
                        self.name = "Well graded Sand with silty-clay"
                elif self.Cu < 6 or (self.Cc < 1 or self.Cc > 3):
                    self.silt_clay()
                    if self.clay is True:
                        self.symbol = "SP-SC"
                        self.name = "Poorly Graded sand with clay"
                    elif self.silt is True:
                        self.symbol = "SP-SM"
                        self.name = "Poorly Graded sand with silt"
                    else:
                        self.symbol = "SP " + self.symbol
                        self.name = "Poorly Graded Sand with Silty-Clay"

    def silt_clay(self):
        if self.LL < 50:
            print("LL < 50")
            if self.organic is True:
                self.symbol = "OL"
                self.name = "Organic"
            else:
                if self.PI > 7 and self.PI >= 0.73*(self.LL - 20):
                    self.symbol = "CL"
                    self.clay = True
                    self.name = "Lean Clay"
                elif self.PI < 4 and self.PI < 0.73*(self.LL - 20):
                    self.symbol = "ML"
                    self.silt = True
                    self.name = "Silt"

                else:
                    self.symbol = "CL-ML"
                    self.name = "Silty-Clay"
        else:
            print("LL > 50")
            if self.organic is True:
                self.symbol = "OH"
            else:
                if self.PI >= 0.73*(self.LL - 20):
                    self.symbol = "MH"
                    self.silt = True
                    self.name = "Elastic Silt"
                else:
                    self.symbol = "CH"
                    self.clay = True
                    self.name = "Fat clay"

    # Plot
    def plot(self):
        # xnew = np.linspace(x.min(), x.max(), 100)
        # f = interp1d(x, y, kind='quadratic')
        # y_smooth = f(xnew)
        title = "Percent Finer vs Diameter, Sample " + str(self.id + 1)
        fig, ax = plt.subplots()
        plt.semilogx(self.x, self.y, '-ok', color='black')
        ax.set(xlabel='Diameter (mm)', ylabel='Percent Finer (%)', title=title)
        ax.xaxis.set_major_formatter(FormatStrFormatter('%.3f'))
        plt.xticks(self.x)
        plt.yticks(np.arange(0, 100+0.1, 10))
        plt.gca().invert_xaxis()
        plt.grid()
        plt.text(0.1, 95, self.symbol + ", " + self.name, size=12,
                 va="baseline", ha="right", multialignment="left",
                 bbox=dict( fc="none"))
        plt.show()

    def classify(self):
        self.PI_calculate()
        # calculations with Cu and Cc
        if self.no200 >= 50:
            print("Fine-Grained Soil")
            self.silt_clay()
        else:
            print("Coarse-Grained Soil")
            self.gravel_sand()

