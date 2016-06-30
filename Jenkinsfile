#!groovy

node {
	stage "build"
	checkout scm
	sh "./make.sh"

	archive 'pkg/*.zip'

	for (Run.Artifact artifact : currentBuild.rawBuild.getArtifacts()) {
		String artifactPath = artifact.getHref()
	}
}
