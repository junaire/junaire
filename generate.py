import requests
from lxml import etree

URL = "https://c.xkcd.com/random/comic/"

README = """
<p align="center"><img src="{image_url}"></p>
<h2 align="center">{image_desc}</h2>
"""


def fetch_image(url):
    print("Fetching the image!")
    response = requests.get(url)
    assert response.status_code == 200, "Can't grab the page!"
    html = etree.HTML(response.content)

    # Get the comic image from the div with id="comic"
    img_src = html.xpath('//div[@id="comic"]//img/@src')
    img_alt = html.xpath('//div[@id="comic"]//img/@alt')
    img_title = html.xpath('//div[@id="ctitle"]/@title')

    if not img_src or not img_alt:
        return None, None

    # xkcd uses protocol-relative URLs, so add https:
    image_url = img_src[0]
    if image_url.startswith('//'):
        image_url = 'https:' + image_url

    # Use alt text as title, and include hover text if available
    image_desc = img_alt[0]
    if img_title:
        image_desc += f" - {img_title[0]}"

    return image_desc, image_url

def generate(readme_format, image_desc, image_url):
    readme_format = README.format(image_url=image_url, image_desc=image_desc)
    with open("README.md", "w+") as f:
        print("Generating the README!")
        f.write(readme_format)

if __name__ == "__main__":
    image_desc, image_url = fetch_image(URL)
    if image_desc is None or image_url is None:
        print("Invalid data when fetching the image, do nothing today")
    else:
        generate(README, image_desc, image_url)

