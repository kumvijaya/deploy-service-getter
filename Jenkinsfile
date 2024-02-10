def confluenceBaseUrl = 'https://vijaik.atlassian.net/wiki'
def confluencePageId = '2523141' 
def table_index = 16
// '33141'
def appName = 'RMI Platform'
def confluenceApiUrl = "${confluenceBaseUrl}/rest/api/content/${confluencePageId}?expand=body.storage"

node () {
    stage('Deploy Services') {
        checkout scm
        withCredentials([usernamePassword(credentialsId: 'CONFLUENCE_CRED', usernameVariable: 'CONFLUENCE_USERNAME', passwordVariable: 'CONFLUENCE_APITOKEN')]) {
            sh "python -m pip install -r requirements.txt --user"
            def serviceGetterCmd = "python service-getter.py --url '$confluenceApiUrl' --table_index ${table_index} --appname '$appName'"
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
