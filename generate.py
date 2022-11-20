import requests
from lxml import etree

URL = "https://apod.nasa.gov/apod/"

README = """
<p align="center"><img src="{image_url}" width="500" height="500"></p>
<h2 align="center">{image_desc}</h2>
"""


def fetch_image(base_url):
    print("Fetching the image!")
    url = base_url + "astropix.html"
    response = requests.get(url)
    assert response.status_code == 200, "Can't grab the page!"
    html = etree.HTML(response.content)

    img_relative_url = html.xpath("//center//a/img/@src")
    assert len(img_relative_url) == 1, "Mutiple images found!"
    image_url = base_url + img_relative_url[0]

    image_desc = html.xpath("//body//center/b/text()")[0]

    return image_desc, image_url

def generate(readme_format, image_desc, image_url):
    readme_format = README.format(image_url=image_url, image_desc=image_desc)
    with open("README.md", "w+") as f:
        print("Generating the README!")
        f.write(readme_format)

if __name__ == "__main__":
    image_desc, image_url = fetch_image(URL)
    generate(README, image_desc, image_url)

