#!/usr/bin/env bash

pyinstaller -y specs/gui.spec
cd dist
if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    tar cjvf 'Solar Sails.app.tar.bz2' 'Solar Sails.app'
else
    tar cjvf solar-sails-linux-x64.tar.bz2 solar-sails
fi
