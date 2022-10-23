import boto3
import pandas
import os
from bs4 import BeautifulSoup

Akey = "AKIAQUFB6MCD72Y42XGL";
SKey = "Dk59+KFmqlVuAFQERYU7lzEG96kPhsT7QLwbAl9D";
rName = "us-east-2";

client = boto3.client(
    's3',
    aws_access_key_id = Akey,
    aws_secret_access_key = SKey,
    region_name = rName
)
    
# Creating the high level object oriented interface
resource = boto3.resource(
    's3',
    aws_access_key_id = Akey,
    aws_secret_access_key = SKey,
    region_name = rName
)

# Fetch the list of existing buckets
clientResponse = client.list_buckets()
    
# Print the bucket names one by one
print('Printing bucket names...')
for bucket in clientResponse['Buckets']:
    print(f'Bucket Name: {bucket["Name"]}')


obj = client.get_object(
    Bucket = 'health-on-track-storage-af0d1995234445-staging',
    Key = 'users-rest-api.xml'
)

# Read data from the S3 object
data = pandas.read_xml(obj['Body'])
    
# Print the data frame
print('Printing the data frame...')
print(data)
print(data.iloc[1]['name'])

# Open test.html for reading
print(os.getcwd())
with open('index.html') as html_file:
    soup = BeautifulSoup(html_file.read(), features='html.parser')

    # Go through each 'A' tag and replace text with '-'
    for tag in soup.find_all(id='greeting'):
        tag.string.replace_with(data.iloc[1]['name'])

    # Store prettified version of modified html
    new_text = soup.prettify()

# Write new contents to test.html
with open('test.html', mode='w') as new_html_file:
    new_html_file.write(new_text)