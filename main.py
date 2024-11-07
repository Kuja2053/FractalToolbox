import os
import shutil
import math
import sys
from collections import deque
import imageio.v2
from enum import Enum
from PIL import Image
Image.MAX_IMAGE_PIXELS = None



# Classes
class ClassCommand(Enum):
    MAKE_ALL = 0
    MAKE_IMAGES = 1
    MAKE_VIDEO = 2

class ClassDebug(Enum):
    NONE = 0
    IMAGES_DENSITY = 1
    WRITE_LOGS = 2
    ALL = 3

class ClassParameters:
    def __init__(self):
        self.a = 0
        self.b = 0
        self.size_x = 0
        self.size_y = 0
        self.start_xmin = 0
        self.start_xmax = 0
        self.start_ymin = 0
        self.start_ymax = 0
        self.zoom_amount = 0
        self.max_iteration = 0
        self.R = 0
        self.G = 0
        self.B = 0
        self.output_folder_pathname = ""
        self.images_number = 0
        self.fps = 0

class ClassLogs:
    logs_filename = "logs.txt"

    def __init__(self):
        self.images_number = 0
        self.cnt_images = 0
        self.current_center_x = 0
        self.current_center_y = 0
        self.nearest_bright_x = 0
        self.nearest_bright_y = 0
        self.current_xmin = 0.0
        self.current_xmax = 0.0
        self.current_ymin = 0.0
        self.current_ymax = 0.0

    def return_output_line(self):
        return (f"{self.cnt_images}/{self.images_number};"
                f"{(cnt_images * 100 / parameters.images_number):.2f}%;"
                f"center(x,y)=({self.current_center_x},{self.current_center_y});"
                f"nearest_bright(x,y)=({self.nearest_bright_x},{self.nearest_bright_y});"
                f"x(min,max)=({self.current_xmin},{self.current_xmax});"
                f"y(min,max)=({self.current_ymin},{self.current_ymax})")

    def write_logs(self, new_line):
        with open(self.logs_filename, "a") as file:
            file.write(new_line + "\n")





# Globales
command = ClassCommand.MAKE_ALL
debug = ClassDebug.WRITE_LOGS

parameters = ClassParameters()
logs = ClassLogs()





# Functions
def luminosity(r, g, b):
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def check_density(image, threshold):
    pixels_from_images = image.load()

    density_map = None
    if (debug == ClassDebug.IMAGES_DENSITY) or (debug == ClassDebug.ALL):
        density_map = Image.new("RGB", image.size, (255, 255, 255))
        density_pixels = density_map.load()

    brightness_flags = [[0] * image.height for _ in range(image.width)]

    for cnt_width in range(image.width):
        for cnt_height in range(image.height):
            value_r, value_g, value_b = pixels_from_images[cnt_width, cnt_height]

            pixel_luminosity = luminosity(value_r, value_g, value_b)

            if pixel_luminosity < threshold:
                if (debug == ClassDebug.IMAGES_DENSITY) or (debug == ClassDebug.ALL):
                    density_pixels[cnt_width, cnt_height] = (255, 255, 255)
            else:
                if (debug == ClassDebug.IMAGES_DENSITY) or (debug == ClassDebug.ALL):
                    density_pixels[cnt_width, cnt_height] = (255, 0, 0)
                brightness_flags[cnt_width][cnt_height] = 1

    return density_map, brightness_flags

def find_nearest_bright_point(brightness_flags_array, width_array, height_array, center_x, center_y):

    queue = deque([(center_x, center_y)])
    visited = set()
    visited.add((center_x, center_y))

    while queue:
        x, y = queue.popleft()

        if brightness_flags_array[x][y] == 1:
            return x, y

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width_array and 0 <= ny < height_array and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))

    return None





