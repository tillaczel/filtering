from warcio.archiveiterator import ArchiveIterator
from bs4 import BeautifulSoup as BS
import gzip
import json
import argparse
import os


def main(warc_path, res_path):
    data = dict()
    with gzip.open(warc_path, 'rb') as stream:
        for record in ArchiveIterator(stream):
            if record.rec_type == 'response':
                try:
                    soup = BS(record.content_stream().read().decode('UTF-8'), "html.parser")
                except UnicodeDecodeError:
                    continue
                for imgtag in soup.find_all('img'):
                    if imgtag.get('src', None) is None or imgtag.get('alt', None) is None:
                        continue
                    if imgtag['src'] in data or len(imgtag['alt']) < 5:
                        continue
                    data[imgtag['src']] = imgtag['alt']
                    if len(data) % 10000 == 0:
                        print(os.path.basename(warc_path), len(data))
    print(f'Saving results to {res_path}')
    with open(res_path, "w") as fp:
        json.dump(data, fp)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--warc-path', type=str, required=True)
    parser.add_argument('--res-path', type=str, required=True)
    args = parser.parse_args()

    main(args.warc_path, args.res_path)
