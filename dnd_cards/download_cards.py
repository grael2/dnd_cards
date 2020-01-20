import csv
import urllib.request
from time import sleep
from PIL import Image
import os
import math

card_width, card_height = 803, 1039
border_x, border_y = 10, 30
a4_size = 2480, 3508
brown_background_rgb = 87, 56, 41, 0  # brown
links_file = 'linki_warlock.txt'
cards_directory = 'karty_warlock'

def download_cards():
    with open(links_file, 'r') as in_file:
        reader = csv.reader(in_file)
        for i, line in enumerate(reader):
            if i != 0:
                sleep(0.5)
                print(line)
                urllib.request.urlretrieve(line[1], cards_directory+'/' + line[2] + '.png')


def prepare_cards_to_print():
    offsets = [(0, 0 + border_y), (card_width + border_x, 0 + border_y), (card_width * 2 + border_x * 2, 0 + border_y),
               (0, card_height + border_y * 2), (card_width + border_x, card_height + border_y * 2),
               (card_width * 2 + border_x * 2, card_height + border_y * 2),
               (0, card_height * 2 + border_y * 3), (card_width + border_x, card_height * 2 + border_y * 3),
               (card_width * 2 + border_x * 2, card_height * 2 + border_y * 3)]

    current_sheet = Image.new("RGBA", a4_size, brown_background_rgb)
    cards = os.listdir(cards_directory)
    filler_cards_count = 0
    for i in range(8):
        if (len(cards) + i) % 9 == 0:
            filler_cards_count = i
            break

    old_page_number = 1
    for i, card in enumerate(cards + ['background.png'] * filler_cards_count):
        page_number = math.ceil((i + 1) / 9)
        if page_number != old_page_number:
            current_sheet = Image.new("RGBA", a4_size, brown_background_rgb)
        old_page_number = page_number
        offsets_index = i % 9

        x_offset, y_offset = offsets[offsets_index][0], offsets[offsets_index][1]
        if i < len(cards):
            image = Image.open(cards_directory+ "/" + card)
        else:
            image = Image.open(card)

        cart_cropped = image.crop(image.getbbox()).resize((card_width, card_height))
        current_sheet.paste(cart_cropped, (x_offset, y_offset), cart_cropped)
        current_sheet.save('druk/page_' + str(page_number) + '.bmp')
        # if offsets_index == 8:
        #     current_sheet.show()


download_cards()
prepare_cards_to_print()

