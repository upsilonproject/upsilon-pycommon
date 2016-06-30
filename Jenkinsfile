#!groovy

node {
	stage "build"
	checkout scm
	sh "./make.sh"

	archive 'pkg/*.zip'

	for (Object artifact : currentBuild.rawBuild.getArtifacts()) {
		String artifact = artifact.toString()
		sh "curl -X POST -d @${artifact} http://ci.teratan.net/repositories/upload.php"
	}
}
