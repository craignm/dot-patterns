import math
from PIL import Image
from sys import stdout

coordinates = []

def output_row(start_x, y):        
   for x_offset in range(0, 9600, 25):
        if x_offset % 75 == 0:
            continue
        x = start_x + x_offset
        if x > 0 and x < 600:
            coordinates.append({'x': x, 'y': y + 900 + 12.5})


def cnc_write_prefix(f):
    f.write("""
% 1/4" flat end mill, Z-min: -11
G90 ; use absolute coordinates
G17 ; select plane XY
G21 ; set units to mm
G28 G91 Z0 ; home
G90 ; use absolute coordinates

T201 M6 ; tool 201: 1/4" flat end mill
S18000 M3 ; router to 18,000 rpm, spindle on
G54; use coordinate system 1
""")


def cnc_write_suffix(f):
    f.write("""
Z15 ; raise router
G28 G91 Z0 ; home Z
G90 ; use absolute coordinates
G28 G91 X0 Y0 ; home X an Y
G90 ; use absolute coordinates
%
""")

def cnc_write_drill(f, x, y):
    f.write("""
G0 Z5
X{x} Y{y}
G1 Z-11 F508
""".format(x=x, y=1800 - y))

def coordinate_key(coordinate):
    return math.floor(coordinate['y'] / 12.5) * 48 + coordinate['x'] / 12.5

def cnc_write(name):
    with open(name + '.nc', "w") as f:
        cnc_write_prefix(f)
        coordinates.sort(key=coordinate_key)

        for coordinate in coordinates:
            cnc_write_drill(f, coordinate['x'], coordinate['y'])
    
        cnc_write_suffix(f)

def svg_write(name):
    coordinates.sort(key=coordinate_key)

    with open(name + '.svg', "w") as f:
        f.write('<svg width="600mm" height="1800mm" xmlns="http://www.w3.org/2000/svg">') 

        for coordinate in coordinates:
            f.write('<circle cx="{x}mm" cy="{y}mm" r="3mm"/>\n'.format(
                x=coordinate['x'], y=coordinate['y']))

        f.write('</svg>')

def write_pattern(name):
    svg_write(name)
    cnc_write(name)
    global coordinates
    coordinates = []

# Speaker grille
coordinates.append({'x': 300, 'y': 900})
for radius in range(1, 40):
    for dot in range(0, radius * 6):
        theta = 2 * math.pi * dot / (radius * 6)
        x = radius * math.sin(theta) * 25 + 300
        y = radius * math.cos(theta) * 25 + 900
        if x > 0 and x < 600 and y > 0 and y < 1800:
            coordinates.append({'x': x, 'y': y})

write_pattern('speaker')

# Fibonacci spiral
phi = (1+math.sqrt(5.0))/2

for n in range(0, 6000):
    theta = 2 * math.pi / (phi * phi) * n
    radius = math.sqrt(n)

    x = radius * math.sin(theta) * 14 + 300
    y = radius * math.cos(theta) * 14 + 900
    if x > 0 and x < 600 and y > 0 and y < 1800:
        coordinates.append({'x': x, 'y': y})

write_pattern('fibonacci')

# Parabola
for y in range(-900, 900, 25):
    start_x = math.floor(y * y / 25 / 25) - 1800
    output_row(start_x, y)

write_pattern('parabola')

# Sine wave
for y in range(-900, 900, 25):
    start_x = math.floor(math.sin(y / 1800 * 2 * math.pi) * 250) - 250
    output_row(start_x, y)

write_pattern('sine')

# Chevron
for y in range(-900, 900, 25):
    start_x = - math.floor(abs(y % 300 - 150) / 1.5)
    output_row(start_x, y)
write_pattern('chevron')

# Sigmoid
for y in range(-900, 900, 25):
    start_x = math.floor(1 / (1 + math.exp(-y / 200)) * 550) - 775
    output_row(start_x, y)
write_pattern('sigmoid')

# Hyperbola
for y in range(-900, 900, 25):
    if y == 0:
        start_x = math.floor(900 / 10 * 30) - 6000
    else:
        start_x = math.floor(900 / y * 30) - 6000
    output_row(start_x, y)
write_pattern('hyperbola')

# Wrench
im = Image.open('/Users/craignm/Dropbox Dropbox/Craig Nevill-Manning/graphics/Photoshop/wrench 2.gif')
row = 0
column = 0

for pixel in im.getdata():
    if pixel == 0:
        coordinates.append({'x': column * 12.5, 'y': row * 12.5})

    column += 1
    if column == 48:
        column = 0
        row += 1

write_pattern('wrench')

        