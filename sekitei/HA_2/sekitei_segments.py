from sklearn import cluster
import numpy as np
import extract_features

sekitei = None
quotas = None
n_features = 0
features = []


def update_data(features, own_features, data):
    for i, feature in enumerate(features):
        if feature in own_features:
            data[i] = 1


def define_segments(QLINK_URLS, UNKNOWN_URLS, QUOTA):
    urls = QLINK_URLS + UNKNOWN_URLS
    global features, n_features, quotas, sekitei
    features = list(extract_features.extract_features(QLINK_URLS, UNKNOWN_URLS))
    n_features = len(features)
    data = np.zeros((len(urls), n_features))
    for i, url in enumerate(urls):
        update_data(features, extract_features.extract_all_features_from_url(url), data[i, :])

    bandwidth = cluster.estimate_bandwidth(data, quantile=0.14)
    sekitei = cluster.MeanShift(bandwidth=bandwidth)
    labels = sekitei.fit_predict(data)
    quotas = np.zeros(max(set(labels)) + 1)
    for i, url in enumerate(urls):
        if url in QLINK_URLS:
            quotas[labels[i]] += 1
    quotas /= len(QLINK_URLS)
    quotas *= QUOTA


#
# returns True if need to fetch url
#
def fetch_url(url):
    global features, n_features, quotas, sekitei
    data = np.zeros(n_features)
    update_data(features, extract_features.extract_all_features_from_url(url), data)
    cluster = sekitei.predict(data.reshape(1, -1))
    if quotas[cluster] > 1:
        quotas[cluster] -= 1
        return True
    else:
        return False


