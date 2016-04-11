package:
	buildid -n
	ls -alh
	zip -r upsilon-pycommon-$(shell buildid -k tag).zip .buildid src/*.py pkg

.PHONY: package
