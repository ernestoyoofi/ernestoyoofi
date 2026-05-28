import uuid
from datetime import datetime, timedelta
from curl_cffi import requests
from bs4 import BeautifulSoup
import log
from urllib.parse import urljoin

session = requests.Session(impersonate="chrome120")

# Base Date Now
now = datetime.now()
now_year = str(now.year)

github_username = "ernestoyoofi"
tabparamsurl = f"?tab=overview&from={now_year}-01-01&to={now_year}-12-31"

headers = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Sec-Ch-Ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
  "Sec-Ch-Ua-Mobile": "?0",
  "Sec-Ch-Ua-Platform": '"Windows"',
}

# Get Access To Widget Contribute
urlaccess = f"https://github.com/{github_username}{tabparamsurl}"
log.info(f"URL Profile: {urlaccess}")

response_profile = session.get(urlaccess, headers=headers)

if response_profile.status_code == 200:
  soup_profile = BeautifulSoup(response_profile.content, "html.parser")

  meta_release = soup_profile.select_one('meta[name="release"]')
  widget_contribute = soup_profile.select('include-fragment[data-nonce]')
  
  if not meta_release or not widget_contribute:
    log.error("Error Get Meta Release")
    exit(1)

  github_version = meta_release.get("content")
  nonce_validate = widget_contribute[0].get("data-nonce")
  widget_url = widget_contribute[0].get("src")

  log.info("Data Params:", github_version, nonce_validate)
else:
  log.error(f"Error Access Profile! Status: {response_profile.status_code}")
  exit(1)

# Get Base Widget
url_widget = urljoin("https://github.com/", widget_url)
log.info(f"URL Widget: {url_widget}")

# Update Headers
new_headers = {
  **headers,
  "Accept": "text/html",
  "Referer": urlaccess,
  "Sec-Fetch-Dest": "empty",
  "Sec-Fetch-Mode": "cors",
  "Sec-Fetch-Site": "same-origin",
  "X-Fetch-Nonce": nonce_validate,
  "X-Github-Client-Version": github_version,
  "X-Requested-With": "XMLHttpRequest",
}

response_widget = session.get(url_widget, headers=new_headers)

if response_widget.status_code == 200:
  # Fetch Data
  soup_widget = BeautifulSoup(response_widget.content, "html.parser")

  # Array To API Data Level
  data_array = []
  get_table = soup_widget.select("td")
  for a in get_table:
    if type(a.get("data-level")) == str:
      json_data = {
        "commit_level": int(a.get("data-level", "0")),
        "commit_date": a.get("data-date", "")
      }
      data_array.append(json_data)
  data_array = sorted(data_array, key=lambda x: x['commit_date'])

  # Checking Weekly If Have Commit
  date_obj = datetime.now().date()
  start_of_week = date_obj - timedelta(days=date_obj.weekday())
  end_of_week = start_of_week + timedelta(days=6)

  # Filter
  filtered_data = [
    item for item in data_array 
    if start_of_week <= datetime.strptime(item['commit_date'], "%Y-%m-%d").date() <= end_of_week
  ]

  # Search & Founding If Have Commit More Big Than Daily
  search_bigcommit = max(filtered_data, key=lambda x: int(x['commit_level']))
  if search_bigcommit["commit_level"] > 1:
    # Generate Uniq Streak
    unique_id = uuid.uuid4().hex
    timestamp = datetime.now().isoformat()
    content = f"{unique_id}-{timestamp}"
    with open("streak.txt", "w") as f:
      f.write(content + "\n")
    log.info("Having commit daily!")
  else: 
    log.info("No have commit daily")
else:
  log.error(f"Error Access Widget! Status: {response_widget.status_code}")
  exit(1)