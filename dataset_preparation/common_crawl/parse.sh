#!/bin/bash
export $(cat ../../.env | xargs)

warc_url=$(sed -n $1p "${DATASETS_PATH}/common_crawl/warc.paths")
warc_url="https://data.commoncrawl.org/${warc_url}"
warc_name=$(basename ${warc_url})
warc_path="${DATASETS_PATH}/common_crawl/warc/${warc_name}"
res_path="${DATASETS_PATH}/common_crawl/parsed/${warc_name%%.*}.json"

wget ${warc_url} -O ${warc_path} --quiet
python3 parse.py --warc-path ${warc_path} --res-path ${res_path}
rm ${warc_path}



