#!/bin/bash
rm -rf pkg
mkdir -p pkg

buildid -n
buildid -qf rpmmacro -W .upsilon-pycommon.rpmmacro

BUILD_DIR=upsilon-pycommon-`buildid -k tag`
mkdir -p $BUILD_DIR
cp -r .buildid src pkg var .upsilon-pycommon.rpmmacro $BUILD_DIR/

zip -r pkg/upsilon-pycommon.zip $BUILD_DIR/

rm -rf $BUILD_DIR
