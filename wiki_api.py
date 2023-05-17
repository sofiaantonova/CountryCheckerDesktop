from requests import get
from urllib.request import urlopen
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import os
from io import BytesIO

def _correction_link(link: str) -> str:
    link = link.replace(" ", "_")  
    link = link.replace("'", "%27")
    return link  

def get_raw_page(symbol: str) -> str:
    symbol = _correction_link(symbol)
    ref = f"https://en.wikipedia.org/w/index.php?action=raw&title={symbol}"
    return get(ref).text

def get_image(file_name) -> Image:
    file_name = _correction_link(file_name)
    link = get(f"https://commons.wikimedia.org/wiki/Special:FilePath/{file_name}")
    url = link.url
    if file_name.find(".svg") != -1:
        # print(link.url)
        url = url.replace("commons", "commons/thumb")
        file_name = url [url.rfind("/") + 1 : len(url)]
        url += f"/800px-{file_name}.png"
        # return renderPM.drawToPIL(svg2rlg(ref))
    try:
        
        return Image.open(urlopen(url))
    except:
        print(file_name)
        print(url)
        return get_image_old(["lider_1", "png"])

def get_image_old(flag) -> Image:
    file_name = _correction_link(flag[0])
    type = flag[1]
    if type=="jpg":
        ref = urlopen(f"https://commons.wikimedia.org/wiki/Special:FilePath/{file_name}.jpg")
        return Image.open(ref)
    if type=="svg": 
        ref = urlopen(f"https://commons.wikimedia.org/wiki/Special:FilePath/{file_name}.svg")
        return renderPM.drawToPIL(svg2rlg(ref))
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static/png/")
    return Image.open(os.path.join(image_path, f"{file_name}.png"))
