import requests
from bs4 import BeautifulSoup

def extract_job(job_container):
  job_box = job_container.find("a", recursive=False)
  title = job_box.find("span", {"class": "title"}).get_text(strip=True)
  company = job_box.find("span", {"class": "company"}).get_text(strip=True)
  link = "https://weworkremotely.com/" + job_box.get("href")
  job = {"title": title, "company": company, "link": link}
  return job


def extract_jobs(url):
  jobs = []
  result = requests.get(url)
  soup = BeautifulSoup(result.text, 'html.parser')
  sections = soup.find_all("section", {"class": "jobs"})
  for section in sections:
    job_containers = section.find_all(["li", {"class": "feature"},"li", {"class": ""}])
    job_containers = job_containers[:-1]
    for job_container in job_containers:
      job = extract_job(job_container)
      jobs.append(job)
  return jobs


def get_jobs(term):
  url = f"https://weworkremotely.com/remote-jobs/search?term={term}"
  jobs = extract_jobs(url)
  return jobs