import requests
from bs4 import BeautifulSoup
import json
import argparse
import os

#Get confluence url and application name
argparser = argparse.ArgumentParser(prog='service-getter',
                                    description='To read table content from confluence page and providing output to jenkins pipeline')
argparser.add_argument('-u', '--url', type=str, metavar='', required=True, help='url to access confluence page')
argparser.add_argument('-t', '--table_index', type=str, metavar='', required=True, help='Table index to read from confluence page')
argparser.add_argument('-p', '--column_app', type=str, metavar='', required=True, help='Table application header name to read from confluence page')
argparser.add_argument('-s', '--column_service', type=str, metavar='', required=True, help='Table service name header to read from confluence page')
argparser.add_argument('-a', '--appname', type=str, metavar='', required=True, help='Application name')

args = argparser.parse_args()
confluence_rest_api = args.url
table_index = args.table_index
column_app = args.column_app
column_service = args.column_service
application_name = args.appname

# Confluence Username and Apitoken
username = os.environ["CONFLUENCE_USERNAME"]
confluence_apitoken = os.environ["CONFLUENCE_APITOKEN"]

def get_confluence_page_html(username, confluence_token):
    """Get the confluence page to read the table data.

    Args:
        username (str) : email id
        confluence_apitoken (str) : confluence api token
        
    Returns:
        page_body : confluence page body where table resides
    """
    params = {"expand": "body.view"}
    auth = (username, confluence_token)
    response = requests.get(confluence_rest_api, params=params, auth=auth)
    page_data = None
    if response.status_code == 200:
        page_data = get_page_data(response)
    else:
        print(f"Failed to retrieve Confluence page. Status code: {response.status_code}")
    return page_data

def get_page_data(response):
    data = response.json()
    storage_content = data.get("body", {}).get("storage", {}).get("value", "")
    page_body = decode_confluence_storage(storage_content)
    return page_body

def decode_confluence_storage(storage_content):
    """Get the decode confluence storage data.

    Args:
        storage_content (str) :html parser
          
    Returns:
        soup : decode html parser confluence storage.
    """
    soup = BeautifulSoup(storage_content, "html.parser")
    return str(soup)

def extract_table_data(html_content):
    """Get the table data.

    Args:
        html_content (str) : content of html
          
    Returns:
        table_data : Extract table data as a list.
    """  
    soup = BeautifulSoup(html_content, "html.parser")
    tables = soup.find_all("table")
    table = None
    index = int(table_index)
    if index < len(tables):
        table = tables[index]
    table_data = None
    if table:
        table_data = get_table_data(table)
    else:
        print("No table found on the Confluence page.")
    return table_data
    
def get_table_data(table):
    table_data = []
    header = [th.get_text(strip=True) for th in table.find_all('th')]
    for row in table.find_all('tr')[1:]:
        row_data = [str(td) for td in row.find_all(['td', 'th'])]
        table_data.append(dict(zip(header, row_data)))
    return table_data

def clean_text(text):
    """Remove HTML tags and additional characters
  
    Returns:
        Data with no paragraphs, line breaks, and additional HTML tags
    """    
    # Remove HTML tags
    cleaned_text = BeautifulSoup(text, 'html.parser').get_text(separator=' ')
    # Remove additional characters
    cleaned_text = cleaned_text.replace('<br/>', '').replace('<p>', '').replace('</p>', '').replace('</td>', '').strip()
    return cleaned_text


def find_app_service_info(table_data, target_application_name, applications_key, service_name_key):
    """Get the service name from confluence page table

    Args:
        table_data (list): List of dictionaries representing the table data from confluence
        target_application_name (str): The name of the application to search for
        applications_key (str): Key for the 'Applications' column in the table_data
        service_name_key (str): Key for the 'ServiceName' column in the table_data

    Returns:
        dict: A dictionary containing the application name as key and the corresponding service names as value
    """
    app_service_map = {}
    for row in table_data:
        application_name = get_application_name_from_row(applications_key, target_application_name, row)
        if application_name and service_name_key in row:
            service_data = get_service_data_from_html(service_name_key, row)
            app_service_map[application_name] = service_data
    return app_service_map

def get_application_name_from_row(applications_key, target_application_name, row):
    application_name = None
    if applications_key in row:
        application_name = row[applications_key]
        if target_application_name.lower() in application_name.lower():
            application_name = clean_text(application_name)
    return application_name

def get_service_data_from_html(service_name_key, row):
    service_name_data = row[service_name_key]
    service_names = [item.split(':') for item in service_name_data.split('<p>') if ':' in item]
    service_data = {name.strip(): clean_text(value) for name, value in service_names if len(name) > 0 and len(value) > 0}
    return service_data

def write_service_output(service_names):
    with open('output.json', 'w') as f:
        json.dump(service_names, f)

def get_updated_service_job(service_map, version):
    updated_service_map = {}
    updated_service_map['job'] = service_map['job']
    params = service_map['parameters']
    updated_params = {}
    for key, value in params.items():
        updated_params[key] = value.replace('{{VERSION}}', version)
    updated_service_map['parameters'] = updated_params
    return updated_service_map

def get_service_jobs_config():
    json_file_path = 'service-job-mapping.json'
    with open(json_file_path, 'r') as file:
        service_mapping = json.load(file)
    return service_mapping

def write_jobs_json(updated_service_jobs):
    updated_json_content = json.dumps(updated_service_jobs, indent=2)
    print(updated_json_content)
    with open('jobs.json', 'w') as updated_file:
        updated_file.write(updated_json_content)

def get_updated_service_jobs(service_jobs_config, app_service_info):
    updated_service_jobs = []
    for service_name, version in app_service_info.items():
        if service_name in service_jobs_config:
            service_job = service_jobs_config[service_name]
            updated_service_jobs.append(get_updated_service_job(service_job, version))
    return updated_service_jobs

def populate_jobs_info(services_info):
    write_service_output(services_info)
    service_jobs_config = get_service_jobs_config()
    app_service_info = services_info[application_name]
    updated_service_jobs = get_updated_service_jobs(service_jobs_config, app_service_info)
    write_jobs_json(updated_service_jobs)

html_content = get_confluence_page_html(username, confluence_apitoken)
if html_content:
    table_data = extract_table_data(html_content)
    if table_data:
        app_services_info = find_app_service_info(table_data, application_name, column_app, column_service) 
        if app_services_info:
            populate_jobs_info(app_services_info)
        else:
            print(f"Applications / Service names not found ")