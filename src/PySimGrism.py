#!/usr/bin/python3
import tkinter as tk
import astropy
from astroquery.simbad import Simbad
from astroquery.skyview import SkyView
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.transforms as mtransforms
import argparse

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
    parser = argparse.ArgumentParser("Grism simulator")
    parser.add_argument("target", help="Simbad target string")
    parser.add_argument("rotation", help="Rotation of image in degrees", type=float)
    args = parser.parse_args()

    query = SimbadQuery(args.target)
#    paths = SkyView.get_images(position="vega", survey=["UVOT UVM2 Intensity"])
    rotation = args.rotation
    position_str = str(query.ra.data[0]) + "," + str(query.dec.data[0])
    print(position_str)
#    paths = SkyView.get_images(position=position_str,survey=['DSS2 Blue','DSS2 IR','DSS2 Red'],pixels='2400,2400',coordinates='J2000',grid=True,gridlabels=True)
    paths = SkyView.get_images(position=position_str,survey=['UVOT UVM2 Intensity'],pixels='2400,2400',coordinates='J2000',grid=True,gridlabels=True)
    print(paths)
    fig, ax = plt.subplots()
    im = ax.imshow(paths[0][0].data)
    trans_data = mtransforms.Affine2D().rotate_deg(rotation) + ax.transData
    im.set_transform(trans_data)
    x1, x2, y1, y2 = im.get_extent()
    ax.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], "y--", transform=trans_data)

    print(paths[0][0].data)
    plt.show()
if __name__=="__main__":
    main()
