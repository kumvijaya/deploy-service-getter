node {
    def confApiUrl = 'https://vijaik.atlassian.net/wiki/rest/api/content/33141?expand=body.storage'
    def appName = 'RMI Platform'

    stage('Deploy Services') {
        checkout scm

        withCredentials([usernamePassword(credentialsId: 'CONFLUENCE_CRED', usernameVariable: 'CONFLUENCE_USERNAME', passwordVariable: 'CONFLUENCE_APITOKEN')]) {
            script {
                sh "python -m pip install -r requirements.txt --user"
                def serviceGetterCmd = "python service-getter.py --url '$confApiUrl' --appname '$appName'"
                String servicesOutput = sh(script: serviceGetterCmd, returnStdout: true).trim()
                echo "Service list getter output: ${servicesOutput}"
            }
        }
    }
}
