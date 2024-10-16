import requests #enable HTTP requests
from bs4 import BeautifulSoup #to parse HTML content

#function to scrape a page on web3.career
def scrape_webpage(page):
    #fetch the HTML content of the page using requests
    r = requests.get(f"https://web3.career/remote-jobs?page={page}")

    #parse the fetched HTML content using BeautifulSoup
    webpage = BeautifulSoup(r.text, "html.parser")

    #find the section of the HTML that contains the jobs table
    table_section = webpage.find("tbody", {"class": "tbody"})

    #initialize an empty string to store job data
    jobs_data = ""

    #loop through each row in the jobs table
    for i in table_section.find_all("tr"):
        try:
            # Extract the job role text from the <h2> tag
            role = i.h2.text.strip()

            # Extract the company name from the <h3> tag
            company = i.h3.text.strip()
            
            # Extract the salary information from the <p> tag
            salary = i.p.text.strip()
            
            # Extract the job link by accessing the 'href' attribute of the <a> tag
            # Modify the link to form a full URL
            link = f"https://web3.career/{i.a['href'][3:]}"
            
            # Append the extracted job data (role, company, salary, link) to jobs_data string
            jobs_data += f"{role},{company},{salary},{link}\n"
        except:
            pass
    
    return jobs_data

#initialize the CSV header
jobs_data = "role,company,salary,link\n"

for i in range(1, 20):       
    print("Scraping page", i)
    # Scrape the current page and append the returned job data to jobs_data
    jobs_data += scrape_webpage(i)

# Write the scraped jobs data into CSV file
open("jobs.csv", "w").write(jobs_data)