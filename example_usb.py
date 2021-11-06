#!/usr/bin/env python

import brotherlabel
from PIL import Image, ImageFont
from label import Label
import items

backend = brotherlabel.USBBackend("usb://0x04f9:0x2085")
printer = brotherlabel.PTPrinter(backend)
printer.quality = brotherlabel.Quality.high_quality
printer.tape = brotherlabel.Tape.TZe12mm
# printer.tape.right_margin = 10
# printer.brotherlabel = {'print_area': 150, 'right_margin': 13}
printer.margin = 0
print(printer.tape)
print(printer.get_status().to_string())

SIZE = 60
font = ImageFont.truetype("msttcorefonts/timesi.ttf", SIZE)
# Use it in the label template, e.g.


class MyLabel(Label):
    items = [
        [items.Text(font, pad_right=50)]
    ]

# Instantiate the label with specific data
l = MyLabel("Jeaaaaannee <3 <3")
print(type(printer.tape.print_area))
# img = l.render(height=150)

img = Image.open('banana.png')
print(printer.print([img]).to_string())
