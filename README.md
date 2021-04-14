# Marine and weather research in a novel, cost-efficient and democratic way
This repository contains all code and data associated with my high school senior thesis. 

# Thesis Abstract
Weather satellites have become an essential part of our everyday modern life. What many do not know is that some of these satellites transmit signals that anyone can receive with very basic equipment. The objectives of the study revolved around the United Nation's Sustainable Development Goals and how to introduce more accessible and democratic ways of conducting water and climate research. This study, therefore, examines the possibilities as an individual with low-cost equipment, to independently receive and conduct a scientific study with images directly from these weather satellites. The study analyses sea surface temperature (SST) in the Baltic Sea region and its development during the fall of 2020.

## Overview
The image and data processing method consisted mainly of two parts:
* To read and analyse pixel values from the decoded SST-image and return a average temperature value for the desired area.
* To collect relevant meta data stored in the decoded images.
The read temperature value and meta data for each observation shall then be stored in a CSV-file called ```SST.csv```.

## Usage
1. Create a directory ```img``` where all decoded SST-images are saved.
2. Then crop all the images manually to the area you want to read. Preferably with [inbac](https://github.com/weclaw1/inbac).
3. Save all cropped images in a sub directory called ```img/crop```.
4. Run ```python main.py``` in its home directory.
5. The sea surface temperature for all cropped images is read, all relevant meta data is then read from the original images and all data is finally saved in  ```data/SST.csv```.

### Observe
* Always use the default palette for SST in WxToImg, so that the false-color values match ```tempscale300.png```.

## Awards
* This project articipated in the national science fair [Swedish Exhibition for Young Scientists 2021](https://digitala-utstallningen.ungaforskare.se/finalutstallning/). 
* Won [Yale Science and Engineering Association Award](http://groupspaces.com/YSEA/pages/ysea-science-fair-award) and [Stockholm Junior Water Prize Sweden](https://www.siwi.org/prizes/stockholmjuniorwaterprize/) in the final.
* Will participate and represent Sweden in the international SJWP finale.

## Thesis
The full-text thesis can be read [here](https://drive.google.com/file/d/1xRwM7fLT9GnPWI2I8pavy73oVzc3Niuh/view?usp=sharing) in swedish and a shorter version in english [here](#).

## License
[MIT](https://choosealicense.com/licenses/mit/)
