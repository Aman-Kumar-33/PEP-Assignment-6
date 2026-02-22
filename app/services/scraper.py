import requests
from bs4 import BeautifulSoup

def get_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

def scrape_ivy_opportunities():
    all_opps = []
    # Using a base URL map to fix relative paths
    targets = [
        {"univ": "Harvard", "base": "https://news.harvard.edu", "url": "https://news.harvard.edu/gazette/section/science-technology/", "selector": "h3 a"},
        {"univ": "Yale", "base": "https://news.yale.edu", "url": "https://news.yale.edu/topics/science-technology", "selector": ".news-listing-item-title a"}
    ]

    for site in targets:
        soup = get_soup(site['url'])
        if soup:
            links = soup.select(site['selector'])[:5]
            for link in links:
                href = link.get('href')
                # FIX: Prepend base URL if the link is relative (starts with /)
                if href and href.startswith('/'):
                    href = site['base'] + href
                
                all_opps.append({
                    "title": link.get_text(strip=True),
                    "link": href,
                    "university": site['univ'],
                    "description": f"Latest intelligence from {site['univ']}."
                })
    return all_opps