from PIL import Image
import math
import statistics

#Create dictionary with RGB(tuple) and temp-values(int)
def temp_scale(temp_array):
    temp_dict = {}
    temp = 0
    for i in reversed(temp_array):
        temp_dict[i] = round(temp, 2)
        temp += 30.0/(len(temp_array)-1)
    return temp_dict

#Distance to RGB values
def distance(c1, c2):
    (r1,g1,b1) = c1
    (r2,g2,b2) = c2
    return math.sqrt((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2)

#Removes false values/temperatures <=5 (Purple from clouds)
def remove_false(wx_array, temp_dict):
    new_list = []
    for color in wx_array:
        if color != (0,0,0):
            if color in temp_dict:
                if temp_dict[color] <= 5:
                    new_list.append((0,0,0))
                else:
                    new_list.append(color)
            else:
                colors = list(temp_dict.keys())
                closest_colors = sorted(colors, key=lambda value: distance(value, color))
                if temp_dict[closest_colors[0]] <= 5:
                    new_list.append((0,0,0))
                else:
                    new_list.append(color)
        else:
            new_list.append(color)
    return new_list

#Creates list with pixel temperature value
def calc_temp(wx_array, temp_dict):
    pixel_count = 0
    color_temp = []
    for color in wx_array:
        if color != (0,0,0):
            if color in temp_dict:
                #Ignore false values >=5 (Purple from clouds)
                if temp_dict[color] >= 5.0:
                    color_temp.append(temp_dict[color])
                    pixel_count += 1
            else:
                colors = list(temp_dict.keys())
                closest_colors = sorted(colors, key=lambda value: distance(value, color))
                if temp_dict[closest_colors[0]] >= 5.0:
                    color_temp.append(temp_dict[closest_colors[0]])
                    pixel_count += 1
    return color_temp

def get_temperature(filename):
    #Open Large Temperature Scale
    temp_image = Image.open("tempscale300.png")
    temp_array = list(temp_image.getdata())

    temp_dict = temp_scale(temp_array)

    #Opens weather image
    wx_image = Image.open(filename)
    wx_array = list(wx_image.getdata())

    #Save new edited image
    #correct_wx_image = Image.new(wx_image.mode, wx_image.size)
    #correct_wx_image.putdata(remove_false(wx_array, temp_dict))
    #wx_array = list(correct_wx_image.getdata())

    #correct_wx_image.save(filename[:-4] + "-corrected.png")

    #Calculated temperature from image
    temp_array = calc_temp(wx_array, temp_dict)
    
    return temp_array

if __name__ == "__main__":

    temp_array = get_temperature("G:/Min enhet/Classroom/Gymnasiearbete 3B/Code/img/new/crops/noaa-18-202011071943-sea.png")
    temperature = statistics.mean(temp_array)
    print(temperature)
    print(len(temp_array))