import csv
import json

def csv_to_2d_array(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        return list(reader)

csv_file = 'map_data.csv'
two_d_array = csv_to_2d_array(csv_file)
print(two_d_array)


HERO = '1'
BLOCK = '2'
MONSTER = '3'
FLAG = '4'

save_as = "world-1.json"

name = 'Bouncy fun times'
designer = 'Your Name'
width = len(two_d_array[0])
height = len(two_d_array)

gravity = 1.2
terminal_velocity = 24

data = {
    "world_name": name,
    "designer": designer,
    "world_width": width,
    "world_height": height,
    "gravity": gravity,
    "terminal_velocity": gravity,
    "hero_start": [],
    "blocks": [],
    "monsters": [],
    "flag": []   
}


for y, row in enumerate(two_d_array):
    for x, cell in enumerate(row):
        loc = [x, y]

        if cell == HERO:
            data['hero_start'].append(loc)
        elif cell == BLOCK:
            data['blocks'].append(loc)
        elif cell == MONSTER:
            data['monsters'].append(loc)
        elif cell == FLAG:
            data['flag'].append(loc)


print(data)

json_str = json.dumps(data)

with open(save_as, 'w') as f:
    f.write(json_str)
