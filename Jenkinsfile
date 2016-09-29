#!groovy

properties(                                                                        
    [                                                                              
        [                                                                          
            $class: 'jenkins.model.BuildDiscarderProperty', strategy: [$class: 'LogRotator', numToKeepStr: '10', artifactNumToKeepStr: '10'],
            $class: 'CopyArtifactPermissionProperty', projectNames: '*'            
        ]                                                                          
    ]                                                                              
)       

node {
	stage "build"
	checkout scm
	sh "./make.sh"

	archive 'pkg/*.zip'
	stash includes:"pkg/*.zip", name: "binaries"
}

def prepareEnv() {                                                                 
    unstash 'binaries'                                                             
                                                                                   
    env.WORKSPACE = pwd()                                                          
                                                                                   
    sh "find ${env.WORKSPACE}"                                                     
                                                                                   
    sh 'mkdir -p SPECS SOURCES'                                                    
    sh "cp build/distributions/*.zip SOURCES/upsilon-pycommon.zip"                      
}  

def buildRpm(dist) {                                                               
    deleteDir()                                                                    
                                                                                   
    prepareEnv()                                                                   
                                                                                    
    sh 'unzip -jo SOURCES/upsilon-pycommon.zip "upsilon-pycommon-*/var/pkg/upsilon-pycommon.spec" "upsilon-pycommon-*/.upsilon-pycommon.rpmmacro" -d SPECS/'
    sh "find ${env.WORKSPACE}"                                                     
                                                                                   
    sh "rpmbuild -ba SPECS/upsilon-pycommon.spec --define '_topdir ${env.WORKSPACE}' --define 'dist ${dist}'"
                                                                                   
    archive 'RPMS/noarch/*.rpm'                                                    
}  

node {
	buildRpm("el7")
}

node {
	buildRpm("el6")
}
