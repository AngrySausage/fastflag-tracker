#!/bin/bash

parent=$(dirname "$0")
libraries_path="$parent/libraries"

if [ ! -d "$libraries_path" ]; then
    mkdir -p "$libraries_path"
fi

pip install --upgrade --target="$libraries_path" requests

read -p "Press [Enter] to continue..."