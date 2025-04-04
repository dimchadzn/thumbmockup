
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
import io
import re
from googleapiclient.discovery import build

# ========== SETUP ==========
API_KEY = "AIzaSyBkAAqlsI218xbNsCOzR4COq-LsGa0L6F0"
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_channel_info_from_url(url):
    channel_id = None
    video_id = None

    if "channel/" in url:
        channel_id = url.split("channel/")[1].split("/")[0]
    elif "youtube.com/@" in url:
        username = url.split("youtube.com/@")[1].split("/")[0]
        req = youtube.search().list(q=username, type="channel", part="snippet", maxResults=1)
        res = req.execute()
        if res["items"]:
            channel_id = res["items"][0]["snippet"]["channelId"]
    elif "watch?v=" in url:
        match = re.search(r"v=([\w-]+)", url)
        if match:
            video_id = match.group(1)
            req = youtube.videos().list(part="snippet", id=video_id)
            res = req.execute()
            if res["items"]:
                channel_id = res["items"][0]["snippet"]["channelId"]

    if channel_id:
        req = youtube.channels().list(part="snippet,statistics", id=channel_id)
        res = req.execute()
        if res["items"]:
            info = res["items"][0]
            return {
                "name": info["snippet"]["title"],
                "subs": info["statistics"]["subscriberCount"],
                "pfp_url": info["snippet"]["thumbnails"]["high"]["url"]
            }
    return None

def format_subs(subs):
    subs = int(subs)
    if subs >= 1_000_000:
        return f"{subs/1_000_000:.2f}M subscribers"
    elif subs >= 1_000:
        return f"{subs/1_000:.1f}K subscribers"
    return str(subs)

# ========== STREAMLIT UI ==========
st.set_page_config(page_title="Thumbnail Mockup Generator", layout="centered")
st.title("🎯 Thumbnail Mockup Generator")

thumb_file = st.file_uploader("Upload Thumbnail (1920x1080)", type=["jpg", "jpeg", "png"])
url = st.text_input("YouTube Channel or Video Link")
title = st.text_input("Video Title")

channel_name = ""
subs = ""
pfp_img = None

if url:
    info = get_channel_info_from_url(url)
    if info:
        channel_name = info["name"]
        subs = format_subs(info["subs"])
        response = requests.get(info["pfp_url"])
        pfp_img = Image.open(io.BytesIO(response.content)).convert("RGB").resize((87, 87), Image.LANCZOS)

if thumb_file and title and channel_name:
    WIDTH, HEIGHT = 1440, 1144
    mockup = Image.new("RGB", (WIDTH, HEIGHT), color=(0, 0, 0))

    thumb = Image.open(thumb_file).convert("RGB").resize((1328, 747))
    mask = Image.new("L", thumb.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle([0, 0, 1328, 747], radius=50, fill=255)
    thumb.putalpha(mask)
    mockup.paste(thumb, (56, 57), thumb)

    draw = ImageDraw.Draw(mockup)
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
    font_channel = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56)
    font_subs = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 45)

    # Title
    draw.text((66, 835), title, font=font_title, fill="white")

    # Channel bar background
    bar = Image.new("RGB", (1328, 135), (24, 24, 24))
    rounded_bar = Image.new("L", (1328, 135), 0)
    draw_bar = ImageDraw.Draw(rounded_bar)
    draw_bar.rounded_rectangle([0, 0, 1328, 135], radius=50, fill=255)
    bar.putalpha(rounded_bar)
    mockup.paste(bar, (56, 947), bar)

    # PFP
    if pfp_img:
        circle = Image.new("L", (87, 87), 0)
        draw_circle = ImageDraw.Draw(circle)
        draw_circle.ellipse((0, 0, 87, 87), fill=255)
        pfp_img.putalpha(circle)
        mockup.paste(pfp_img, (93, 971), pfp_img)

    draw.text((208, 980), channel_name, font=font_channel, fill="white")
    draw.text((927, 988), subs, font=font_subs, fill="#B0B0B0")

    st.image(mockup, caption="Mockup Output", use_container_width=True)
    mockup.save("mockup_final_output.png")
    with open("mockup_final_output.png", "rb") as f:
        st.download_button("Download Mockup", f, file_name="thumbnail_mockup.png")
