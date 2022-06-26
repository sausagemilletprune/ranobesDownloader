from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path
import sys


def main():
    URL = sys.argv[1]
    driver = create_chromium_driver()

    storyname = get_story_name(URL, driver)
    bookPath = f"{storyname}.html"
    print(bookPath)

    while URL:
        pageContent = get_page_content(URL, driver)

        soup = BeautifulSoup(pageContent, "html.parser")

        title = find_title(soup)[:-len(" | Lord of the Mysteries")]
        body = find_body(soup)

        chapter = f'<h1 class="chapter">{title}</h1>\n' \
                  f'<div class="chapter-inner chapter-content">{body}</div>\n' \
                  f'<!--{URL}-->\n\n'

        print(f"Scraped chapter {title}")
        URL = get_next_url(soup)

        with open(bookPath, "a") as file:
            file.write(chapter)


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
    ps = map(lambda p: f"<p>{p.text.strip()}</p>", article.find_all("p"))
    return "\n".join(ps)


def find_title(soup):
    return soup.find(id="dle-content").find_all("h1", class_="title")[0].text.strip()


def find_btn_next(soup):
    return soup.find(id="next")


def create_chromium_driver():
    service_object = Service(binary_path)
    options = webdriver.ChromeOptions()
    options.binary_location = "/Applications/Chromium.app/Contents/MacOS/Chromium"
    return webdriver.Chrome(service=service_object, options=options)


def get_page_content(URL, driver):
    driver.get(URL)
    pageContent = driver.page_source
    return pageContent


if __name__ == "__main__":
    main()