# Main
if __name__ == '__main__':

    # Configuration
    parameters.a = 0.39
    parameters.b = 0.6
    parameters.size_x = 1920
    parameters.size_y = 1088
    parameters.start_xmin = -1.25
    parameters.start_xmax = 1.25
    parameters.start_ymin = -1.25
    parameters.start_ymax = 1.25
    parameters.zoom_amount = 0.99
    parameters.max_iteration = 256
    parameters.R = 3
    parameters.G = 2
    parameters.B = 1
    parameters.output_folder_pathname = "output"
    parameters.images_number = 4320
    parameters.fps = 24
    logs.images_number = parameters.images_number

    # Prepare output folder
    if command != ClassCommand.MAKE_VIDEO:
        if os.path.exists(parameters.output_folder_pathname):
            shutil.rmtree(parameters.output_folder_pathname)
        os.makedirs(parameters.output_folder_pathname)

    # Loop for images generation
    if (command == ClassCommand.MAKE_IMAGES) or (command == ClassCommand.MAKE_ALL):

        cnt_images = 0

        xmin = parameters.start_xmin
        xmax = parameters.start_xmax
        ymin = parameters.start_ymin
        ymax = parameters.start_ymax

        center_x, center_y = parameters.size_x // 2, parameters.size_y // 2
        logs.current_center_x = center_x
        logs.current_center_y = center_y

        for frame in range(parameters.images_number):

            # Initialize image
            im = Image.new("RGB", (parameters.size_x, parameters.size_y), (255, 255, 255))
            pixels = im.load()

            # Fill logs class if needed
            logs.cnt_images = (cnt_images + 1)
            logs.current_xmin = xmin
            logs.current_xmax = xmax
            logs.current_ymin = ymin
            logs.current_ymax = ymax

            # Make image
            for line in range(parameters.size_y):
                for col in range(parameters.size_x):

                    i = 1
                    x = xmin + col * (xmax - xmin) / parameters.size_x
                    y = ymax - line * (ymax - ymin) / parameters.size_y

                    while i <= parameters.max_iteration and (x ** 2 + y ** 2) <= 4:
                        stock = x
                        x = x ** 2 - y ** 2 + parameters.a
                        y = 2 * stock * y + parameters.b
                        i += 1

                    if i > parameters.max_iteration and (x ** 2 + y ** 2) <= 4:
                        pixels[col, line] = (0, 0, 0)
                    else:
                        pixels[col, line] = ((parameters.R * i) % 256, (parameters.G * i) % 256, (parameters.B * i) % 256)

            # Calculate brightness average
            nb_pixels = (parameters.size_y * parameters.size_x)
            sum_brightness = 0
            for line in range(parameters.size_y):
                for col in range(parameters.size_x):
                    sum_brightness += luminosity(pixels[col, line][0], pixels[col, line][1], pixels[col, line][2])
            brightness_average = sum_brightness / nb_pixels

            # Calculate variance
            sum_deviation_squared = 0
            for line in range(parameters.size_y):
                for col in range(parameters.size_x):
                    sum_deviation_squared += (luminosity(pixels[col, line][0], pixels[col, line][1], pixels[col, line][2]) - brightness_average) ** 2
            variance = sum_deviation_squared / nb_pixels

            # Calculate standard deviation
            standard_deviation = math.sqrt(variance)
            threshold_standard_deviation = (brightness_average + (2 * standard_deviation))

            # Calculate brightness map, generate density image for debug
            density_map, flags_density = check_density(im, threshold_standard_deviation)
            if (debug == ClassDebug.IMAGES_DENSITY) or (debug == ClassDebug.ALL):
                density_map.save(f"{parameters.output_folder_pathname}/julia_density_{frame:05d}.png")

            # Calculate the new center
            bright_point = find_nearest_bright_point(flags_density, parameters.size_x, parameters.size_y, center_x, center_y)
            if bright_point == None:
                print("Terminated prematurely (nothing left to display)")
                sys.exit(1)

            logs.nearest_bright_x, logs.nearest_bright_y = bright_point

            # Print and write logs
            log_line = logs.return_output_line()
            print(log_line)
            if (debug == ClassDebug.ALL) or (debug == ClassDebug.WRITE_LOGS):
                logs.write_logs(log_line)

            # Calculate center
            bright_x, bright_y = bright_point
            fractal_x = (xmin + (bright_x * ((xmax - xmin) / parameters.size_x)))
            fractal_y = (ymax - (bright_y * ((ymax - ymin) / parameters.size_y)))
            width = xmax - xmin
            height = ymax - ymin
            xmin, xmax = (fractal_x - (width / 2)), (fractal_x + (width / 2))
            ymin, ymax = (fractal_y - (height / 2)), (fractal_y + (height / 2))

            # Calculate next zoom
            width = xmax - xmin
            height = ymax - ymin
            xmin += ((width * (1.0 - parameters.zoom_amount)) / 2)
            xmax -= ((width * (1.0 - parameters.zoom_amount)) / 2)
            ymin += ((height * (1.0 - parameters.zoom_amount)) / 2)
            ymax -= ((height * (1.0 - parameters.zoom_amount)) / 2)

            # Save image with numbering
            im.save(f"{parameters.output_folder_pathname}/julia_zoom_{frame:05d}.png")
            #im.show()

            # Increment image counter
            cnt_images += 1

    # Make video
    if (command == ClassCommand.MAKE_VIDEO) or (command == ClassCommand.MAKE_ALL):

        # Sort images for output video
        images = sorted([img for img in os.listdir(parameters.output_folder_pathname) if (img.endswith(".png")) and (img.startswith("julia_zoom_"))])

        # Create output video
        with imageio.get_writer(f"{parameters.output_folder_pathname}/julia.mp4", fps=parameters.fps) as writer:
            for filename in images:
                image_path = os.path.join(parameters.output_folder_pathname, filename)
                image = imageio.v2.imread(image_path)
                writer.append_data(image)

    # End
    sys.exit(0)