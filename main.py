from PIL import Image, ImageDraw
import math
import numpy as np

def parse_data_line(text: str):
    space_idx = text.index(' ')
    
    x = int(text[:space_idx])
    y = int(text[(space_idx + 1):])

    return (x, y)

angle = 50 * (math.pi / 180)
origin_x = 480
origin_y = 480

translate_plus_matrix = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [origin_x, origin_y, 1]
], dtype=np.float64)

translate_minus_matrix = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [-origin_x, -origin_y, 1]
], dtype=np.float64)

rotation_matrix = np.array([
    [math.cos(angle), math.sin(angle), 0],
    [-math.sin(angle), math.cos(angle), 0],
    [0, 0, 1]
], dtype=np.float64)

transform_matrix = np.matmul(np.matmul(translate_minus_matrix, rotation_matrix), translate_plus_matrix)

img = Image.new("RGB", (960, 960))
img_draw = ImageDraw.ImageDraw(img)

with open("DS4.txt", mode='r') as data_file:
    while True:
        line = data_file.readline()
        if line == "":
            break

        (point_x, point_y) = parse_data_line(line)
        point = np.array([[point_x, point_y, 1]], dtype=np.float64)
        
        transformed_point = np.matmul(point, transform_matrix)

        img_draw.point((transformed_point[0][0], transformed_point[0][1]), fill=(0, 0, 255)) 

img.save("result.jpg", "jpeg")