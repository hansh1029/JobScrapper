import requests
from bs4 import BeautifulSoup

def get_last_page(url):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, 'html.parser')
  pages = soup.find_all("a", {"class": "s-pagination--item"})
  last_page = int(pages[-2].get_text(strip=True))
  return last_page

def extract_job(job_container):
  title = job_container.find("a", {"class": "s-link"}).get("title")
  company = job_container.find("h3", {"class": "fc-black-700 fs-body1 mb4"}).find("span").get_text(strip=True)
  link = "https://stackoverflow.com" + job_container.find("a", {"class": "s-link"}).get("href")
  job = {"title": title, "company": company, "link": link}
  return job


def extract_jobs(url, last_page):
  jobs = []
  for page in range(last_page):
    url = f"{url}&pg={page+1}"
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    job_containers = soup.find_all("div", {"class": "-job"})
    for job_container in job_containers:
      job = extract_job(job_container)
      jobs.append(job)
  return jobs


def get_jobs(term):
  url = f"https://stackoverflow.com/jobs?r=true&q={term}"
  last_page = get_last_page(url)
  jobs = extract_jobs(url, last_page)
  return jobs