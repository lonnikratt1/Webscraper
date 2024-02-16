import flask
from flask import Flask, request

app = Flask(__name__)

@app.route('/crawl')
def crawl(url, max_depth=3, current_depth=1, visited_links=set()):
  if current_depth > max_depth or url in visited_links:
    return
  visited_links.add(url)
  try:
    response = requests.get(url)
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    print(f"Failed to retrieve the page at {url}. Error: {e}")
    return
  soup = BeautifulSoup(response.text, 'html.parser')
  links = soup.find_all('a', href=True)
  print(f"Links from {url}:")
  for link in links:
    next_url = link['href']
    print(next_url)
    if next_url.startswith('http') and current_depth < max_depth:
        crawl_links(next_url, max_depth, current_depth + 1, visited_links)
    url = request.args.get('url')
    # Perform crawling and return the result
    return f'Crawling {url}...'

@app.route('/scrape')
def scrape(url):
  response = requests.get(url)
  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    for link in links:
          print(link.get('href'))
    else:
      print(f"Failed to retrieve the page. Status code: {response.status_code}")
    url = request.args.get('url')
    # Perform scraping and return the result
    return f'Scraping {url}...'

if __name__ == '__main__':
    app.run(debug=True)
