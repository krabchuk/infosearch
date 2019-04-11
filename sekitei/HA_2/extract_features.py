# coding: utf-8

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


def extract_all_features_from_url (url):
    features = []
    parsed = urlparse.urlsplit(url)
    segments = unquote(parsed.path).split('/')
    qs = urlparse.parse_qs(unquote(parsed.query))

    for param in qs.keys():
        features.append('param_name:' + param)
        features.append('param:' + param + '=' + str(qs[param]))

    index = 0
    for segment in segments:
        if segment == "":
            continue
        features.append('segment_name_' + str(index) + ':' + segment)
        features.append('segment_len_' + str(index) + ':' + str(len(segment)))
        ext = got_ext(segment)
        if segment.isdigit():
            features.append('segment_[0-9]_' + str(index) + ':1')
        if re.match(r'\D+\d+\D*', segment):
            features.append('segment_substr[0-9]_' + str(index) + ':1')
            if ext:
                features.append('segment_ext_substr[0-9]_' + str(index) + ':' + ext)
        if ext:
            features.append('segment_ext_' + str(index) + ':' + ext)
        index += 1
    features.append("segments:" + str(index))

    return features


def extract_features(qlinks, uknown_urls):
    features = {}
    urls = qlinks + uknown_urls

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

    return map(lambda i: i[0], filter(lambda i: i[1] > 100, features.iteritems()))
