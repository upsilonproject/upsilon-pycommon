#!groovy

node {
	stage "build"
	checkout scm
	sh "./make.sh"

	archive 'pkg/*.zip'

	for (Object artifact : currentBuild.rawBuild.getArtifacts()) {
		String artifactPath = artifact.toString()
		sh "curl -X POST -d @${artifactPath} http://ci.teratan.net/repositories/upload.php"
	}
}
