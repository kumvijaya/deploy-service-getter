def confluenceBaseUrl = 'https://vijaik.atlassian.net/wiki'
def confluencePageId = '2523141'
def appTableIndex = 16
def columnApp = 'Applications'
def columnService = 'ServiceName'
def appName = 'RMI Platform'
def confluenceApiUrl = "${confluenceBaseUrl}/rest/api/content/${confluencePageId}?expand=body.storage"

node () {
    stage('Deploy Services') {
        checkout scm
        withCredentials([usernamePassword(credentialsId: 'CONFLUENCE_CRED', usernameVariable: 'CONFLUENCE_USERNAME', passwordVariable: 'CONFLUENCE_APITOKEN')]) {
            def jobsInfo = getJobsFromConfluence(confluenceApiUrl, appTableIndex, columnApp, columnService, appName)
            if(jobsInfo) {
                executeJobs(jobsInfo)
            } else {
                error "No jobs to execute. Exiting pipeline"
            }           
        }
    }
}

def executeJobs(jobsInfo) {
    Map jobs = getJobDefinitions(jobsInfo)
    parallel(jobs)
}

def getJobsFromConfluence(confluenceApiUrl, appTableIndex, columnApp, columnService, appName) {
    sh "python -m pip install -r requirements.txt --user"
    def serviceGetterCmd = "python service-getter.py --url '$confluenceApiUrl' --table_index ${appTableIndex} --column_app '$columnApp' --column_service '$columnService' --appname '$appName'"
    def status = sh(script: serviceGetterCmd, returnStatus: true)
    def jobsInfo
    if (status == 0) {
        jobsInfo = readJSON file: "jobs.json"
    }else {
        error "Failed to get services list from confluece page"
    }
}

def getJobDefinitions(jobsInfo) {
    Map jobs = [:]
    for(jobInfo in jobsInfo) {
        String jobName = jobInfo.job
        echo "Job: ${jobName}"
        if(!jobs.containsKey(jobName)) {
            echo "Adding job: ${jobName}"
            def jobDef = getJobDefinition(jobName, jobInfo.parameters)
            jobs.put(jobName, jobDef)
        }
    }
    return jobs
}

def getJobDefinition(jobName, parameters) {
    return {
        stage(jobName) {
            build(job: jobName, parameters: getJobParamters(parameters), propagate: false)
        }
    }
}

def getJobParamters(parameters) {
   def jobParameters = []
   for (entry in parameters) {
        jobParameters.add(new StringParameterValue(entry.key, entry.value))
   }
   return jobParameters
}
