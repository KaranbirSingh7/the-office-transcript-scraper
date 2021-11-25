from bs4 import BeautifulSoup
import requests

home_urls = [
    "https://transcripts.foreverdreaming.org/viewforum.php?f=574",
    "https://transcripts.foreverdreaming.org/viewforum.php?f=574&start=25",
    "https://transcripts.foreverdreaming.org/viewforum.php?f=574&start=50",
    "https://transcripts.foreverdreaming.org/viewforum.php?f=574&start=75",
    "https://transcripts.foreverdreaming.org/viewforum.php?f=574&start=100",
    "https://transcripts.foreverdreaming.org/viewforum.php?f=574&start=125",
    "https://transcripts.foreverdreaming.org/viewforum.php?f=574&start=150",
    "https://transcripts.foreverdreaming.org/viewforum.php?f=574&start=175"
]

def get_transcript(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    ts = soup.find_all(class_='postbody')
    body  = ts[0].get_text()
    return body.strip()

def scrap_transcripts_url(homepage_url):
    base_url = "https://transcripts.foreverdreaming.org"    
    all_data = []
    r = requests.get(homepage_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    all_transcript_elements = soup.find_all('a', class_='topictitle')
    for a in all_transcript_elements:
        if a.get_text() not in "Please Read Updates: Take the 2021 Challenge!":
            print(f'episode: {a.get_text()}')
            just_url = a['href'].removeprefix('.')
            absolute_url = base_url + just_url
            transcript_data = get_transcript(absolute_url)
            episode_data = {
                'episode_name': a.get_text(),
                'url': absolute_url,
                'transcript_data': transcript_data,
            }

            all_data.append(str(episode_data))
            
    return all_data

    
all_urls = []
for each_page in home_urls:
    all_urls.extend(scrap_transcripts_url(each_page))


textfile = open("data.txt", "w")
for element in all_urls:
    textfile.write(element + "\n")
textfile.close()