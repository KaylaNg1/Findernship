import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

languages = [
    "Python",
    "JavaScript",
    "Java",
    "C++",
    "C#",
    "Ruby",
    "Swift",
    "Kotlin"
]

frontend_frameworks_libraries = [
    "React.js",
    "Angular",
    "Vue.js",
    "jQuery",
    "Bootstrap",
    "Sass/SCSS",
    "Tailwind CSS"
]

backend_frameworks_libraries = [
    "Node.js",
    "Express.js",
    "Django",
    "Flask",
    "Spring Boot",
    "Ruby on Rails",
    "ASP.NET",
    "Laravel"
]

database_technologies = [
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "SQLite",
    "Firebase"
]

mobile_development = [
    "React Native",
    "Flutter",
    "Swift (iOS)",
    "Kotlin (Android)"
]

testing_frameworks = [
    "Jest (JavaScript)",
    "Jasmine (JavaScript)",
    "Pytest (Python)",
    "JUnit (Java)",
    "Selenium",
    "Cucumber"
]

devops_deployment = [
    "Docker",
    "Kubernetes",
    "Jenkins",
    "Travis CI",
    "CircleCI",
    "Heroku",
    "AWS",
    "Google Cloud Platform (GCP)",
    "Microsoft Azure"
]

def jobScraper(): # will rename to github scraper
  # GITHUB 2025 Summer Internships ( don't need to filter down ):
  URL = "https://github.com/Ouckah/Summer2025-Internships"
  LOGO_URL = "https://worldvectorlogo.com/logo/"
  page = requests.get(URL) 
  hdr = {'User-Agent': 'Mozilla/5.0'}

  # Creating BeautifulSoup Object
  # You’ll want to pass page.content instead of page.text to avoid problems with character encoding. 
  # The .content attribute holds raw bytes, which can be decoded better than the text representation you printed earlier using the .text attribute.
  soup = BeautifulSoup(page.content, "html.parser") # page.content <-> HTML content

  results = soup.find_all("tbody")
  if len(results) >=2:
    results = results[1]
    jobs = results.find_all("tr")

    # TODO: need to handle multiple location case + subjob case + dupes
    output = []
    for jobElement in jobs:
      info = jobElement.find_all("td")
      if len(info) >=3:
        newJob = {}
        titleElement = info[1].text.strip()
        companyElement = info[0].text.strip()
        
        # edge cases
        if companyElement in output:
          continue
        elif companyElement == '↳':
          companyElement = output[-1]["company"]
          
        LOGO_URL = "https://worldvectorlogo.com/logo/"
        LOGO_URL += companyElement.lower().replace(" ", "-")
        
        try:
          logoPage = urlopen(Request(LOGO_URL, headers = hdr))
          logoSoup = BeautifulSoup(logoPage, "html.parser")
          logoResults = logoSoup.find_all("img", class_ = "larger")
          newJob["logo"] = logoResults[0]["src"]
        except:
          newJob["logo"] = "/defaultJob.png"
        locationElement = info[2].text.strip()
        links = jobElement.find_all("a")
        
        if links:
          linkElement = links[0]["href"]
          newJob["position"] = titleElement
          newJob["company"] = companyElement
          newJob["location"] = locationElement
          newJob["link"] = linkElement
          
          
          
          output.append(newJob)
    return output