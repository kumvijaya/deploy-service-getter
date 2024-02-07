node {
    def confApiUrl = 'https://vijaik.atlassian.net/wiki/rest/api/content/33141?expand=body.storage'
    def appName = 'RMI Platform'

    stage('Deploy Services') {
        checkout scm

        withCredentials([usernamePassword(credentialsId: 'CONFLUENCE_CRED', usernameVariable: 'CONFLUENCE_USERNAME', passwordVariable: 'CONFLUENCE_APITOKEN')]) {
            script {
                def serviceInfoCommand = """
                    python -m pip install -r requirements.txt --user
                    python service-getter.py --url "$confApiUrl" --appname "$appName"
                    
                """
                def servicesOutput = sh(script: serviceInfoCommand, returnStdout: true)
                echo "Service list getter output: ${servicesOutput}"
            }
        }
    }
}
