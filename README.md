# Master job for service deployments

## Setup Jenkins credentials for confluence connection
- Type: UserNamePassword
- Username: {{confluence user email}}
- Password: {{confluence api token}}
- ID: CONFLUENCE_CRED

Note: 
- **Username**: Confluence user name
- **Password**: Confluence personal access token. Refer creating [confluence personal access token](https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html)

## Configure Service Job Mapping Json 

Mapping json file **service-job-mapping.json** should be updated the job names and parameters key-vals for each service name.
Also for the parameters that takes the version, put the place holder string "**{{VERSION}}**".
Note: The version place holder will be replaced as the service version fetched from the confluence page.

Replace job names and required parameters accordingly.

[service-job-mapping.json](https://github.com/kumvijaya/deploy-service-getter/blob/main/service-job-mapping.json)

## Update Jenkinsfile with confluence url and page id.
Update below variables in *Jenkinsfile* as per the confluence page where services list exists.

```
def confluenceBaseUrl = 'https://vijaik.atlassian.net/wiki'
def confluencePageId = '33141'
def appTableIndex = 16
def columnApp = 'Applications'
def columnService = 'ServiceName'
def appName = 'RMI Platform'
```
- **confluenceBaseUrl**: Provide the base confluence url where the required page resides. Need to update this field with right url.

- **confluencePageId**: Refer viewing [confluence page id](https://confluence.atlassian.com/confkb/how-to-get-confluence-page-id-648380445.html). Need to update this field with right page id.

- **appTableIndex**: Provide the table index to get application services. Currently the required table *PROD - Openshift Deployments* present as 16 th table (Starts with index 0).

- **columnApp**: Provide applications column name in the table (Default - 'Applications').

- **columnService**: Provide services column name in the table (Default - 'ServiceName').

- **appName**: Provide application name to look for in the table rows (Default - 'RMI Platform').

## Create Jenkins job and Test
Create master job using *Jenkinsfile* of this repo. This will work as master job.

Execute this master job.

It should print the services list as Json and Map. All the services are executed separately as per Mapping Json File.
Version in the Mapping file will be updated with the service version given in confluence page.

![jenkins-job-listing-services](https://github.com/kumvijaya/deploy-service-getter/blob/main/images/jenkins-job-listing-services1.png)
![jenkins-job-listing-services](https://github.com/kumvijaya/deploy-service-getter/blob/main/images/jenkins-job-listing-services2.png)
![jenkins-job-listing-services](https://github.com/kumvijaya/deploy-service-getter/blob/main/images/jenkins-job-listing-services3.png)
![jenkins-job-listing-services](https://github.com/kumvijaya/deploy-service-getter/blob/main/images/jenkins-job-listing-services4.png)

