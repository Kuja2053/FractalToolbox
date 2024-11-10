import os
import sys
import imageio.v2





# Classes
class ClassParameters:
    def __init__(self):
        self.input_output_folder_pathname = ""
        self.fps = 0
        self.reverse_video = 0





# Globales
parameters = ClassParameters()








# Main
if __name__ == '__main__':

    # Configuration
    parameters.input_output_folder_pathname = "output"
    parameters.fps = 24
    parameters.reverse_video = 0

    # Sort images for output video
    if parameters.reverse_video == 0:
        images = sorted([img for img in os.listdir(parameters.input_output_folder_pathname) if (img.endswith(".png")) and (img.startswith("julia_zoom_"))])
    else:
        images = sorted([img for img in os.listdir(parameters.input_output_folder_pathname) if (img.endswith(".png")) and (img.startswith("julia_zoom_"))], reverse=True)

    # Create output video
    if parameters.reverse_video == 0:
        filename = "julia"
    else:
        filename = "reverse_julia"
    with imageio.get_writer(f"{parameters.input_output_folder_pathname}/{filename}.mp4", fps=parameters.fps) as writer:
        for filename in images:
            image_path = os.path.join(parameters.input_output_folder_pathname, filename)
            image = imageio.v2.imread(image_path)
            writer.append_data(image)

    # End
    sys.exit(0)

