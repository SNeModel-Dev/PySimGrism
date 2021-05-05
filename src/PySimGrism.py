#!/usr/bin/python3
import astropy
from astropy import units as u
from astroquery.simbad import Simbad
from astroquery.skyview import SkyView
from astroquery.vizier import Vizier
from astropy.io import fits
from astropy.coordinates import Angle
from astropy.coordinates import SkyCoord
from astropy.wcs import WCS
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.transforms as mtransforms
import montage_wrapper as montage
import argparse
import pandas as pd
import matplotlib.patches as patches

class SimbadQuery:
    def __init__(self, target_name):
        self.target = target_name
        self.result_table = Simbad.query_object(target_name)
        print(self.result_table)
        self.ra = self.result_table["RA"]
        self.dec = self.result_table["DEC"]
        print("ra: " + str(type(self.ra)))
        print("dec: " + str(type(self.dec)))

def queryVizier(target, cat):
    result = Vizier.query_region(target, radius=Angle(0.10, "deg"), catalog='GALEX')
    #print(result)
    good_objects = []
    for table_name in result.keys():
        #########print(result[table_name].keys())
        data = result[table_name]
        print("Asymtotic FUV Magnitude:")
        print(data['asyFUV'])
        print("Asymtototic NUV Magnitude:")
        print(data['asyNUV'])
    #    print("Ra:")
    #    print(data["RAJ2000"])
        pd_data = data.to_pandas()
    #    print(pd_data)
        print("Pandas print")
        print(pd_data['RAJ2000'][0])
        print(pd_data['DEJ2000'][0])
        coord = SkyCoord(pd_data['RAJ2000'][0] + " " + pd_data['DEJ2000'][0], unit=(u.hourangle, u.deg), frame="icrs", equinox="j2000")
        good_objects.append(coord)
    return good_objects
def main():
    parser = argparse.ArgumentParser("Grism simulator")
    parser.add_argument("target", help="Simbad target string")
    parser.add_argument("rotation", help="Rotation of image in degrees", type=float)
    args = parser.parse_args()

    query = SimbadQuery(args.target)
    targets = queryVizier(args.target, 0.1)

#    paths = SkyView.get_images(position="vega", survey=["UVOT UVM2 Intensity"])
    rotation = args.rotation
    position_str = str(query.ra.data[0]) + "," + str(query.dec.data[0])
    position_str2 = str(query.ra.data[0]) + " " + str(query.dec.data[0])
    coor = SkyCoord(position_str2, unit=(u.hourangle, u.deg), frame="icrs", equinox="j2000")

    print(position_str)
    #paths = SkyView.get_images(position=position_str,survey=['DSS2 Blue','DSS2 IR','DSS2 Red'],pixels='2400,2400',coordinates='J2000',grid=True,gridlabels=True)
    paths = SkyView.get_images(position=position_str,survey=['GALEX Near UV', 'GALEX Far UV'],pixels='2400,2400',coordinates='J2000',grid=True,gridlabels=True)
    print(paths)
    fig, ax = plt.subplots()
    targets.append(coor)
    for path in paths:
        w = WCS(path[0].header)
        for targ in targets:
            x,y = w.world_to_pixel(targ)
            print("X: " + str(x) + " Y: " + str(y))
            rect = patches.Rectangle((x-5, y-5), 11, 11, linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
   #     montage.mRotate(path[0], "test.fits", rotation_angle="20.0")

    #print(paths[0][0])
    im = ax.imshow(paths[0][0].data)
    trans_data = mtransforms.Affine2D().rotate_deg(rotation) + ax.transData
    im.set_transform(trans_data)
    x1, x2, y1, y2 = im.get_extent()
    ax.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], "y--", transform=trans_data)

    print(paths[0][0].data)
    plt.show()
if __name__=="__main__":
    main()
