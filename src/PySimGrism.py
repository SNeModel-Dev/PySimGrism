#!/usr/bin/python3
import tkinter as tk
import astropy
from astroquery.simbad import Simbad
from astroquery.skyview import SkyView
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

class SimbadQuery:
    def __init__(self, target_name):
        self.target = target_name
        self.result_table = Simbad.query_object(target_name)
        print(self.result_table)
        self.ra = self.result_table["RA"]
        self.dec = self.result_table["DEC"]
        print("ra: " + str(type(self.ra)))
        print("dec: " + str(type(self.dec)))


def main():
    query = SimbadQuery("vega")
#    paths = SkyView.get_images(position="vega", survey=["UVOT UVM2 Intensity"])
    paths = SkyView.get_images(position='22:57:00,62:38:00',survey=['DSS2 Blue','DSS2 IR','DSS2 Red'],pixels='2400,2400',coordinates='J2000',grid=True,gridlabels=True)
    print(paths)
    plt.imshow(paths[0][0].data)
    print(paths[0][0].data)
    plt.show()
if __name__=="__main__":
    main()
