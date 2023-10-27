#!/bin/bash

cd "$(dirname "$0")"
/usr/bin/uvicorn main:app --host=0.0.0.0 --workers=4 