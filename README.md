# Getting service names from confluence page

## Setup Jenkins credentials for confluence connection
- Type: UserNamePassword
- Username: {{confluence user email}}
- Password: {{confluence api token}}
- ID: CONFLUENCE_CRED

## Update Jenkinsfile with confluence url and page id.
Update below variables in *Jenkinsfile* as per the confluence page where services list exists.

```
def confluenceBaseUrl = 'https://vijaik.atlassian.net/wiki'
def confluencePageId = '33141'
```

## Create Jenkins job and Test
Create pipeline job using *Jenkinsfile* of this repo

Execute the job
It should print the services list as Json and Map

![jenkins-job-listing-services](https://github.com/kumvijaya/deploy-service-getter/blob/main/images/jenkins-job-listing-services.png)

