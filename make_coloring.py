import os
import sys
import argparse
import csv
import zipfile
import struct
from multiprocessing import Pool, Manager, Lock
import psutil
import time
from PIL import Image
Image.MAX_IMAGE_PIXELS = None






# Classes
class ClassInput():
    def __init__(self):
        self.input_iteration_pathfile = ""
        self.output_image_pathfile = ""
        self.size_x = 0
        self.size_y = 0
        self.R = 0
        self.G = 0
        self.B = 0








# Globales
lock = Lock()









# Functions
def ReadInputsFile(inputs_filepath):
    try:
        with open(inputs_filepath, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=";")
            count = 0
            data = []
            for row in reader:
                if count == 0:
                    count += 1
                    continue

                if len(row) == 0:
                    continue

                local_inputs = ClassInput()

                local_inputs.input_iteration_pathfile = row[0]
                local_inputs.output_image_pathfile = row[1]

                local_inputs.size_x = int(row[2])
                local_inputs.size_y = int(row[3])

                local_inputs.R = int(row[4])
                local_inputs.G = int(row[5])
                local_inputs.B = int(row[6])

                data.append(local_inputs)

                count += 1

            if len(data) < 1:
                return []

            return data
    except:
        return []

def process_image(coloring_input, progress, cpu_limit):

    try:

        # check existence
        if not os.path.exists(coloring_input.input_iteration_pathfile) or not os.path.isfile(coloring_input.input_iteration_pathfile):
            print(f"Error, input file {coloring_input.input_iteration_pathfile} does not exist.")
            return

        # Load iteration grid from zip file
        iterations_grid = []
        for col in range(0, coloring_input.size_x):
            iterations_grid.append([])
            for line in range(0, coloring_input.size_y):
                iterations_grid[col].append(0)

        with zipfile.ZipFile(coloring_input.input_iteration_pathfile, 'r') as zip_file:
            bin_filename = os.path.basename(coloring_input.input_iteration_pathfile).replace(".zip", "")
            with zip_file.open(bin_filename) as file:
                content = file.read()

                if len(content) != (2 * coloring_input.size_x * coloring_input.size_y):
                    print(f"Error, input file {coloring_input.input_iteration_pathfile} has bad size.")
                    return

                for col in range(0, coloring_input.size_x):
                    for line in range(0, coloring_input.size_y):
                        index_bytes = (((col * coloring_input.size_y) + line) * 2)
                        number = struct.unpack('<H', content[index_bytes:index_bytes + 2])[0]
                        iterations_grid[col][line] = number

        # Create output image
        im = Image.new("RGB", (coloring_input.size_x, coloring_input.size_y), (255, 255, 255))
        pixels = im.load()

        for col in range(0, coloring_input.size_x):

            if cpu_limit < 100:
                while psutil.cpu_percent(interval=0.0001) > cpu_limit:
                    time.sleep(0.2)

            for line in range(0, coloring_input.size_y):

                nb_iterations = iterations_grid[col][line]
                pixels[col, line] = ((coloring_input.R * nb_iterations) % 256,
                                     (coloring_input.G * nb_iterations) % 256,
                                     (coloring_input.B * nb_iterations) % 256)

        im.save(coloring_input.output_image_pathfile)

        # Display progress
        with lock:
            progress["processed"] += 1
            current_percent_images = f"{int(progress["processed"] / progress['total'] * 100)}"
            if current_percent_images != progress["string_percent_images"]:
                print("", end="\r")
                print(f"{progress["processed"]}/{progress['total']}, {current_percent_images}%", end="")
                progress["string_percent_images"] = current_percent_images

    except Exception as e:
        print(f"Error processing image {coloring_input.output_image_pathfile}: {e}")

def validate_nb_cores_arg(value):
    try:
        cores_value = int(value)
        if cores_value <= 0:
            raise argparse.ArgumentTypeError("Number of cores must be equal to 1 or up.")
        return cores_value
    except ValueError:
        raise argparse.ArgumentTypeError("Number of cores must be equal to 1 or up.")

def validate_cpu_arg(value):
    try:
        cpu_value = int(value)
        if (cpu_value <= 0) or (cpu_value > 100):
            raise argparse.ArgumentTypeError("CPU limit must be between 1 and 100.")
        return cpu_value
    except ValueError:
        raise argparse.ArgumentTypeError("CPU limit must be between 1 and 100.")




# Main
if __name__ == '__main__':

    # Configure arguments detection
    parser = argparse.ArgumentParser(description="Script used to recolor images with iterations files.")

    parser.add_argument(
        "inputs_filepath",
        type=str,
        help="Path to a file containing instructions.",
    )

    parser.add_argument(
        "--cores",
        type=validate_nb_cores_arg,
        default=os.cpu_count(),
        help="Number of cores (1 or up)."
    )

    parser.add_argument(
        "--cpu",
        type=validate_cpu_arg,
        default=100,
        help="CPU limitation in percent."
    )

    # Parse arguments
    args = parser.parse_args()

    # Treat the arguments
    if not os.path.exists(args.inputs_filepath) or not os.path.isfile(args.inputs_filepath):
        print("Given file does not exist.")
        sys.exit(0)

    # Read inputs file
    inputs = ReadInputsFile(args.inputs_filepath)
    if len(inputs) == 0:
        print("Error with Inputs file")
        sys.exit(1)

    # Multiprocessing setup
    manager = Manager()
    progress = manager.dict({
        "processed": 0,
        "total": len(inputs),
        "string_percent_images": ""
    })

    # Start multiprocessing
    with Pool(processes=args.cores) as pool:
        pool.starmap(process_image, [(inp, progress, args.cpu) for inp in inputs])

    # End
    sys.exit(0)

