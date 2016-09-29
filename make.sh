#!/bin/bash
rm -rf pkg
mkdir -p pkg

buildid -n
buildid -qf rpmmacro -W .upsilon-pycommon.rpmmacro
zip -r pkg/upsilon-pycommon-$(buildid -k tag).zip .buildid src/*.py pkg var .upsilon-pycommon.rpmmacro
