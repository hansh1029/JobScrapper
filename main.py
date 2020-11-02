from flask import Flask, render_template, request, redirect, send_file
from so import get_jobs as get_jobs_so
from wework import get_jobs as get_jobs_wework
from remoteok import get_jobs as get_jobs_remoteok
from exporter import save_to_file

"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""

app = Flask("RemoteJobScrapper")

db = {}

def get_jobs(term):
  jobs_so = get_jobs_so(term)
  jobs_wework = get_jobs_wework(term)
  jobs_remoteok = get_jobs_remoteok(term)
  jobs = jobs_so + jobs_wework + jobs_remoteok
  return jobs

@app.route('/')
def home():
  return render_template("home.html")

@app.route('/report')
def report():
  term = request.args.get("term")
  term = term.lower()
  if term:
    term = term.lower()
    existingJobs = db.get(term)
    if existingJobs:
        jobs = existingJobs
    else:
        jobs = get_jobs(term)
        db[term] = jobs
  else:
    return redirect("/")
  jobs_num = len(jobs)
  return render_template("report.html", jobs=jobs, jobs_num=jobs_num, term=term)

@app.route('/export')
def export():
  try:
    term = request.args.get("term")
    if not term:
      raise Exception()
    term = term.lower()
    jobs = db.get(term)
    if not jobs:
      raise Exception()
    save_to_file(jobs, term)
    result = send_file(f"{term}.csv", mimetype='application/x-csv', as_attachment=True, attachment_filename=f"{term}.csv")
    return result
  except:
    return redirect("/")

app.run(host="0.0.0.0")