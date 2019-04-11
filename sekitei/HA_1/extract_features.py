# coding: utf-8

import sys
from random import shuffle
import urlparse
import re
from urllib import unquote
# you may add imports if needed (and if they are installed)


def add_feature(features, feature_name):
    try:
        features[feature_name] += 1
    except:
        features[feature_name] = 1


def get_urls_from_file(filename):
    urls = []
    with open(filename) as f:
        for line in f:
            urls.append(line.strip())
    return urls


def got_ext(string):
    if re.match(r'.+[.](\w+)', string):
        return re.findall(r'.+[.](\w+)', string)[0]


def extract_features(INPUT_FILE_1, INPUT_FILE_2, OUTPUT_FILE):
    features = {}
    urls = []
    for f in (INPUT_FILE_1, INPUT_FILE_2):
        whole_urls = get_urls_from_file(f)
        shuffle(whole_urls)
        urls += whole_urls[:1000]

    for url in urls:
        parsed = urlparse.urlsplit(url)
        segments = unquote(parsed.path).split('/')
        qs = urlparse.parse_qs(unquote(parsed.query))

        for param in qs.keys():
            add_feature(features, 'param_name:' + param)
            add_feature(features, 'param:' + param + '=' + str(qs[param]))

        index = 0
        for segment in segments:
            if segment == "":
                continue
            add_feature(features, 'segment_name_' + str(index) + ':' + segment)
            add_feature(features, 'segment_len_' + str(index) + ':' + str(len(segment)))
            ext = got_ext(segment)
            if segment.isdigit():
                add_feature(features, 'segment_[0-9]_' + str(index) + ':1')
            if re.match(r'\D+\d+\D*', segment):
                add_feature(features, 'segment_substr[0-9]_' + str(index) + ':1')
                if ext:
                    add_feature(features, 'segment_ext_substr[0-9]_' + str(index) + ':' + ext)
            if ext:
                add_feature(features, 'segment_ext_' + str(index) + ':' + ext)
            index += 1
        add_feature(features, "segments:" + str(index))

    features = dict(sorted(features.items(), key=lambda x: -x[1]))

    with open(OUTPUT_FILE, 'w') as f:
        for i in features:
            if features[i] > 100:
                f.write(str(i) + '\t' + str(features[i]) + '\n')
