import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?as_and=python&limit={LIMIT}"

def extract_indeed_pages():
  indeed_result = requests.get(URL)

  indeed_soup = BeautifulSoup(indeed_result.text,"html.parser")

  pagination = indeed_soup.find("div", {"class":"pagination"})

  links = pagination.find_all('a')
  pages = []

  for link in links[:-1]:
    pages.append(int(link.string))

  max_page = pages[-1]

  return max_page


def extract_indeed_jobs(last_page):
  jobs = []
  #for page in range(last_page):
  result = requests.get(f"{URL}&start={0*LIMIT}")
  soup = BeautifulSoup(result.text, "html.parser")
  results = soup.find_all("div", {"class":"job_seen_beacon"})
  
  for result in results:
    
    title = ""
    try:
      title = result.find("h2", {"class": "jobTitle"}).find("span")["title"]
    except:
      continue
    
    company = result.find("span", {"class": "companyName"}).string

    location = result.select_one("pre > div").text
    #find("div", {"class": "companyLocation"}).string

    jobs.append({"title":title, "company":company, "location":location})

  return jobs