import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib3.exceptions import InsecureRequestWarning
import urllib3

# Define the skills table
table = {
    "languages": ["Python", "JavaScript", "Java", "C++", "C#", "Ruby", "Swift", "Kotlin"],
    "frontend_frameworks_libraries": ["React.js", "Angular", "Vue.js", "jQuery", "Bootstrap", "Sass/SCSS", "Tailwind CSS"],
    "backend_frameworks_libraries": ["Node.js", "Express.js", "Django", "Flask", "Spring Boot", "Ruby on Rails", "Pytorch"],
    "database_technologies": ["MySQL", "PostgreSQL", "MongoDB", "SQLite", "Firebase"],
    "mobile_development": ["React Native", "Flutter", "Swift", "Kotlin"],
    "devops_deployment": ["Docker", "Kubernetes", "AWS", "Google Cloud Platform", "Microsoft Azure"]
}

def fetch_logo(company, hdr):
    logo_url = f"https://worldvectorlogo.com/logo/{company.lower().replace(' ', '-')}"
    try:
        logoPage = urlopen(Request(logo_url, headers=hdr))
        logoSoup = BeautifulSoup(logoPage, "html.parser")
        logoResults = logoSoup.find_all("img", class_="larger")
        return logoResults[0]["src"] if logoResults else "/" + company.replace(" ", "") + ".png"
    except:
        return "/logos/" + company.replace(" ", "").lower() + ".png"

def fetch_job_details(job):
    job_url = job["link"]
    application = requests.get(job_url, verify=False)
    soup = BeautifulSoup(application.content, "html.parser")
    text_content = soup.get_text().lower().strip()  # Use get_text() to extract text content

    skill_counts = {}
    for key, skills in table.items():
        for skill in skills:
            count = text_content.count(skill.lower())
            if count > 0:
                skill_counts[skill] = count

    sorted_skills = sorted(skill_counts.items(), key=lambda item: item[1], reverse=True)
    job["skills"] = []
    for skill, count in sorted_skills:
        job["skills"].append(skill)
        if len(job["skills"]) == 5:
            break
    return job

def jobSraper(): 
    # Disable warnings for unverified HTTPS requests
    urllib3.disable_warnings(InsecureRequestWarning)  
    URL = "https://github.com/Ouckah/Summer2025-Internships"
    hdr = {'User-Agent': 'Mozilla/5.0'}

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find_all("tbody")
    if len(results) < 2:
        return []

    results = results[1]
    jobs = results.find_all("tr")

    output = []
    jobs_list = []
    for jobElement in jobs:
        info = jobElement.find_all("td")
        if len(info) < 3:
            continue

        titleElement = info[1].text.strip()
        companyElement = info[0].text.strip()

        if companyElement == '↳':
            companyElement = output[-1]["company"]

        locationElement = info[2].text.strip()
        links = jobElement.find_all("a")
        if not links:
            continue

        linkElement = links[0]["href"]
        newJob = {
            "position": titleElement,
            "company": companyElement,
            "location": locationElement,
            "link": linkElement,
            "logo": fetch_logo(companyElement, hdr),
            "skills": []
        }
        output.append(newJob)

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_job = {executor.submit(fetch_job_details, job): job for job in output}
        for future in as_completed(future_to_job):
            job = future_to_job[future]
            try:
                result = future.result()
                jobs_list.append(result)
            except Exception as exc:
                print(f"Job {job['company']} generated an exception: {exc}")


    return jobs_list
