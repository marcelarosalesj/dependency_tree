#!/bin/bash

repo init -u https://opendev.org/starlingx/manifest -m default.xml
repo sync -j$(nproc)
