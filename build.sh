# /usr/bin/bash

rm -rf ./dist
python -m nuitka --standalone --plugin-enable=pyside6 --macos-create-app-bundle --output-dir=dist --output-filename=JonSnowIptvPlayer.app src/jsip.py
