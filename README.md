# Fractal Toolbox

Fractals Toolbox is a series of python scripts that let you
discover the world of fractals by generating images and videos.
The provided tools allow you to customize many parameters
to suit your creativity.


## Table of Contents

1. [Features](#features)
2. [Gallery](#gallery)
3. [Requirements](#requirements)
4. [Usage](#usage)
5. [Examples](#examples)
6. [License](#license)
7. [Compatibility](#compatibility)
8. [Contributing](#contributing)
9. [Authors](#authors)


## Features

- Split into different scripts according to functions :
  a script to generate images, a script to modify image
  coloring without recalculating iterations and a script
  to assemble images into a video.  
  

- Based on a project file system in xml format for customizing
  general parameters without having to modify the script(s).  
  

- Parameters for pure calculations or recoloring of fractals
  (area, maximum number of iterations, parameters in formulas,
  color parameters, displacement parameters, etc.) are separated
  from project files via csv files for greater ease of use
  (one line equals one image).
  

- Customizable and adaptive number of significant digits in
  iteration calculations to optimize processing time and avoid
  image pixelation.
  

- Resume function for resuming image generation in the event
  of script stoppage.
  

- Zoom in/out function.
  

- Centering function to stay on interesting fractal shapes.
  

- Move up, down, left, right functionality.
  

- Log function for overall progress, as well as variable parameters
  related to zooming, moving and centering.
  

- Generation of iteration files in parallel with images for
  recoloring without the need for intensive recalculation.
  

- Multiprocessing image generation and recoloring script,
  with the option of configuring the number of cores to modulate
  CPU load and calculation time.
  

- Option to set the CPU percentage dedicated to image and color
  calculations.


## Gallery

Here are some examples of fractal videos created using the Fractal Toolbox :  
  

- [Zoom video of the Julia set](https://www.facebook.com/100088855103723/videos/pcb.545812228390609/1427190824868173)
- [Zoom out version of the same images](https://www.facebook.com/100088855103723/videos/pcb.545812228390609/561415066481875)


- [Video showing the impact of the iterations number on the Mandelbrot set](https://www.facebook.com/100088855103723/videos/586853053824957/)


## Requirements

- Python 3.x is required.
  

- Clone the project :
```bash
git clone https://github.com/Kuja2053/fractaltoolbox.git
cd FractalToolbox
```  


- Install the dependencies using :
```bash
pip install -r requirements.txt
```


## Usage

### Generating images

#### Generate fractal parameters new file

First, you need to create a CSV file containing the parameters
for calculating the images. One line is equivalent to one image,
except for the first line, which is never processed. You can
create a file by hand, but the most efficient way of processing
several images is to create a python script or other dedicated
script. The examples given later in this document can help you.  
  
The expected format is :
```csv
type_fractal;max_iterations;julia_a;julia_b;xmin;xmax;ymin;ymax;r;g;b;opt_next_image;zoom_amount;centering_sigma;centering_up;centering_down;centering_left;centering_right;move_x;move_y
julia;100;0.8910135587868762;-0.7435589375813296;-1.5;1.5;-1.5;1.5;38;4;36;;0.0;0.0;0;0;0;0;0.0;0.0
mandelbrot;50;;;-0.75;-0.747;0.06;0.063;40;45;5;;0.0;2.0;0;0;0;0;0.0;0.0
mandelbrot;1000;;;-0.75;-0.747;0.06;0.063;60;25;15;CENTERING+MOVE;0.0;2.0;0;0;1;1;0.0;1e-05
```

**type_fractal** : the expected values are ‘julia’ if based on the Julia set
or ‘mandelbrot’ to use the Mandelbrot set. Case is irrelevant.  
  

**max_iterations** : indicates the maximum number of iterations in the
calculation of points. The higher this value, the more interesting details
you will see in your images, but the longer the calculation time will be.
A value of 100 to 200 is interesting for the ‘Julia’ set but ‘Mandelbrot’
requires more iterations (1000 is a good value).  
  

**julia_a** and **julia_b** : these fields must be filled in if you have
chosen a set of ‘Julia’ and they correspond to the constants in the formula.
The shapes can be completely different depending on the values chosen.
It's up to you to explore.There are no coefficients to define for the
Mandelbrot set, as these are calculated automatically according to the
position of the point.  
  

**xmin**, **xmax**, **ymin** and **ymax** : respectively the minimum abscissa,
the maximum abscissa, the minimum ordinate and the maximum ordinate. These are
the bounds to choose from in the “Julia” or “Mandelbrot” set. The shapes may differ
depending on where you are in the fractal. However, the closer the bounds, the
greater the number of significant digits used, and therefore the longer the
calculations. Areas of interest for each of the fractals can be found on the
internet.  
  
**r**, **g** and **b** : these are the R, G and B coefficients for coloring
according to the number of iterations for each point. You can run several tests
to obtain different coloration in your images.  
  
**opt_next_image** : this field expects keywords to indicate the desired options
for the next image (leave this field empty if you don't want any options).
Case is irrelevant. Keywords can be separated by any character you like, except “;”.
‘**ZOOM**’ zooms in or out, ‘**CENTERING**’ automatically centers on the interesting shape
closest to the center, and ‘**MOVE**’ moves in the desired direction. These options can
be configured via dedicated fields, explained below. The values of **xmin**, **xmax**,
**ymin** and **ymax** are no longer taken into account for the next image(s) if one of
these options is activated. In this case, **xmin**, **xmax**, **ymin** and **ymax** must
only be entered for the first image.  
  
**zoom_amount** : enter this value if you have enabled the “ZOOM” option, to
indicate the zoom value between this image and the next one. It is a positive value,
non-zero, less than 1 to zoom in and greater than 1 to zoom out.  
  
**centering_sigma** : this value must be entered if the “CENTERING” option has been
activated. It corresponds to the sigma value for the standard deviation used to
search for interesting shapes. The higher the value, the more selective you'll be.
A value of 2.0 (95% of excluded values) is a good choice. No need to go beyond 3.0.  
  
**centering_up**, **centering_down**, **centering_left** and **centering_right** :
values to be set for centering, taking the value either 0 or 1. 0 indicates that
centering in this direction is forbidden, while 1 allows it. It is therefore possible
to exclude certain directions or allow them all (up, down, left and right).  
  
**move_x** and **move_y** : these fields must be completed if the “MOVE” option is
active, and provide information on the movement to be made between this image
and the next one (move_x < 0: left, move_x > 0: right, move_y < 0: down,
move_y > 0: up).


#### Create a new images calculation project

To create an empty image project file, simply run the “**make_images.py**” script without
providing any arguments. You'll then be asked to enter the path containing the name
to your new xml-format project file.  
  
The contents of the file will be as follows :

```xml
<?xml version="1.0" encoding="utf-8"?>
<Project_images>
 <description/>
 <inputs_pathfile/>
 <size_x>
  0
 </size_x>
 <size_y>
  0
 </size_y>
 <adaptive_decimal_precision>
  0
 </adaptive_decimal_precision>
 <output_folder_path/>
 <output_images_prefix/>
 <output_iterations_prefix/>
 <density_images_prefix/>
 <logs_pathfile/>
 <resume_pathfile/>
 <fps>
  0
 </fps>
</Project_images>
```

All that's left is to complete the fields as follows :

**description** : you can provide a short text describing your project. The description
will be displayed the next time you load the project file with “**make_images.py**”.  
  
**inputs_pathfile** : In this field, you must enter the path to the csv file
containing the fractal parameters (file format indicated above).  
  
**size_x** and **size_y** : corresponds to the desired resolution of the images,
with “size_x” the width and “size_y” the height.  
  
**adaptive_decimal_precision** : indicates the minimum number of significant digits
for iteration calculations (6 is a correct value).  
  
**output_folder_path** : indicates the name or path to the folder containing images
and iteration files. The folder will be created if it doesn't already exist.  
  
**output_images_prefix** : the images are numbered to make the link with the logs and
the CSV inputs files, but also for video assembly. This field simply asks for the
prefix to be used for image files.  
  
**output_iterations_prefix** : as with images, it is necessary to provide a prefix
for iteration files.  
  
**density_images_prefix** : this field asks for the prefix to be used for density files.
These files are optional and are used to display the shape recognition result of the
centering option. This is useful if you need to configure the “**centering_sigma**”
parameter of the input CSV files.  
  
**logs_pathfile** : you must provide the path and name of the log file
(format *.txt or *.log). This file can be set into the "**output_folder_path**" folder.  
  
**resume_pathfile** : you need to specify the path to the resume file so that you
can pick up where you left off if the script is stopped. It can also be placed in
the “**output_folder_path**” folder.  
  
**fps** : this is the number of fps for a possible future video. This indicates
the length of video available in realtime logs. Even if you don't want to make a
video, this value must be a positive integer greater than zero.


#### Start images calculation

To start image calculation, simply run “**make_images.py**” with the path to the image
project file you want as an unnamed parameter.  
  
There are several possibilities : either the project has never been launched and the
process begins, or at least one image has already been calculated, in which case
the script will ask you whether you want to start again from the beginning or pick up
where you left off.  
  
On the other hand, in the event of a project not being resumed, if the output folder
is not empty, you will be asked if you wish to delete its contents first.  
  
The logs displayed or written in the files look like this :
```csv
52/1440;3.61%;E:00h08m06s;R:04h45m;V:00m02s166ms;center(x,y)=(960,544);nearest_interesting(x,y)=(960,544);precision=6;x(min,max)=(-0.366926,0.320432);y(min,max)=(-0.337210,0.350150)
```

Available information includes :
- Progress.
- Elapsed time (“E” for “elapsed time”).
- Remaining time (“R” for “remaining time”).
- Calculated video time (“V” for “video time”).
- Current center coordinates.
- Future center coordinates for centering option.
- Current number of significant digits.
- Values of xmin, xmax, ymin and ymax.

The script also accepts the following arguments in addition to the project file :
```bash
--cores=desired_number_of_cores
```
By default, all cores are used, but you can choose the number of active cores for
multiprocessing to reduce CPU impact.

```bash
--cpu=maximum_cpu_time_in_percent
```
This can also be used to reduce CPU time by specifying the desired maximum
CPU load as a percentage.

```bash
--density
```
Request to generate density files to configure the centering option.
This makes the process slightly longer.


#### Using the images calculation resume function

It's quite simple : you can stop your script whenever you like, and the next time
you load it, you'll be asked whether you want to start again from the beginning or
resume after the last finalized image.


### Recoloring images

#### Generate recoloring parameter new file

Even if you've already generated your images, you can still change the coloring
quickly if you also have the iteration files (these files are normally generated
at the same time as the images).  
  
First, you need to create a CSV file containing the parameters
for recoloring the images. One line is equivalent to one image,
except for the first line, which is never processed. You can
create a file by hand, but the most efficient way of processing
several images is to create a python script or other dedicated
script. The examples given later in this document can help you.  
  
The expected format is :
```csv
input_iteration_pathfile;output_image_pathfile;size_x;size_y;R;G;B
../Examples/Outputs/mandelbrot_iterations_up\mandelbrot_iterations_00001.bin.zip;../Examples/Outputs/mandelbrot_iterations_up\mandelbrot_images_00001.png;1920;1088;60;60;60
../Examples/Outputs/mandelbrot_iterations_up\mandelbrot_iterations_00002.bin.zip;../Examples/Outputs/mandelbrot_iterations_up\mandelbrot_images_00002.png;1920;1088;60;60;60
```

**input_iteration_pathfile** : this field indicates the path to the iteration file.  
  
**output_image_pathfile** : this is the path to the image to be created. This
can be the same path as the original image (in which case the image will be
overwritten), but you can also create new images.  
  
**size_x** and **size_y** : these fields represent the resolution of the original
images, with “**size_x**” the width and “**size_y**” the height.  
  
**R**, **G** and **B** : represent the new RGB color coefficients to be applied.  
  

#### Start recoloring calculation

To start image coloration, simply run “**make_coloring.py**” with the path 
to the recoloring parameters file you want as an unnamed parameter.  

The script also accepts the following arguments in addition to the recoloring
parameters file :

```bash
--cores=desired_number_of_cores
```
By default, all cores are used, but you can choose the number of active cores for
multiprocessing to reduce CPU impact.

```bash
--cpu=maximum_cpu_time_in_percent
```
This can also be used to reduce CPU time by specifying the desired maximum
CPU load as a percentage.


### Assemble into a video

#### Generate video new project

To create an empty video project file, simply run the “**make_videos.py**” script
without providing any arguments. You'll then be asked to enter the path containing
the name to your new xml-format project file.  
  
The contents of the file will be as follows :

```xml
<?xml version="1.0" encoding="utf-8"?>
<Project_video>
 <description/>
 <input_folder_path/>
 <input_images_prefix/>
 <fps>
  0
 </fps>
 <reverse_video>
  0
 </reverse_video>
 <output_pathfile/>
</Project_video>
```

All that's left is to complete the fields as follows :

**description** : you can provide a short text describing your project.
The description will be displayed the next time you load the project file
with “**make_videos.py**”.  
  
**input_folder_path** : indicate the path to the folder containing the images
to be assembled into a video.

**input_images_prefix** : provides value of images suffixes.

**fps** : indicates the desired fps for the video.

**reverse_video** : allows you to edit the video in reverse if desired
(set to 1 to edit in reverse, otherwise set to 0).

**output_pathfile** : indicates the path and name to the video to be created.


#### Start video assembly

To start video assembly, simply run “**make_videos.py**” with the path to the video
project file you want as an unnamed parameter.  
  

## Examples

### Organization of examples

All example files have been placed in the “Examples” folder. The following folder
hierarchy has been adopted :

- "**Projects**" : this folder contains only the XML project files for creating images
  (with “**make_images.py**”) and videos (with “**make_videos.py**”).  
  

- "**Inputs**" : contains sample python scripts to generate CSV files for
  fractal calculation and recoloring parameters.  
  

- "**Inputs/Outputs**" : this folder doesn't originally exist, but is
  automatically created to host CSV files (for fractal parameters and
  recoloring).  
  

- "**Outputs**" : this folder doesn't exist at the outset, but is
  automatically created to accommodate subfolders (one per project)
  for storing results.


### *"Examples/Projects/images/julia_random.xml" (images)*

This is an example of a project generating random images in the
“**Julia**” set.  

Start by running the “**julia_random.py**” script in the “Examples/Inputs” folder
(no arguments required). This should have created the “Examples/Inputs/Outputs”
folder if it didn't exist, as well as the “julia_random.csv” file inside.  
  
Next, run “**make_images.py**”, loading the associated project file with the
following argument :

```bash
"../Examples/Projects/images/julia_random.xml"
```

The “Examples/Outputs/julia_random” folder had to be created and will
contain the results for this project.
  

### *"Examples/Projects/images/julia_zoom.xml" (images)*

This is an example project generating images for a zoom video in the “Julia” set.

Start by running the “**julia_zoom.py**” script in the “Examples/Inputs” folder
(no arguments required). This should have created the “Examples/Inputs/Outputs”
folder if it didn't exist, as well as the “julia_zoom.csv” file inside.  
  
Next, run “**make_images.py**”, loading the associated project file with the
following argument :

```bash
"../Examples/Projects/images/julia_zoom.xml"
```

The “Examples/Outputs/julia_zoom” folder had to be created and will
contain the results for this project.


### *"Examples/Projects/videos/video_julia_zoom_in.xml" (video)*

This folder uses images generated by the “Examples/Projects/images/julia_zoom.xml”
project to create a zoom in video at 24 fps in the “Julia” set.

Run “make_videos.py” and load the associated project file as an argument :

```bash
"../Examples/Projects/videos/video_julia_zoom_in.xml"
```

The video is created in “Examples/Outputs/julia_zoom”.


### *"Examples/Projects/videos/video_julia_zoom_out.xml" (video)*

Similar to the “Examples/Projects/videos/video_julia_zoom_in.xml” project,
but for creating a zoom out video.

Run “make_videos.py” and load the associated project file as an argument :

```bash
"../Examples/Projects/videos/video_julia_zoom_out.xml"
```

The video is also created in “Examples/Outputs/julia_zoom”.


### *"Examples/Projects/images/mandelbrot_iterations_up.xml" (images)*

This project is used to create a video showing the importance of the iterations
number in the “Mandelbrot” set. The number of calculations is increased frame by frame.

Start by running the “**mandelbrot_iterations_up.py**” script in the “Examples/Inputs”
folder (no arguments required). This should have created the “Examples/Inputs/Outputs”
folder if it didn't exist, as well as the “mandelbrot_iterations_up.csv” file inside.  
  
Next, run “**make_images.py**”, loading the associated project file with the
following argument :

```bash
"../Examples/Projects/images/mandelbrot_iterations_up.xml"
```

The “Examples/Outputs/mandelbrot_iterations_up” folder had to be created and will
contain the results for this project.


### *"Examples/Projects/images/mandelbrot_iterations_up.xml" (recoloring)*

This section shows an example of images recoloring without having to
recalculate them.  
  
Run the “**mandelbrot_iterations_up_recoloring.py**” script in the “Examples/Inputs”
folder (no arguments required). The “mandelbrot_iterations_up_recoloring.csv” file
must have been created in the “Examples/Inputs/Outputs” folder.  
  
Then run “**make_coloring.py**” with the following argument:

```bash
"../Examples/Inputs/Outputs/mandelbrot_iterations_up_recoloring.csv"
```

This must have recolored the images in the “Examples/Outputs/mandelbrot_iterations_up”
folder.


### *"Examples/Projects/videos/video_mandelbrot_iterations_up.xml" (video)*

This folder uses images generated by the
“Examples/Projects/images/mandelbrot_iterations_up.xml” project to create a video
at 24 fps in the “Mandelbrot” set.

Run “make_videos.py” and load the associated project file as an argument :

```bash
"../Examples/Projects/videos/video_mandelbrot_iterations_up.xml"
```

The video is created in “Examples/Outputs/mandelbrot_iterations_up”.


### *"Examples/Projects/images/mandelbrot_move_up.xml" (images)*

This example generates images for a video in which you move upwards through
the “Mandelbrot” set.

Start by running the “**mandelbrot_move_up.py**” script in the “Examples/Inputs”
folder (no arguments required). This should have created the “Examples/Inputs/Outputs”
folder if it didn't exist, as well as the “mandelbrot_move_up.csv” file inside.  
  
Next, run “**make_images.py**”, loading the associated project file with the
following argument :

```bash
"../Examples/Projects/images/mandelbrot_move_up.xml"
```

The “Examples/Outputs/mandelbrot_move_up” folder had to be created and will
contain the results for this project.


### *"Examples/Projects/videos/video_mandelbrot_move_up.xml" (video)*

This folder uses images generated by the “Examples/Projects/images/mandelbrot_move_up.xml”
project to create a video at 24 fps in the “Mandelbrot” set.

Run “make_videos.py” and load the associated project file as an argument :

```bash
"../Examples/Projects/videos/mandelbrot_move_up.xml"
```

The video is created in “Examples/Outputs/mandelbrot_move_up”.


## License
This project is licensed under the GNU General Public License v3.0.  
Copyright (C) 2024 Vivien ELIE  
  
You can view the full text of the license in the file [COPYING](COPYING).  

For more information about the GPLv3, visit the official website :  
[https://www.gnu.org/licenses/gpl-3.0.html](https://www.gnu.org/licenses/gpl-3.0.html).  



## Compatibility

This project was developed and tested on Windows.  
Compatibility with other systems (Linux, macOS) has not been verified.  
Contributions to improve portability are welcome !  

## Contributing

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push to the branch
5. Open a pull request


## Authors
Vivien ELIE, the main developer - [GitHub profile](https://github.com/Kuja2053)  
For inquiries, contact: kuja2053@hotmail.com  
