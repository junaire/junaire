import requests
from lxml import etree

URL = "https://apod.nasa.gov/apod/"

README = """
<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Astronomy Picture of the Day</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        body {
            font-family: 'Poppins', sans-serif;
        }
    </style>
</head>

<body class="flex items-center justify-center h-screen bg-gray-100">

    <div class="text-center">
        <img src="{image_url}"
            class="w-4/5 max-w-md mx-auto mb-4 rounded-lg  shadow-xl">
        <p class="text-gray-700 font-semibold text-lg">{image_desc}</p>
    </div>

</body>

</html>
"""


def fetch_image(base_url):
    print("Fetching the image!")
    url = base_url + "astropix.html"
    response = requests.get(url)
    assert response.status_code == 200, "Can't grab the page!"
    html = etree.HTML(response.content)

    img_relative_url = html.xpath("//center//a/img/@src")
    if len(img_relative_url) != 1:
        return None, None
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
    if image_desc is None or image_url is None:
        print("Invalid data when fetching the image, do nothing today")
        return
    generate(README, image_desc, image_url)

