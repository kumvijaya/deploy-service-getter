# Getting service names from confluence page

## Setup Jenkins credentials for confluence connection
- Type: UserNamePassword
- Username: {{confluence user email}}
- Password: {{confluence api token}}
- ID: CONFLUENCE_CRED

Note: 
- **Username**: Confluence user name
- **Password**: Confluence personal access token. Refer creating [confluence personal access token](https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html)

## Update Jenkinsfile with confluence url and page id.
Update below variables in *Jenkinsfile* as per the confluence page where services list exists.

```
def confluenceBaseUrl = 'https://vijaik.atlassian.net/wiki'
def confluencePageId = '33141'
def appTableIndex = 16
```
- **confluenceBaseUrl**: Provide the base url parent path where the required page resides.

- **confluencePageId**: Refer viewing [confluence page id](https://confluence.atlassian.com/confkb/how-to-get-confluence-page-id-648380445.html)

- **appTableIndex**: Provide the table index to get application services. Currently the required table *PROD - Openshift Deployments* present as 16 th table (Starts with index 0).

## Create Jenkins job and Test
Create pipeline job using *Jenkinsfile* of this repo

Execute the job
It should print the services list as Json and Map

![jenkins-job-listing-services](https://github.com/kumvijaya/deploy-service-getter/blob/main/images/jenkins-job-listing-services.png)

