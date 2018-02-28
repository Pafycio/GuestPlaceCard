from collections import namedtuple

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


bottom_buffor = 200
line_padding = 25

Size = namedtuple('Size', ['x', 'y'])


class GuestCard(object):
    def __init__(self, size, text, font, bg=(255, 255, 255)):
        self.img = Image.new('RGB', size, bg)
        self.draw = ImageDraw.Draw(self.img)
        self.font = font

        self._set_text(text)

    def _set_text(self, text):
        text_size = Size(*font.getsize(text))
        if text_size.x < img_size.x:
            text_y_position = (img_size.y - bottom_buffor - text_size.y)/2
            text_x_position = (img_size.x - text_size.x)/2

            self.draw.text((text_x_position, text_y_position),
                           text, (0, 0, 0), font=font)
        else:
            name, surname = text.split(' ')
            name_y_position = (img_size.y - bottom_buffor -
                               (2*text_size.y) - line_padding)/2
            surname_y_position = name_y_position + text_size.y + line_padding

            name_x_position = (img_size.x - font.getsize(name)[0])/2
            surname_x_position = (img_size.x - font.getsize(surname)[0])/2

            self.draw.text((name_x_position, name_y_position),
                           name, (0, 0, 0), font=font)
            self.draw.text((surname_x_position, surname_y_position),
                           surname, (0, 0, 0), font=font)

    def save(self, filename):
        with open('{}.jpg'.format(filename), 'w') as f:
            self.img.save(f, 'JPEG')

    def get_img(self):
        return self.img


class CardGenerator(object):
    def __init__(self, guests, card_size, page_format, print_dpi):

        # img_size = (1890, 1181)


img_size = Size(945, 600)
font = ImageFont.truetype('LiberationSans-Bold.ttf', 100)

guests = ['Pawel Fert', 'Urszula Szelegiewicz']

for guest in guests:
    card = GuestCard(img_size, guest, font)
    card.save(guest.replace(' ', ''))
