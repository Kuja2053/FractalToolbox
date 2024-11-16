import os
import shutil
import math
import sys
import time
from decimal import Decimal, getcontext
import xml.etree.ElementTree as ET
from collections import deque
from enum import Enum
from PIL import Image
Image.MAX_IMAGE_PIXELS = None




# Classes
class ClassDebug(Enum):
    NONE = 0
    IMAGES_DENSITY = 1
    WRITE_LOGS = 2
    ALL = 3

class ClassParameters:
    def __init__(self):
        self.a = Decimal(0)
        self.b = Decimal(0)
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
        self.adaptive_decimal_precision = 0
        self.output_folder_pathname = ""
        self.output_images_prefix = ""
        self.density_images_prefix = ""
        self.images_number = 0
        self.fps = 0

class ClassLogs:
    logs_filename = "logs.txt"

    def __init__(self):
        self.images_number = 0
        self.cnt_images = 0
        self.current_center_x = 0
        self.current_center_y = 0
        self.nearest_interesting_x = 0
        self.nearest_interesting_y = 0
        self.current_precision = 0
        self.current_xmin = 0.0
        self.current_xmax = 0.0
        self.current_ymin = 0.0
        self.current_ymax = 0.0

    def return_output_line(self, elapsed_time, remaining_time):
        elapsed_hours = int(elapsed_time // 3600)
        elapsed_minutes = int((elapsed_time % 3600) // 60)
        elapsed_seconds = int(elapsed_time % 60)

        remaining_hours = int(remaining_time // 3600)
        remaining_minutes = int((remaining_time % 3600) // 60)

        current_video_duration = (self.cnt_images / parameters.fps)
        current_video_minutes = int((current_video_duration % 3600) // 60)
        current_video_seconds = int(current_video_duration % 60)
        current_video_milliseconds = int((current_video_duration - int(current_video_duration)) * 1000)

        return (f"{elapsed_hours:02d}h{elapsed_minutes:02d}m{elapsed_seconds:02d}s;"
                f"{self.cnt_images}/{self.images_number};"
                f"{(self.cnt_images * 100 / parameters.images_number):.2f}%;"
                f"{remaining_hours:02d}h{remaining_minutes:02d}m;"
                f"{current_video_minutes:02d}m{current_video_seconds:02d}s{current_video_milliseconds:03d}ms;"
                f"center(x,y)=({self.current_center_x},{self.current_center_y});"
                f"nearest_interesting(x,y)=({self.nearest_interesting_x},{self.nearest_interesting_y});"
                f"precision={self.current_precision};"
                f"x(min,max)=({self.current_xmin},{self.current_xmax});"
                f"y(min,max)=({self.current_ymin},{self.current_ymax})")

    def write_logs(self, new_line):
        with open(self.logs_filename, "a") as file:
            file.write(new_line + "\n")

class ClassResume:
    resume_filename = "resume.xml"

    def __init__(self):
        self.cnt_images = 0
        self.xmin = Decimal(0.0)
        self.xmax = Decimal(0.0)
        self.ymin = Decimal(0.0)
        self.ymax = Decimal(0.0)
        self.elapsed_time = 0.0

    def resume_file_exist(self):
        return os.path.exists(self.resume_filename)

    def save_to_xml(self):
        root = ET.Element("Resume")

        ET.SubElement(root, "cnt_images").text = str(self.cnt_images)
        ET.SubElement(root, "xmin").text = str(self.xmin)
        ET.SubElement(root, "xmax").text = str(self.xmax)
        ET.SubElement(root, "ymin").text = str(self.ymin)
        ET.SubElement(root, "ymax").text = str(self.ymax)
        ET.SubElement(root, "elapsed_time").text = str(self.elapsed_time)

        tree = ET.ElementTree(root)

        temp_filename = f"{self.resume_filename}.tmp"
        with open(temp_filename, "wb") as tempfile:
            tree.write(tempfile)
        os.replace(temp_filename, self.resume_filename)     # atomic replacement to avoid file corruption

    def load_from_xml(self):
        tree = ET.parse(self.resume_filename)
        root = tree.getroot()

        self.cnt_images = int(root.find("cnt_images").text)
        self.xmin = Decimal(float(root.find("xmin").text))
        self.xmax = Decimal(float(root.find("xmax").text))
        self.ymin = Decimal(float(root.find("ymin").text))
        self.ymax = Decimal(float(root.find("ymax").text))
        self.elapsed_time = float(root.find("elapsed_time").text)

class ClassEMA:
    def __init__(self, smoothing_factor):
        self.smoothing_factor = smoothing_factor
        self.ema_value = None

    def add_value(self, value):
        if self.ema_value is None:
            self.ema_value = value
        else:
            self.ema_value = (((1 - self.smoothing_factor) * value) + (self.smoothing_factor * self.ema_value))
        return self.ema_value







# Globales
debug = ClassDebug.WRITE_LOGS

parameters = ClassParameters()
logs = ClassLogs()
resume = ClassResume()





# Functions
def check_density(grid, width, height, threshold):

    density_map = None
    if (debug == ClassDebug.IMAGES_DENSITY) or (debug == ClassDebug.ALL):
        density_map = Image.new("RGB", (width, height), (255, 255, 255))
        density_pixels = density_map.load()

    interesting_pixels = [[0] * height for _ in range(width)]

    for cnt_width in range(width):
        for cnt_height in range(height):
            pixel_interest = grid[cnt_width][cnt_height]

            if pixel_interest < threshold:
                if (debug == ClassDebug.IMAGES_DENSITY) or (debug == ClassDebug.ALL):
                    density_pixels[cnt_width, cnt_height] = (255, 255, 255)
            else:
                if (debug == ClassDebug.IMAGES_DENSITY) or (debug == ClassDebug.ALL):
                    density_pixels[cnt_width, cnt_height] = (255, 0, 0)
                interesting_pixels[cnt_width][cnt_height] = 1

    return density_map, interesting_pixels

def find_most_interesting_point(interesting_grid, width_grid, height_grid, center_x, center_y):

    queue = deque([(center_x, center_y)])
    visited = set()
    visited.add((center_x, center_y))

    while queue:
        x, y = queue.popleft()

        if interesting_grid[x][y] == 1:
            return x, y

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width_grid and 0 <= ny < height_grid and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))

    return None


def adjust_precision(xmin, xmax, significant_digits):

    difference = abs(Decimal(xmax) - Decimal(xmin))     # difference with current precision

    magnitude = difference.log10().to_integral_value()
    precision = significant_digits - int(magnitude)
    getcontext().prec = precision

    return precision








# Main
if __name__ == '__main__':

    # Configuration
    parameters.a = Decimal(0.39)
    parameters.b = Decimal(0.6)
    parameters.size_x = 1920
    parameters.size_y = 1088
    parameters.start_xmin = -1.25
    parameters.start_xmax = 1.25
    parameters.start_ymin = -1.25
    parameters.start_ymax = 1.25
    parameters.zoom_amount = 0.975
    parameters.max_iteration = 256
    parameters.R = 15
    parameters.G = 25
    parameters.B = 18
    parameters.adaptive_decimal_precision = 6
    parameters.output_folder_pathname = "output"
    parameters.output_images_prefix = "julia_zoom_"
    parameters.density_images_prefix = "julia_density_"
    parameters.images_number = 1248
    parameters.fps = 24

    logs.images_number = parameters.images_number

    # ask for resume if needed
    use_resume = 0
    if resume.resume_file_exist():
        response_resume = ""
        while (response_resume != "N") and (response_resume != "R"):
            response_resume = input("Enter R to resume, otherwise enter N : ").upper()
        if response_resume == "R":
            use_resume = 1

    # Prepare output folder
    if use_resume == 0:
        if os.path.exists(parameters.output_folder_pathname):
            shutil.rmtree(parameters.output_folder_pathname)
        os.makedirs(parameters.output_folder_pathname)

    # Fix precision
    getcontext().prec = 50      # set a high value to start

    # calcul start time
    start_time = time.time()

    # manage resume feature if needed, otherwise initialize variables with parameter
    if use_resume == 1:
        resume.load_from_xml()

        start_frame = resume.cnt_images
        xmin = Decimal(resume.xmin)
        xmax = Decimal(resume.xmax)
        ymin = Decimal(resume.ymin)
        ymax = Decimal(resume.ymax)
        resume_time = resume.elapsed_time
    else:
        start_frame = 0
        xmin = Decimal(parameters.start_xmin)
        xmax = Decimal(parameters.start_xmax)
        ymin = Decimal(parameters.start_ymin)
        ymax = Decimal(parameters.start_ymax)
        resume_time = 0

    center_x, center_y = parameters.size_x // 2, parameters.size_y // 2

    # start fill in logs
    logs.current_center_x = center_x
    logs.current_center_y = center_y

    # Initialize EMA
    EMA_duration_per_image = ClassEMA(0.80)

    for frame in range(start_frame, parameters.images_number):

        # Calcul start image for this frame
        start_time_frame = time.time()

        # Adapt decimal precision
        logs.current_precision = adjust_precision(xmin, xmax, parameters.adaptive_decimal_precision)

        # Initialize image
        im = Image.new("RGB", (parameters.size_x, parameters.size_y), (255, 255, 255))
        pixels = im.load()

        # Fill logs class
        logs.current_xmin = xmin
        logs.current_xmax = xmax
        logs.current_ymin = ymin
        logs.current_ymax = ymax

        # Make image
        iterations_grid = [[0] * parameters.size_y for _ in range(parameters.size_x)]
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

                iterations_grid[col][line] = i

                if i > parameters.max_iteration and (x ** 2 + y ** 2) <= 4:
                    pixels[col, line] = (0, 0, 0)
                else:
                    pixels[col, line] = ((parameters.R * i) % 256, (parameters.G * i) % 256, (parameters.B * i) % 256)

        # Calculate brightness average
        nb_pixels = (parameters.size_y * parameters.size_x)
        sum_iterations = 0
        for line in range(parameters.size_y):
            for col in range(parameters.size_x):
                sum_iterations += iterations_grid[col][line]
        iterations_average = sum_iterations / nb_pixels

        # Calculate variance
        sum_deviation_squared = 0
        for line in range(parameters.size_y):
            for col in range(parameters.size_x):
                sum_deviation_squared += (iterations_grid[col][line] - iterations_average) ** 2
        variance = sum_deviation_squared / nb_pixels

        # Calculate standard deviation
        standard_deviation = math.sqrt(variance)
        threshold_standard_deviation = (iterations_average + (2 * standard_deviation))

        # Calculate interesting map, generate density image for debug
        density_map, flags_density = check_density(iterations_grid, parameters.size_x, parameters.size_y, threshold_standard_deviation)
        if (debug == ClassDebug.IMAGES_DENSITY) or (debug == ClassDebug.ALL):
            density_map.save(f"{parameters.output_folder_pathname}/{parameters.density_images_prefix}{(frame+1):05d}.png")

        # Calculate the new center
        most_interesting_point = find_most_interesting_point(flags_density, parameters.size_x, parameters.size_y, center_x, center_y)
        if most_interesting_point == None:
            print("Terminated prematurely (nothing left to display)")
            sys.exit(1)

        logs.nearest_interesting_x, logs.nearest_interesting_y = most_interesting_point

        # Calculate center
        interesting_x, interesting_y = most_interesting_point
        fractal_x = (xmin + (interesting_x * ((xmax - xmin) / parameters.size_x)))
        fractal_y = (ymax - (interesting_y * ((ymax - ymin) / parameters.size_y)))
        width = xmax - xmin
        height = ymax - ymin
        xmin, xmax = (fractal_x - (width / 2)), (fractal_x + (width / 2))
        ymin, ymax = (fractal_y - (height / 2)), (fractal_y + (height / 2))

        # Calculate next zoom
        width = xmax - xmin
        height = ymax - ymin
        inverse_zoom = Decimal(1.0 - parameters.zoom_amount)
        xmin += ((width * inverse_zoom) / 2)
        xmax -= ((width * inverse_zoom) / 2)
        ymin += ((height * inverse_zoom) / 2)
        ymax -= ((height * inverse_zoom) / 2)

        # Save image with numbering
        im.save(f"{parameters.output_folder_pathname}/{parameters.output_images_prefix}{(frame+1):05d}.png")
        #im.show()

        # Get elapsed time for logs and resume
        elapsed_time = (time.time() - start_time)
        duration_per_frame = EMA_duration_per_image.add_value(time.time() - start_time_frame)
        remaining_time = (duration_per_frame * (parameters.images_number - (frame + 1)))

        # Print and write logs
        logs.cnt_images = (frame + 1)
        log_line = logs.return_output_line(elapsed_time + resume_time, remaining_time)
        print(log_line)
        if (debug == ClassDebug.ALL) or (debug == ClassDebug.WRITE_LOGS):
            logs.write_logs(log_line)

        # Write resume file
        resume.cnt_images = (frame + 1)
        resume.xmin = xmin
        resume.xmax = xmax
        resume.ymin = ymin
        resume.ymax = ymax
        resume.elapsed_time = (elapsed_time + resume_time)
        resume.save_to_xml()

    # End
    sys.exit(0)

