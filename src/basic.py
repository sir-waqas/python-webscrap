from bs4 import BeautifulSoup
import requests
import pandas as pd 

# url = "https://10pearls.com"
# url = "https://boston.craigslist.org/search/sof"
# response = requests.get(url)
# print(response)
# data = response.text
# # print(data)
# soup = BeautifulSoup(data, 'html.parser')
# print(soup)

# Extracting tags
# tags = soup.find_all('a')
# for tag in tags:
#     print(tag.get('href'))

# # Extracting titles
# titles = soup.find_all('a', {'class': 'result-title'})
# # titles = soup.find_all('h2')
# for title in titles:
#     print(title.text)

# #  Extracting Addresses
# addresses = soup.find_all('span', {'class': 'result-hood'})
# for address in addresses:
#     print(address.text)

# Extracting jobs super tag and find something while nesting into it
npo_jobs = {}
job_no = 0
url = "https://boston.craigslist.org/search/sof"
while True:
    response = requests.get(url)
    print(response)
    data = response.text
    # print(data)
    soup = BeautifulSoup(data, 'html.parser')

    jobs = soup.find_all('p', {'class': 'result-info'})

    for job in jobs:
        title = job.find('a', {'class': 'result-title'}).text
        location_tag = job.find('span', {'class': 'result-hood'})
        location = location_tag.text[2:-1] if location_tag else 'N/A'
        date = job.find('time', {'class': 'result-date'}).text
        link = job.find('a', {'class': 'result-title'}).get('href')
        job_response = requests.get(link)
        job_data = job_response.text
        job_soup = BeautifulSoup(job_data, 'html.parser')
        job_description = job_soup.find('section',{'id':'postingbody'}).text
        job_attibutes_tag = job_soup.find('p', {'class': 'attrgroup'})
        job_attibutes = job_attibutes_tag.text if job_attibutes_tag else 'N/A'
        job_no += 1
        npo_jobs[job_no] = [title, location, date , link, job_attibutes, job_description]
        # print('\nJob Title: ', title, '\nLocation: ', location, '\nDate: ', date, '\nLink: ', link, '\nJobAttributes: ', job_attibutes, '\nJobDescription: ', job_description)

    url_tag = soup.find('a', {'title':'next page'})
    if url_tag.get('href'):
        url = 'https://'+url_tag.get('href')
        print(url)
    else:
        break

print('Total Number of Jobs Extracted: ', job_no)
npo_jobs_df = pd.DataFrame.from_dict(npo_jobs, orient= 'index', columns= ['Job Title', 'Location', 'Date', 'Link', 'Job Attributes', 'Job Description'])
print(npo_jobs_df.head())