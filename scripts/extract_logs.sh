#!/bin/bash

LOG_FILE="data/test_secure.log"
OUTPUT_FILE="data/failed_logins.log"

mkdir -p data

grep "Failed password" $LOG_FILE > $OUTPUT_FILE

echo "Extraction completed! Log used: $LOG_FILE"

