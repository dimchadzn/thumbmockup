
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
from io import BytesIO
import textwrap
import re

def fetch_channel_data(channel_url):
    channel_name = "Channel Name"
    subscriber_count = "1M subscribers"
    match = re.search(r"youtube\.com/(?:@)?([\w\d_-]+)", channel_url)
    if match:
        channel_name = match.group(1).strip()
    return channel_name, subscriber_count

def round_corners(image, radius):
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, image.size[0], image.size[1]], radius=radius, fill=255)
    rounded = image.copy()
    rounded.putalpha(mask)
    return rounded

def create_mockup(thumbnail, channel_name, subscriber_count, title):
    WIDTH = 1328
    HEIGHT = 980
    FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    
    base = Image.new("RGB", (WIDTH, HEIGHT), "black")
    draw = ImageDraw.Draw(base)

    thumb = thumbnail.resize((1328, 747)).convert("RGB")
    thumb = round_corners(thumb, 50)
    base.paste(thumb, (0, 0), thumb)

    font_title = ImageFont.truetype(FONT_PATH, 60)
    font_channel = ImageFont.truetype(FONT_PATH, 48)
    font_subs = ImageFont.truetype(FONT_PATH, 40)

    title_y = 747 + 40
    draw.text((66, title_y), title, font=font_title, fill="white")

    box_height = 135
    box_y = HEIGHT - box_height
    channel_box = Image.new("RGB", (1328, box_height), "#181818")
    base.paste(channel_box, (0, box_y))

    try:
        profile_pic_url = f"https://yt3.googleusercontent.com/ytc/{channel_name}=s176-c-k-c0x00ffffff-no-rj"
        pfp = Image.open(BytesIO(requests.get(profile_pic_url).content)).convert("RGB")
    except:
        pfp = Image.new("RGB", (87, 87), color="gray")

    pfp = pfp.resize((87, 87))
    mask = Image.new("L", (87, 87), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, 87, 87), fill=255)
    base.paste(pfp, (66, box_y + 24), mask)

    draw.text((168, box_y + 38), channel_name, font=font_channel, fill="white")

    subs_text_size = draw.textlength(subscriber_count, font=font_subs)
    subs_x = WIDTH - subs_text_size - 66
    draw.text((subs_x, box_y + 42), subscriber_count, font=font_subs, fill="#B0B0B0")

    return base

st.set_page_config(page_title="Thumbnail Mockup Generator", layout="centered")

st.title("🎯 Thumbnail Mockup Generator")
thumb_file = st.file_uploader("Upload Thumbnail (1920x1080)", type=["jpg", "jpeg", "png"])
channel_url = st.text_input("YouTube Channel or Video Link")
title = st.text_input("Video Title")

if thumb_file and channel_url and title:
    image = Image.open(thumb_file).convert("RGB")
    channel_name, sub_count = fetch_channel_data(channel_url)
    result = create_mockup(image, channel_name, sub_count, title)
    st.image(result, caption="Mockup Output", use_container_width=True)
    buffered = BytesIO()
    result.save(buffered, format="PNG")
    st.download_button("Download Mockup", buffered.getvalue(), "thumbnail_mockup.png", "image/png")
