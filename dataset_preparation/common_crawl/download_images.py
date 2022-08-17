import json
import argparse
from PIL import Image, UnidentifiedImageError
import requests
from requests.exceptions import MissingSchema, InvalidSchema, ConnectionError, TooManyRedirects, ContentDecodingError, \
    ReadTimeout
from io import BytesIO
import h5py
from joblib import Parallel, delayed


def get_img(url):
    try:
        response = requests.get(url, timeout=10)
    except (MissingSchema, InvalidSchema, ConnectionError, TooManyRedirects, ContentDecodingError, ReadTimeout) as e:
        return None
    if response.status_code != 200:
        return None
    try:
        return Image.open(BytesIO(response.content))
    except:# (UnidentifiedImageError, OSError) as e:
        return None


def main(parsed_json_path, h5_path, annotation_path):
    with open(parsed_json_path, "r") as f:
        data = json.load(f)

    results = Parallel(n_jobs=256, verbose=1)(delayed(get_img)(url) for url in list(data.keys()))

    text = dict()
    idx = 0
    for url, img in zip(data.keys(), results):
        if img is None:
            continue
        with h5py.File(h5_path, 'a') as hf:
            hf[str(idx)] = img
            text[str(idx)] = data[url]
            idx += 1
    print(f'Saving results to {annotation_path}')
    with open(annotation_path, "w") as fp:
        json.dump(text, fp)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--parsed-json-path', type=str, required=True)
    parser.add_argument('--h5-path', type=str, required=True)
    parser.add_argument('--annotation-path', type=str, required=True)
    args = parser.parse_args()

    main(args.parsed_json_path, args.h5_path, args.annotation_path)
