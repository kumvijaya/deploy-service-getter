def confluenceBaseUrl = 'https://vijaik.atlassian.net/wiki'
def confluencePageId = '2523141'  // '33141' for test
def appTableIndex = 16
def columnApp = 'Applications'
def columnService = 'ServiceName'
def appName = 'RMI Platform'
def confluenceApiUrl = "${confluenceBaseUrl}/rest/api/content/${confluencePageId}?expand=body.storage"

node () {
    stage('Deploy Services') {
        checkout scm
        withCredentials([usernamePassword(credentialsId: 'CONFLUENCE_CRED', usernameVariable: 'CONFLUENCE_USERNAME', passwordVariable: 'CONFLUENCE_APITOKEN')]) {
            sh "python -m pip install -r requirements.txt --user"
            def serviceGetterCmd = "python service-getter.py --url '$confluenceApiUrl' --table_index ${appTableIndex} --column_app '$columnApp' --column_service '$columnService' --appname '$appName'"
            def status = sh(script: serviceGetterCmd, returnStatus: true)
            if (status == 0) {
                def servicesInfo = readJSON file: "output.json"
                echo "Service getter output (Map): ${servicesInfo}"
            }else {
                error "Failed to get services list from confluece page"
            }
        }
    }
}


