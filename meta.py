from PIL import Image
import os
from datetime import datetime
import csv
from get_temperature import get_temperature
import statistics

with open("data/SST.csv", mode="w", newline="") as SST_file:
    fieldnames = ["Datum Tid (UTC)", "Satellit", "Elevation", "Havstemperatur", "Pixlar"]
    writer = csv.DictWriter(SST_file, delimiter=";", fieldnames=fieldnames)
    writer.writeheader()

    path, dirs, files = next(os.walk("img/crop/"))
    file_count = len(files)
    iteration = 0

    #Loops through all images in directory
    for entry in os.scandir("img//crop/"):
        print("Image " + str(iteration) + " of " + str(file_count))
        iteration += 1

        #For PNG-files
        if entry.path.endswith(".png") and entry.is_file():
            print(entry.path[9:])

            image = Image.open("img" + entry.path[9:])
            image.load()
            
            time = image.info["Pass Start"]
            time = time[:-4]
            date_object = datetime.strptime(time, "%d %b %Y %H:%M:%S")

            temp_array = get_temperature(entry.path)

            writer.writerow({"Datum Tid (UTC)" : date_object, "Satellit" : image.info["Satellite"], "Elevation" : image.info["Elevation"], "Havstemperatur": round(statistics.mean(temp_array), 2), "Pixlar" : len(temp_array)})
        
        #For JPG-files
        elif entry.path.endswith(".jpg") and entry.is_file():
            print(entry.path[9:])
            
            image = Image.open("img/" + entry.path[9:])

            image_comment = (image.info["comment"]).decode()
            image_comment = image_comment[:-1]

            image_info = dict((x.strip(), y.strip()) 
			for x, y in (element.split(': ') 
			for element in image_comment.split('\n')))

            time = image_info["Pass Start"]
            time = time[:-4]
            date_object = datetime.strptime(time, "%d %b %Y %H:%M:%S")

            temp_array = get_temperature(entry.path)

            writer.writerow({"Datum Tid (UTC)" : date_object, "Satellit" : image_info["Satellite"], "Elevation" : int(image_info["Elevation"]), "Havstemperatur": round(statistics.mean(temp_array), 2), "Pixlar" : len(temp_array)})