#!/bin/bash

for i in {1..10}; do
  bash parse.sh ${i} &
done
