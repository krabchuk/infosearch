# -*- coding: UTF-8 -*-

import numpy as np


class LanguageModel:
    def __init__(self, queries_filename):
        self.dict = {}

        with open(queries_filename, "r") as f:
            for line in f:
                line = line.strip()
                q = line.split("\t")
                if len(q) == 1:
                    right_q = q[0]
                else:
                    right_q = q[1]
                for word in right_q.split():
                    try:
                        self.dict[word] += 1
                    except KeyError:
                        self.dict[word] = 1


class ErrorModel:
    def __init__(self):
        pass


keyboard_en = [
    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]"],
    ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'"],
    ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"]
]

keyboard_ru = [
    ["й", "ц", "у", "к", "е", "н", "г", "ш", "щ", "з", "х", "ъ"],
    ["ф", "ы", "в", "а", "п", "р", "о", "л", "д", "ж", "э"],
    ["я", "ч", "с", "м", "и", "т", "ь", "б", "ю", "."]
]


def key_coordinate(key):
    for line in range(3):
        if key in keyboard_en[line]:
            return line, keyboard_en[line].index(key)
        if key in keyboard_ru[line]:
            return line, keyboard_ru[line].index(key)

    return 1000, 1000


def keys_distance(key1, key2):
    coord1 = key_coordinate(key1)
    coord2 = key_coordinate(key2)
    dist = np.sqrt((coord1[0] - coord2[0]) * (coord1[0] - coord2[0]) +
                   (coord1[1] - coord2[1]) * (coord1[1] - coord2[1]))
    return dist


key_distances_data = None


def update_key_distances_data():
    key_distances_data = {}
    for layout1 in [keyboard_en, keyboard_ru]:
        for line1 in layout1:
            for key1 in line1:
                for layout2 in [keyboard_en, keyboard_ru]:
                    for line2 in layout2:
                        for key2 in line2:
                            key_distances_data[(key1, key2)] = keys_distance(key1, key2)


def lev_dist(first_string, second_string, insert_cost=1, delete_cost=1, replace_cost=1, swap_cost=1):
    if key_distances_data is None:
        update_key_distances_data()
    first_string_len = len(first_string) + 1
    second_string_len = len(second_string) + 1
    d = np.zeros((first_string_len, second_string_len))

    first_string = " " + first_string
    second_string = " " + second_string

    d[0, 0] = 0
    for i in range(1, first_string_len):
        d[i, 0] = d[i-1, 0] + delete_cost
    for j in range(1, second_string_len):
        d[0, j] = d[0, j-1] + insert_cost

    for i in range(1, first_string_len):
        for j in range(1, second_string_len):
            if first_string[i] == second_string[j]:
                d[i, j] = d[i-1, j-1]
            else:
                d[i, j] = d[i-1, j-1] + replace_cost

            d[i, j] = min(d[i, j],
                          d[i-1, j] + delete_cost,
                          d[i, j-1] + insert_cost)

            if i > 1 and j > 1 and first_string[i] == second_string[j - 1] and first_string[i - 1] == second_string[j]:
                d[i, j] = min(d[i, j],
                              d[i - 2, j - 2] + key_distances_data[(first_string[i], first_string[i-1])])

    return d[first_string_len - 1, second_string_len - 1]

