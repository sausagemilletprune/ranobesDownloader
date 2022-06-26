from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path
import sys

# MODIFY THIS TO YOUR OS
CHROMIUM_PATH = "/Applications/Chromium.app/Contents/MacOS/Chromium"


def main():
    check_arguments()

    URL = sys.argv[1]
    driver = create_chromium_driver()
    storyname = get_story_name(URL, driver)

    bookPath = f"{storyname}.html"
    print(bookPath)

    while URL:
        soup = BeautifulSoup(get_page_content(URL, driver), "html.parser")
        append_chapter_to_file(bookPath, parse_chapter(URL, soup, storyname))
        URL = get_next_url(soup)


def check_arguments():
    if len(sys.argv) < 2:
        raise RuntimeError(f"Must include 1 argument: URL\nUsage: `python3 {sys.argv[0]} URL")


def append_chapter_to_file(bookPath, chapter):
    with open(bookPath, "a") as file:
        file.write(chapter)


def parse_chapter(URL, soup, storyname):
    title = find_title(soup, storyname)
    body = find_body(soup)
    chapter = create_chapter_string(URL, body, title)
    print(f"Scraped chapter {title}")
    return chapter


def create_chapter_string(URL, body, title):
    return f'<h1 class="chapter">{title}</h1>\n' \
           f'<div class="chapter-inner chapter-content">{body}</div>\n' \
           f'<!--{URL}-->\n\n'


def get_story_name(URL, driver):
    pageContent = get_page_content(URL, driver)
    soup = BeautifulSoup(pageContent, "html.parser")
    navBar = soup.find(id="dle-speedbar")
    return navBar.find_all("a")[1].text


def get_next_url(soup):
    nextButton = find_btn_next(soup)
    if not nextButton:
        return None

    return nextButton["href"]


def find_body(soup):
    article = soup.find(id="arrticle")
    ps = map(str, article.find_all("p"))
    return "\n".join(ps)


def find_title(soup, storyname):
    return soup.find(id="dle-content").find_all("h1", class_="title")[0].text.strip()[:-len(f" | {storyname}")]


def find_btn_next(soup):
    return soup.find(id="next")


def create_chromium_driver():
    service_object = Service(binary_path)
    options = webdriver.ChromeOptions()
    options.binary_location = CHROMIUM_PATH
    return webdriver.Chrome(service=service_object, options=options)


def get_page_content(URL, driver):
    driver.get(URL)
    pageContent = driver.page_source
    return pageContent


if __name__ == "__main__":
    main()
