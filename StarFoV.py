'''
StarFoV
Copyright (C) 15/04/23 Riccardo La Grassa

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import os
import shutil
import numpy as np
import pandas as pd

filename= "/home/super/rlagrassa/stars_catalog/result_JOB02363_ST-151-8Plgn0MKrcKUkcxsdKnt.csv"



def howmanystars(x_min, x_max, y_min, y_max, stars):
    bucket_stars = stars[(stars['gaiaSource_ra'] >= x_min) & (stars['gaiaSource_ra'] <= x_max) & (stars['gaiaSource_decl']  >= y_min) & (stars['gaiaSource_decl'] <= y_max)]
    return bucket_stars

def readStarsCatalog():
    f = pd.read_csv(filename, header=0)
    return f
    # ra_error = f['gaiaSource_raError']
    # declination = f['gaiaSource_decl']
    # return ra_error, declination, f
    # if sortlat:
    #     craters.sort_values(by='LAT_CIRC_IMG', inplace=True)
    #     craters.reset_index(inplace=True, drop=True)
    #
    # craters["Latitude"] = craters["LAT_CIRC_IMG"]
    # craters["Longitude"] = np.where(craters["LON_CIRC_IMG"] <= 180, craters["LON_CIRC_IMG"],
    #                                 craters["LON_CIRC_IMG"] - 360)  # because we have 0-360 range!
    #
    # craters["Diameter"] = craters["DIAM_CIRC_IMG"]
    # craters = craters[(craters["Diameter"] >= min_crater_diameter) & (craters["Diameter"] <= max_crater_diameter)]
    # craters = craters[(craters["Longitude"] >= minLon) & (craters["Longitude"] <= maxLon) & (craters["Latitude"] >= minLat) & (craters["Latitude"] <= maxLat)]

    #print("Robbins craters loaded: ", len(craters))
    #return craters

path_fovStars_LonLat = "/home/super/rlagrassa/stars_catalog/searchStars_results_V1"

try:
    if os.path.exists(path_fovStars_LonLat):
        shutil.rmtree(path_fovStars_LonLat)
        os.makedirs(path_fovStars_LonLat)
    else:
        os.makedirs(path_fovStars_LonLat)
except:
    print("Error IO Craters folder creation.. Exit")
    exit()


f = readStarsCatalog()

ra = np.arange(0, 360, .01)
decl = np.arange(-90, 90, .01)
# Create the meshgrid
ra_mesh, decl_mesh = np.meshgrid(ra, decl)
print("Mesh done...")
X_fov_dimension = 538 #5.38 -> multiply by 100 because the meshgrid is created using 0.01 as step
Y_fov_dimension = 231 #2.31

for i in range(0, len(ra) - Y_fov_dimension + 1, 40):
    for j in range(0, len(decl) - X_fov_dimension + 1, 40):
        x_window = ra_mesh[i:i+X_fov_dimension, j:j+X_fov_dimension]
        y_window = decl_mesh[i:i+Y_fov_dimension, j:j+Y_fov_dimension]
        x_min, x_max, y_min, y_max = np.min(x_window), np.max(x_window), np.min(y_window), np.max(y_window)
        real_fov_size = (x_max - x_min, y_max - y_min)
        bucket_stars = howmanystars(x_min, x_max, y_min, y_max, f)
        if bucket_stars.shape[0] >=30:
            bucket_stars.to_csv(path_fovStars_LonLat + '/' + str(x_min) + ',' + str(x_max) + ',' + str(y_min) + ',' + str(y_max)+'_'+str(bucket_stars.shape[0]))