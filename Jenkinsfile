#!groovy

node {
	stage "build"
	checkout scm
	sh "./make.sh"

	archive 'pkg/*.zip'

	for (Object artifact : currentBuild.rawBuild.getArtifacts()) {
		println "pkg: ${artifact}"
	}
}
