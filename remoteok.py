import requests
from bs4 import BeautifulSoup
import re

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


def not_closed(value):
    return value and not re.compile("closed").search(value)


def extract_job(job_container):
  title = job_container.find("h2", {"itemprop": "title"}).get_text(strip=True)
  company = job_container.find("h3", {"itemprop": "name"}).get_text(strip=True)
  link = "https://remoteok.io" + job_container.get("data-href")
  job = {"title": title, "company": company, "link": link}
  return job


def extract_jobs(url):
  jobs = []
  result = requests.get(url, headers=headers)
  soup = BeautifulSoup(result.text, 'html.parser')
  job_table = soup.find("table")
  job_containers = job_table.find_all("tr", {"class": "job"})
  for job_container in job_containers:
    is_closed = "closed" in job_container.get("class")
    if is_closed:
      continue
    job = extract_job(job_container)
    jobs.append(job)
  return jobs


def get_jobs(term):
  url = f"https://remoteok.io/remote-dev+{term}-jobs"
  jobs = extract_jobs(url)
  return jobs

  

