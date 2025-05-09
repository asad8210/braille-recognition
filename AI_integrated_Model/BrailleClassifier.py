import cv2
import numpy as np
from math import sqrt

class BrailleImage(object):
    def __init__(self, image):
        self.original = cv2.imread(image)
        if self.original is None:
            raise IOError('Cannot open given image')

        gray = cv2.cvtColor(self.original, cv2.COLOR_BGR2GRAY)
        self.edged_binary_image = self.__get_edged_binary_image(gray)
        self.binary_image = self.__get_binary_image(gray)
        self.final = self.original.copy()
        self.height, self.width, self.channels = self.original.shape

    def bound_box(self, left, right, top, bottom, color=(255, 0, 0), size=1):
        self.final = cv2.rectangle(self.final, (left, top), (right, bottom), color, size)
        return True

    def get_final_image(self):
        return self.final

    def get_original_image(self):
        return self.original

    def get_edged_binary_image(self):
        return self.edged_binary_image

    def get_binary_image(self):
        return self.binary_image

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def __get_edged_binary_image(self, gray):
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        thres = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 4)
        blur2 = cv2.medianBlur(thres, 3)
        _, th2 = cv2.threshold(blur2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        blur3 = cv2.GaussianBlur(th2, (3, 3), 0)
        _, th3 = cv2.threshold(blur3, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return cv2.bitwise_not(th3)

    def __get_binary_image(self, gray):
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        _, th2 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        blur2 = cv2.medianBlur(th2, 3)
        _, th3 = cv2.threshold(blur2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return cv2.bitwise_not(th3)

def get_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return ((x2 - x1) ** 2) + ((y2 - y1) ** 2)

def get_left_nearest(dots, diameter, left):
    nearest = None
    for dot in dots:
        x, y = dot[0]
        dist = int(x - left)
        if dist <= diameter:
            if nearest is None or (int(nearest[0][0] - left) > dist):
                nearest = dot
    return nearest

def get_right_nearest(dots, diameter, right):
    nearest = None
    for dot in dots:
        x, y = dot[0]
        dist = int(right - x)
        if dist <= diameter:
            if nearest is None or (int(right - nearest[0][0]) > dist):
                nearest = dot
    return nearest

def get_dot_nearest(dots, diameter, pt1):
    nearest = None
    diameter **= 2
    for dot in dots:
        point = dot[0]
        dist_from_pt1 = get_distance(point, pt1)
        if dist_from_pt1 <= diameter:
            if nearest is None or get_distance(nearest[0], pt1) > dist_from_pt1:
                nearest = dot
    return nearest

def get_combination(box, dots, diameter):
    result = [0, 0, 0, 0, 0, 0]
    left, right, top, bottom = box
    midpointY = int((bottom - top) / 2)
    end = (right, midpointY)
    start = (left, midpointY)
    width = int(right - left)
    corners = {
        (left, top): 1, (left, int((top + bottom) / 2)): 2, (left, bottom): 3,
        (right, top): 4, (right, int((top + bottom) / 2)): 5, (right, bottom): 6
    }
    for corner in corners:
        D = get_dot_nearest(dots, int(diameter), corner)
        if D is not None:
            dots.remove(D)
            result[corners[corner] - 1] = 1
        if len(dots) == 0:
            break
    return end, start, width, tuple(result)

def translate_to_number(value):
    return {'a': '1', 'b': '2', 'c': '3', 'd': '4', 'e': '5',
            'f': '6', 'g': '7', 'h': '8', 'i': '9', 'j': '0'}.get(value.lower(), '*')

class Symbol(object):
    def __init__(self, value=None, letter=False, special=False):
        self.is_letter = letter
        self.is_special = special
        self.value = value

    def is_valid(self):
        return self.value is not None and (self.is_letter or self.is_special)

    def letter(self):
        return self.is_letter

    def special(self):
        return self.is_special

class BrailleClassifier(object):
    symbol_table = {
        (1,0,0,0,0,0): Symbol('a', True), (1,1,0,0,0,0): Symbol('b', True),
        (1,0,0,1,0,0): Symbol('c', True), (1,0,0,1,1,0): Symbol('d', True),
        (1,0,0,0,1,0): Symbol('e', True), (1,1,0,1,0,0): Symbol('f', True),
        (1,1,0,1,1,0): Symbol('g', True), (1,1,0,0,1,0): Symbol('h', True),
        (0,1,0,1,0,0): Symbol('i', True), (0,1,0,1,1,0): Symbol('j', True),
        (1,0,1,0,0,0): Symbol('k', True), (1,1,1,0,0,0): Symbol('l', True),
        (1,0,1,1,0,0): Symbol('m', True), (1,0,1,1,1,0): Symbol('n', True),
        (1,0,1,0,1,0): Symbol('o', True), (1,1,1,1,0,0): Symbol('p', True),
        (1,1,1,1,1,0): Symbol('q', True), (1,1,1,0,1,0): Symbol('r', True),
        (0,1,1,1,0,0): Symbol('s', True), (0,1,1,1,1,0): Symbol('t', True),
        (1,0,1,0,0,1): Symbol('u', True), (1,1,1,0,0,1): Symbol('v', True),
        (0,1,0,1,1,1): Symbol('w', True), (1,0,1,1,0,1): Symbol('x', True),
        (1,0,1,1,1,1): Symbol('y', True), (1,0,1,0,1,1): Symbol('z', True),
        (0,0,1,1,1,1): Symbol('#', special=True),
        (0,1,0,0,1,1): Symbol('.', special=True),
        (0,1,0,0,0,1): Symbol(',', special=True),
        (0,1,1,0,0,1): Symbol('?', special=True),
        (0,1,1,0,1,0): Symbol('!', special=True),
    }

    def __init__(self):
        self.result = ''
        self.shift_on = False
        self.prev_end = None
        self.number = False

    def push(self, character):
        if not character.is_valid():
            return
        box = character.get_bounding_box()
        dots = character.get_dot_coordinates()
        diameter = character.get_dot_diameter()
        end, start, width, combination = get_combination(box, dots, diameter)
        if combination not in self.symbol_table:
            self.result += '*'
            return
        if self.prev_end is not None:
            dist = get_distance(self.prev_end, start)
            if dist * 0.5 > (width ** 2):
                self.result += ' '
        self.prev_end = end
        symbol = self.symbol_table[combination]
        if symbol.letter() and self.number:
            self.number = False
            self.result += translate_to_number(symbol.value)
        elif symbol.letter():
            self.result += symbol.value.upper() if self.shift_on else symbol.value
        else:
            if symbol.value == '#':
                self.number = True

    def digest(self):
        return self.result

    def clear(self):
        self.result = ''
        self.shift_on = False
        self.prev_end = None
        self.number = False
