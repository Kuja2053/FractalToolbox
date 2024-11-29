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


import os
import sys
import imageio.v2
import argparse
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup





# Classes
class ClassParameters:
    def __init__(self):
        self.description = ""
        self.input_folder_path = ""
        self.input_images_prefix = ""
        self.fps = 0
        self.reverse_video = 0
        self.output_pathfile = ""

    def CreateNewProjectFile(self, project_filepath):
        root = ET.Element("Project_video")

        ET.SubElement(root, "description").text = self.description
        ET.SubElement(root, "input_folder_path").text = self.input_folder_path
        ET.SubElement(root, "input_images_prefix").text = self.input_images_prefix
        ET.SubElement(root, "fps").text = str(self.fps)
        ET.SubElement(root, "reverse_video").text = str(self.reverse_video)
        ET.SubElement(root, "output_pathfile").text = self.output_pathfile

        tree = ET.ElementTree(root)

        temp_filename = f"{project_filepath}.tmp"
        with open(temp_filename, "wb") as tempfile:
            tree.write(tempfile)

        with open(temp_filename, "r", encoding="utf-8") as file:
            xml_content = file.read()

        soup = BeautifulSoup(xml_content, "lxml-xml")
        prettified_xml = soup.prettify()

        with open(temp_filename, "w", encoding="utf-8") as file:
            file.write(prettified_xml)

        os.replace(temp_filename, project_filepath)  # atomic replacement to avoid file corruption

    def project_file_exist(self, project_filepath):
        return os.path.exists(project_filepath)

    def load_from_xml(self, project_filepath):
        tree = ET.parse(project_filepath)
        root = tree.getroot()

        def get_text_or_empty(element, default=""):
            return element.text if element is not None and element.text is not None else default

        self.description = get_text_or_empty(root.find("description"))
        self.input_folder_path = get_text_or_empty(root.find("input_folder_path"))
        self.input_images_prefix = get_text_or_empty(root.find("input_images_prefix"))
        self.fps = int(root.find("fps").text)
        self.reverse_video = int(root.find("reverse_video").text)
        self.output_pathfile = get_text_or_empty(root.find("output_pathfile"))









# Globales
parameters = ClassParameters()








# Main
if __name__ == '__main__':

    # Configure arguments detection
    parser = argparse.ArgumentParser(description="Script used to generate video from images.")

    parser.add_argument(
        "project_filepath",
        nargs="?",
        type=str,
        help="Path to an existing project file.",
    )

    # Parse arguments
    args = parser.parse_args()

    # Treat the arguments
    if args.project_filepath == None:
        project_pathfile = input("\nNo project pathfile provided.\n"
                                 "--h or --help to get help.\n"
                                 "Enter to exit.\n"
                                 "Enter a pathfile to create a new project file.\n"
                                 "Input: ")

        if project_pathfile == "":
            sys.exit(0)

        print("")
        if parameters.project_file_exist(project_pathfile):
            overwrite_existing_project_file = ""
            while (overwrite_existing_project_file != "n") and (overwrite_existing_project_file != "y"):
                overwrite_existing_project_file = input("This file already exists.\n"
                                                        "Enter Y or y to overwrite the file, "
                                                        "otherwise enter N or n: ").lower()
            if overwrite_existing_project_file == "n":
                sys.exit(0)

        parameters.CreateNewProjectFile(project_pathfile)
        print("File created.")
        sys.exit(0)

    else:
        parameters.load_from_xml(args.project_filepath)
        print(f"Description: {parameters.description}")

    # Sort images for output video
    if parameters.reverse_video == 0:
        images = sorted([img for img in os.listdir(parameters.input_folder_path) if (img.endswith(".png")) and (img.startswith(parameters.input_images_prefix))])
    else:
        images = sorted([img for img in os.listdir(parameters.input_folder_path) if (img.endswith(".png")) and (img.startswith(parameters.input_images_prefix))], reverse=True)

    # Create output video
    if not parameters.output_pathfile.endswith(".mp4"):
        parameters.output_pathfile += ".mp4"

    with imageio.get_writer(parameters.output_pathfile, fps=parameters.fps) as writer:
        cnt_images = 0
        string_percent_images = ""
        for filename in images:
            image_path = os.path.join(parameters.input_folder_path, filename)
            image = imageio.v2.imread(image_path)
            writer.append_data(image)

            cnt_images += 1
            current_percent_images = f"{int(cnt_images / len(images) * 100)}"
            if current_percent_images != string_percent_images:
                print("", end="\r")
                print(f"{cnt_images}/{len(images)}, "
                      f"{current_percent_images}%", end="")
                string_percent_images = current_percent_images

    # End
    sys.exit(0)

