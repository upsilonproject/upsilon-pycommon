package:
	buildid -n
	zip -r upsilon-pycommon-$(shell buildid -k tag).zip .buildid src/*.py pkg

.PHONY: package
