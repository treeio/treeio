#!/usr/bin/env bash
sudo yum install mercurial
# pillow dependencies
sudo yum install libtiff-devel libjpeg-devel libzip-devel freetype-devel lcms2-devel libwebp-devel tcl-devel tk-devel
python --version
pip install -r requirements.txt