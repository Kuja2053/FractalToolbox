import os
import sys
import imageio.v2





# Classes
class ClassParameters:
    def __init__(self):
        self.input_output_folder_pathname = ""
        self.input_output_images_prefix = ""
        self.fps = 0
        self.reverse_video = 0
        self.output_filename = ""





# Globales
parameters = ClassParameters()








# Main
if __name__ == '__main__':

    # Configuration
    parameters.input_output_folder_pathname = "Outputs/random_together_v0_v1"
    parameters.input_output_images_prefix = "julia_random_"
    parameters.fps = 24
    parameters.reverse_video = 0
    parameters.output_filename = "julia_random"

    # Sort images for output video
    if parameters.reverse_video == 0:
        images = sorted([img for img in os.listdir(parameters.input_output_folder_pathname) if (img.endswith(".png")) and (img.startswith(parameters.input_output_images_prefix))])
    else:
        images = sorted([img for img in os.listdir(parameters.input_output_folder_pathname) if (img.endswith(".png")) and (img.startswith(parameters.input_output_images_prefix))], reverse=True)

    # Create output video
    with imageio.get_writer(f"{parameters.input_output_folder_pathname}/{parameters.output_filename}.mp4", fps=parameters.fps) as writer:
        for filename in images:
            image_path = os.path.join(parameters.input_output_folder_pathname, filename)
            image = imageio.v2.imread(image_path)
            writer.append_data(image)

    # End
    sys.exit(0)

