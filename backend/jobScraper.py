from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib3.exceptions import InsecureRequestWarning
import urllib3
import logging
import requests

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Define the skills table
skillsTable = {
    "languages": ["Python", "JavaScript", "Java", "C++", "C#", "Ruby", "Swift", "Kotlin"],
    "frontendFrameworksLibraries": ["React.js", "Angular", "Vue.js", "jQuery", "Bootstrap", "Sass/SCSS", "Tailwind CSS"],
    "backendFrameworksLibraries": ["Node.js", "Express.js", "Django", "Flask", "Spring Boot", "Ruby on Rails", "Pytorch"],
    "databaseTechnologies": ["MySQL", "PostgreSQL", "MongoDB", "SQLite", "Firebase"],
    "mobileDevelopment": ["React Native", "Flutter", "Swift", "Kotlin"],
    "devopsDeployment": ["Docker", "Kubernetes", "AWS", "Google Cloud Platform", "Microsoft Azure"]
}

# Define months
months = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12"
}
    
def fetchLogo(company, hdr):
    logoUrl = f"https://worldvectorlogo.com/logo/{company.lower().replace(' ', '-')}"
    try:
        logoPage = urlopen(Request(logoUrl, headers=hdr))
        logoSoup = BeautifulSoup(logoPage, "html.parser")
        logoResults = logoSoup.find_all("img", class_="larger")
        return logoResults[0]["src"] if logoResults else f"/logos/{company.replace(' ', '').lower()}.png"
    except Exception as e:
        logging.warning(f"Failed to fetch logo for {company}: {e}")
        return f"/logos/{company.replace(' ', '').lower()}.png"

def fetchJobDetails(job, session):
    try:
        jobUrl = job["link"]
        application = session.get(jobUrl, verify=False, timeout=10)
        application.raise_for_status()
        soup = BeautifulSoup(application.content, "html.parser")
        textContent = soup.get_text().lower().strip()

        skillCounts = {}
        for skills in skillsTable.values():
            for skill in skills:
                count = textContent.count(skill.lower())
                if count > 0:
                    skillCounts[skill] = count

        sortedSkills = sorted(skillCounts.items(), key=lambda item: item[1], reverse=True)
        job['skills'] = [skill for skill, count in sortedSkills[:5]]
        return
    except Exception as e:
        # logging.error(f"Error fetching job details for {job['company']}: {e}")
        # return job
        pass

def jobScraper():
    # Disable warnings for unverified HTTPS requests
    urllib3.disable_warnings(InsecureRequestWarning)
    url = "https://github.com/Ouckah/Summer2025-Internships"
    hdr = {'User-Agent': 'Mozilla/5.0'}

    try:
        page = requests.get(url, timeout=10)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, "html.parser")
    except Exception as e:
        logging.error(f"Failed to fetch the main page: {e}")
        return []

    results = soup.find_all("tbody")
    if len(results) < 2:
        logging.warning("No job postings found on the page.")
        return []

    results = results[1]
    jobs = results.find_all("tr")

    output = []
    seenLinks = set()
    for jobElement in jobs:
        info = jobElement.find_all("td")
        if len(info) < 3:
            continue

        companyElement = info[0].text.strip()
        titleElement = info[1].text.strip()

        if companyElement == '↳':
            companyElement = output[-1]["company"]

        locationElement = info[2].text.strip()
        links = info[3].find_all("a")
        if not links:
            continue
        linkElement = links[0]["href"]
        dateElement = info[4].text.strip()
        dateElement = months[dateElement[:-3]] + "-"  + dateElement[-2:]

        if linkElement in seenLinks:
            continue
        
        newJob = {
            "position": titleElement,
            "company": companyElement,
            "location": locationElement,
            "link": linkElement,
            "logo": fetchLogo(companyElement, hdr),
            "skills": [],
            "date": dateElement
        }
    
        output.append(newJob)
        seenLinks.add(linkElement)
            

    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=10) as executor:
            futureToJob = {executor.submit(fetchJobDetails, job, session): job for job in output}
            for future in as_completed(futureToJob):
                job = futureToJob[future]
                try:
                    result = future.result()
                except Exception as exc:
                    logging.error(f"Job {job['company']} generated an exception: {exc}")

    return output

# Test the scraper function
if __name__ == "__main__":
    job_listings = jobScraper()
