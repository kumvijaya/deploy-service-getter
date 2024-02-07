node {
    def confApiUrl = 'https://vijaik.atlassian.net/wiki/rest/api/content/33141?expand=body.storage'
    def appName = 'RMI Platform'

    stage('Deploy Services') {
        checkout scm

        withCredentials([usernamePassword(credentialsId: 'CONFLUENCE_CRED', usernameVariable: 'CONFLUENCE_USERNAME', passwordVariable: 'CONFLUENCE_APITOKEN')]) {
            script {
                sh "python -m pip install -r requirements.txt --user"
                def serviceGetterCmd = "python service-getter.py --url '$confApiUrl' --appname '$appName'"
                def status = sh(script: serviceGetterCmd, returnStatus: true)
                if (status == 0) {
                    // def servicesInfo = readJSON file: "output.json"
                    def servicesInfo = readFile "output.json"
                    echo "Service getter output: ${servicesInfo}"
                }else {
                    error "Failed to get services info"
                }
            }
        }
    }
}
