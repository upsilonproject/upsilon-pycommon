#!/bin/bash
rm -rf pkg
mkdir -p pkg

buildid -n
zip -r pkg/upsilon-pycommon-$(buildid -k tag).zip .buildid src/*.py pkg
