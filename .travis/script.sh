#!/usr/bin/env bash

VERSION="$(python -c 'import sails; print(sails.build_number())')"
echo ${VERSION} > solar-sails-version.txt
pyinstaller -y specs/gui.spec
cd dist
if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    mv 'Solar Sails.app' "Solar Sails ${VERSION}.app"
    tar cjvf 'Solar Sails.app.tar.bz2' "Solar Sails ${VERSION}.app"
else
    mv solar-sails solar-sails-${VERSION}
    tar cjvf solar-sails-linux-x64.tar.bz2 solar-sails-${VERSION}
fi
