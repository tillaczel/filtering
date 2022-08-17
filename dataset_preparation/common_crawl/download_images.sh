#!/bin/bash
export $(cat ../../.env | xargs)

warc_url=$(sed -n $1p "${DATASETS_PATH}/common_crawl/warc.paths")
warc_name=$(basename ${warc_url})

parsed_json_path="${DATASETS_PATH}/common_crawl/parsed/${warc_name%%.*}.json"
h5_path="${DATASETS_PATH}/common_crawl/images/$1.h5"
annotation_path="${DATASETS_PATH}/common_crawl/text/$1.json"

python3 download_images.py --parsed-json-path ${parsed_json_path} --h5-path ${h5_path} --annotation-path ${annotation_path}
