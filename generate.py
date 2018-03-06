from collections import namedtuple

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


bottom_buffor = 200
line_padding = 25

pages_format = {'A5': (14.8, 21),
                'A4': (21, 29.7),
                'A3': (29.7, 42)}

Size = namedtuple('Size', ['x', 'y'])


class PrintSize(object):
    def __init__(self, width, height, dpi):
        self.width = int(self.to_inch(width) * dpi)
        self.height = int(self.to_inch(height) * dpi)

    def to_tuple(self):
        return (self.width, self.height)

    def rotate(self):
        self.width, self.height = self.height, self.width

    @staticmethod
    def to_inch(val):
        return val / 2.54


class GuestCard(object):
    def __init__(self, size, text, font, bg=(255, 255, 255)):
        self.img = Image.new('RGB', size, bg)
        self.draw = ImageDraw.Draw(self.img)
        self.font = font

        self._set_text(text)

    def _set_text(self, text):
        text_size = Size(*font.getsize(text))
        if text_size.x < img_size.x - 20:
            text_y_position = (img_size.y - bottom_buffor - text_size.y)/2
            text_x_position = (img_size.x - text_size.x)/2 + 20

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
        """Save card with filename as guest name"""
        with open('{}.jpg'.format(filename), 'w') as f:
            self.img.save(f, 'JPEG')

    def get_img(self):
        """Not sure if nessesary"""
        return self.img


class CardsGenerator(object):
    pad = 10

    def __init__(self, guests, card_size, font, page_format='A3', dpi=300):
        """
        gusets     is a list with names
        card_size  tuple in cm
        font       object ImageFont
        """
        self.guests = guests
        self.card_size = PrintSize(*card_size, dpi)
        self.page_size = PrintSize(*pages_format[page_format], dpi)
        self.font = font
        self.cards = []

    def generate_cards(self):
        for guest in self.guests:
            card = GuestCard(self.card_size.to_tuple(), guest, self.font)
            self.cards.append(card)

    def create_print_files(self):
        rotation, cards_on_page = self.get_max_cards_on_page()
        if rotation:
            self.page_size.rotate()

        files_with_cards = len(self.cards) / cards_on_page
        if files_with_cards is not int:
            files_with_cards = int(files_with_cards + 1)
        print(files_with_cards)
        for file_id in range(files_with_cards):
            page = Image.new('RGB', self.page_size.to_tuple())
            x, y = 0, 0
            for _ in range(cards_on_page):
                if self.cards:
                    c = self.cards.pop()
                    page.paste(c.get_img(), (x, y))
                    x += self.card_size.width + self.pad
                    if x + self.card_size.width > self.page_size.width:
                        x = 0
                        y += self.card_size.height + self.pad
                else:
                    break
            with open('cards_{}.jpeg'.format(file_id), 'w') as f:
                page.save(f, 'JPEG')

    def get_max_cards_on_page(self):
        x1 = self.page_size.width // (self.card_size.width +
                                      self.pad)
        y1 = self.page_size.height // (self.card_size.height +
                                       self.pad)

        x2 = self.page_size.width // (self.card_size.height +
                                      self.pad)
        y2 = self.page_size.height // (self.card_size.width +
                                       self.pad)

        if x1*y1 >= x2*y2:
            return False, x1*y1
        else:
            return True, x2*y2


# img_size = (1890, 1181)
img_size = Size(945, 600)
font = ImageFont.truetype('LiberationSans-Bold.ttf', 100)

with open('guests.txt') as f:
    guests = f.readlines()

gen = CardsGenerator(guests, (8, 5), font)
gen.generate_cards()
gen.create_print_files()
