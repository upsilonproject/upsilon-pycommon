node {
	stage "build"
	checkout scm
	sh "./make.sh"

	archive 'pkg/*.zip'

	for (Object artitact : currentBuild.rawBuild.getArtifacts()) {
		println "pkg: ${artifact}"
	}
}
