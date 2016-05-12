package:
	buildid -n
	zip -r bin/upsilon-pycommon-$(shell buildid -k tag).zip .buildid src/*.py pkg

.PHONY: package
