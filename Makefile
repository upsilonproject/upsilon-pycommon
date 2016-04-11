package:
	buildid -n
	zip -r upsilon-pycommon-$(shell buildid -k tag).zip src/*.py pkg

.PHONY: package
