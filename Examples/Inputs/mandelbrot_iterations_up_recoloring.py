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
import numpy as np
import matplotlib.pyplot as plt



# Classes
class ClassParameters:
    def __init__(self):
        self.size_x = 0
        self.size_y = 0

        self.num_points = 0
        self.rest = 20
        self.peak = 60
        self.sequence = []

        self.input_output_folder_path = ""
        self.input_iterations_prefix = ""
        self.output_images_prefix = ""

        self.output_folder_pathname = ""
        self.output_filename = ""

        self.show_chart = False






# Globales
parameters = ClassParameters()











# Functions
def generate_rgb_from_sequence(num_points, sequence, rest, peak):

    num_segments = len(sequence)
    points_per_segment = num_points // num_segments
    x = np.linspace(0, num_points - 1, num_points)

    r = np.full(num_points, rest, dtype=float)
    g = np.full(num_points, rest, dtype=float)
    b = np.full(num_points, rest, dtype=float)

    for i, value in enumerate(sequence):
        start = i * points_per_segment
        end = start + points_per_segment
        if i == num_segments - 1:
            end = num_points

        r_active = (value & 4) > 0
        g_active = (value & 2) > 0
        b_active = (value & 1) > 0

        if r_active:
            r[start:end] = peak
        if g_active:
            g[start:end] = peak
        if b_active:
            b[start:end] = peak

    return x, r, g, b








# Main
if __name__ == '__main__':

    # Configuration
    parameters.size_x = 1920
    parameters.size_y = 1088

    parameters.input_output_folder_path = "Outputs/mandelbrot_iterations_up"
    parameters.input_iterations_prefix = "mandelbrot_iterations_"
    parameters.output_images_prefix = "mandelbrot_images_"

    parameters.output_folder_pathname = "Outputs"
    parameters.output_filename = "mandelbrot_iterations_up_recoloring.csv"

    parameters.show_chart = True

    # Prepare output folder
    if not os.path.exists(parameters.output_folder_pathname):
        os.makedirs(parameters.output_folder_pathname)

    # Check input/output folder
    if not os.path.exists("../" + parameters.input_output_folder_path):
        print("Error input/output folder does not exist.")
        sys.exit(1)

    # Prepare csv header
    data = []
    data.append(["input_iteration_pathfile", "output_image_pathfile", "size_x", "size_y", "R", "G", "B"])

    # List iterations files
    iterations = sorted([iter for iter in os.listdir("../" + parameters.input_output_folder_path) if (iter.endswith(".zip")) and (iter.startswith(parameters.input_iterations_prefix))])

    # Configure RGB variations parameters
    parameters.num_points = len(iterations)
    parameters.rest = 20
    parameters.peak = 60
    parameters.sequence = [0, 1, 2, 3, 4, 5, 6, 7]

    # Generates waves
    x, r, g, b = generate_rgb_from_sequence(parameters.num_points,
                                            parameters.sequence,
                                            parameters.rest,
                                            parameters.peak)

    # Adds data
    cnt_iterations = 0
    for filename in iterations:
        output_filename = filename.replace(parameters.input_iterations_prefix, parameters.output_images_prefix).replace(".bin.zip", ".png")
        data.append([os.path.join("../Examples/" + parameters.input_output_folder_path, filename),
                     os.path.join("../Examples/" + parameters.input_output_folder_path, output_filename),
                     str(parameters.size_x),
                     str(parameters.size_y),
                     str(int(r[cnt_iterations])),
                     str(int(g[cnt_iterations])),
                     str(int(b[cnt_iterations]))])
        cnt_iterations += 1

    # Write output csv file
    with open(os.path.join(parameters.output_folder_pathname, parameters.output_filename),
              mode="w",
              newline="",
              encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(data)

    # Show chart if needed
    if parameters.show_chart:
        plt.figure(figsize=(10, 6))
        plt.plot(x, r, label="R", color="red")
        plt.plot(x, g, label="G", color="green")
        plt.plot(x, b, label="B", color="blue")
        plt.title("RGB evolutions")
        plt.xlabel("Points")
        plt.ylabel("Values")
        plt.legend()
        plt.grid(True)
        plt.show()

    # End
    sys.exit(0)

