package:
	buildid -n
	zip -r upzilon-pycommon-$(shell buildid -k tag).zip src/*.py

.PHONY: package
