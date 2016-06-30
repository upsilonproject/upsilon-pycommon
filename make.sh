#!/bin/bash
buildid -n
zip -r bin/upsilon-pycommon-$(buildid -k tag).zip .buildid src/*.py pkg
