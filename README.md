# Getting servcie names from confluence page

## Set up jenkins credentials

ID: CONFLUENCE_CRED

Username: <<email_id>>

Password: <<conflunce_api_token>>

## To execute service getter script
python service-getter.py --url "<<confluence_api_url>>"  --appname "<<application_name>>"

Example
```
python service-getter.py --url 'https://vijaik.atlassian.net/wiki/rest/api/content/33141?expand=body.storage' --appname 'RMI Platform'
```

