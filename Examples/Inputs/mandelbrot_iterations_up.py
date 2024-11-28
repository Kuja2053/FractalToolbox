import sys
import os
import csv



# Classes
class ClassParameters:
    def __init__(self):
        self.images_number = 0
        self.type_fractal = ""
        self.start_iterations = 0
        self.iterations_added = 0
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0
        self.R = 0
        self.G = 0
        self.B = 0
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
    parameters.images_number = 950
    parameters.type_fractal = "mandelbrot"
    parameters.start_iterations = 50
    parameters.iterations_added = 1
    parameters.xmin = -0.75
    parameters.xmax = -0.747
    parameters.ymin = 0.06
    parameters.ymax = 0.063
    parameters.R = 40
    parameters.G = 45
    parameters.B = 5
    parameters.opt_next_image = ""
    parameters.zoom_amount = 0.0
    parameters.centering_sigma = 2.0
    parameters.centering_up = 0
    parameters.centering_down = 0
    parameters.centering_left = 0
    parameters.centering_right = 0
    parameters.move_x = 0.0
    parameters.move_y = 0.0

    parameters.output_folder_pathname = "Outputs"
    parameters.output_filename = "mandelbrot_iterations_up.csv"

    # Prepare output folder
    if not os.path.exists(parameters.output_folder_pathname):
        os.makedirs(parameters.output_folder_pathname)

    # Prepare csv header and first data line
    data = []
    iterations = parameters.start_iterations
    data.append(["type_fractal", "max_iterations", "julia_a", "julia_b", "xmin", "xmax", "ymin", "ymax", "r", "g", "b",
                 "opt_next_image", "zoom_amount", "centering_sigma",
                 "centering_up", "centering_down", "centering_left", "centering_right",
                 "move_x", "move_y"])
    data.append([parameters.type_fractal,
                 str(iterations),
                 "",
                 "",
                 str(parameters.xmin),
                 str(parameters.xmax),
                 str(parameters.ymin),
                 str(parameters.ymax),
                 str(parameters.R),
                 str(parameters.G),
                 str(parameters.B),
                 parameters.opt_next_image,
                 str(parameters.zoom_amount),
                 str(parameters.centering_sigma),
                 str(parameters.centering_up),
                 str(parameters.centering_down),
                 str(parameters.centering_left),
                 str(parameters.centering_right),
                 str(parameters.move_x),
                 str(parameters.move_y)])

    # Adds data
    iterations += parameters.iterations_added
    for cnt in range(1, parameters.images_number):
        data.append([parameters.type_fractal,
                     str(iterations),
                     "",
                     "",
                     str(parameters.xmin),
                     str(parameters.xmax),
                     str(parameters.ymin),
                     str(parameters.ymax),
                     str(parameters.R),
                     str(parameters.G),
                     str(parameters.B),
                     parameters.opt_next_image,
                     str(parameters.zoom_amount),
                     str(parameters.centering_sigma),
                     str(parameters.centering_up),
                     str(parameters.centering_down),
                     str(parameters.centering_left),
                     str(parameters.centering_right),
                     str(parameters.move_x),
                     str(parameters.move_y)])
        iterations += parameters.iterations_added

    # Write output csv file
    with open(os.path.join(parameters.output_folder_pathname, parameters.output_filename),
              mode="w",
              newline="",
              encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(data)

    # End
    sys.exit(0)

