# Fractal Toolbox is a series of python scripts for generating images
# and videos based on Julia and Mandelbrot sets.
# Copyright (C) 2024  Vivien ELIE
#
# This file is part of Fractal Toolbox.
#
# Fractal Toolbox is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# Fractal Toolbox is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Fractal Toolbox.
# If not, see <https://www.gnu.org/licenses/>.


import sys
import os
import csv
import random



# Classes
class ClassParameters:
    def __init__(self):
        self.images_number = 0
        self.type_fractal = ""
        self.max_iterations = 0
        self.julia_min_a = 0
        self.julia_max_a = 0
        self.julia_min_b = 0
        self.julia_max_b = 0
        self.min_xmin = 0
        self.max_xmin = 0
        self.min_xmax = 0
        self.max_xmax = 0
        self.min_ymin = 0
        self.max_ymin = 0
        self.min_ymax = 0
        self.max_ymax = 0
        self.min_R = 0
        self.max_R = 0
        self.min_G = 0
        self.max_G = 0
        self.min_B = 0
        self.max_B = 0
        self.opt_next_image = ""
        self.zoom_amount = 0
        self.centering_sigma = 0
        self.centering_up = 0
        self.centering_down = 0
        self.centering_left = 0
        self.centering_right = 0
        self.move_x = 0.0
        self.move_y = 0.0

        self.output_folder_pathname = ""
        self.output_filename = ""






# Globales
parameters = ClassParameters()





# Main
if __name__ == '__main__':

    # Configuration
    parameters.images_number = 2000
    parameters.type_fractal = "julia"
    parameters.max_iterations = 100
    parameters.julia_min_a = -1
    parameters.julia_max_a = 1
    parameters.julia_min_b = -1
    parameters.julia_max_b = 1
    parameters.min_xmin = -1.5
    parameters.max_xmin = -1.5
    parameters.min_xmax = 1.5
    parameters.max_xmax = 1.5
    parameters.min_ymin = -1.5
    parameters.max_ymin = -1.5
    parameters.min_ymax = 1.5
    parameters.max_ymax = 1.5
    parameters.min_R = 1
    parameters.max_R = 100
    parameters.min_G = 1
    parameters.max_G = 100
    parameters.min_B = 1
    parameters.max_B = 100
    parameters.opt_next_image = ""
    parameters.zoom_amount = 0.0
    parameters.centering_sigma = 0.0
    parameters.centering_up = 0
    parameters.centering_down = 0
    parameters.centering_left = 0
    parameters.centering_right = 0
    parameters.move_x = 0.0
    parameters.move_y = 0.0

    parameters.output_folder_pathname = "Outputs"
    parameters.output_filename = "julia_random.csv"

    # Prepare output folder
    if not os.path.exists(parameters.output_folder_pathname):
        os.makedirs(parameters.output_folder_pathname)

    # Prepare csv header
    data = []
    data.append(["type_fractal", "max_iterations", "julia_a", "julia_b", "xmin", "xmax", "ymin", "ymax", "r", "g", "b",
                 "opt_next_image", "zoom_amount", "centering_sigma",
                 "centering_up", "centering_down", "centering_left", "centering_right",
                 "move_x", "move_y"])

    # Adds data
    for cnt in range(0, parameters.images_number):

        random_a = random.uniform(parameters.julia_min_a, parameters.julia_max_a)
        random_b = random.uniform(parameters.julia_min_b, parameters.julia_max_b)

        while(True):
            random_xmin = random.uniform(parameters.min_xmin, parameters.max_xmin)
            random_xmax = random.uniform(parameters.min_xmax, parameters.max_xmax)
            if random_xmin < random_xmax:
                break

        while (True):
            random_ymin = random.uniform(parameters.min_ymin, parameters.max_ymin)
            random_ymax = random.uniform(parameters.min_ymax, parameters.max_ymax)
            if random_ymin < random_ymax:
                break

        random_R = int(random.uniform(parameters.min_R, parameters.max_R))
        random_G = int(random.uniform(parameters.min_G, parameters.max_G))
        random_B = int(random.uniform(parameters.min_B, parameters.max_B))

        data.append([parameters.type_fractal,
                     str(parameters.max_iterations),
                     str(random_a),
                     str(random_b),
                     str(random_xmin),
                     str(random_xmax),
                     str(random_ymin),
                     str(random_ymax),
                     str(random_R),
                     str(random_G),
                     str(random_B),
                     parameters.opt_next_image,
                     str(parameters.zoom_amount),
                     str(parameters.centering_sigma),
                     str(parameters.centering_up),
                     str(parameters.centering_down),
                     str(parameters.centering_left),
                     str(parameters.centering_right),
                     str(parameters.move_x),
                     str(parameters.move_y)])

    # Write output csv file
    with open(os.path.join(parameters.output_folder_pathname, parameters.output_filename),
              mode="w",
              newline="",
              encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(data)

    # End
    sys.exit(0)

