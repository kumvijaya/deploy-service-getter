# Getting servcie names from confluence page

## Set up Jenkins credentials
- Type: UserNamePassword
- Username: <<confluce user email>>
- Password: <<conflunce api_token>>
- ID: CONFLUENCE_CRED

## Update Jenkinsfile
Update below variables in *Jenkinsfile* as per the confluence page where services list exists.

```
def confluenceBaseUrl = 'https://vijaik.atlassian.net/wiki'
def confluencePageId = '33141'
```

## Create Jenkins job and Test
Create pipeline job using *Jenkinsfile* of this repo

Execute the job
It should print the services list as Json and map

![jenkins-job-listing-services](https://github.com/kumvijaya/deploy-service-getter/blob/main/images/jenkins-job-listing-services.png)

