import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import re

st.set_page_config(page_title="Thumbnail Mockup Generator", layout="centered")

st.markdown("## 🎯 Thumbnail Mockup Generator")

uploaded_file = st.file_uploader("Upload Thumbnail (1920x1080)", type=["jpg", "jpeg", "png"])
channel_url = st.text_input("YouTube Channel or Video Link")
video_title = st.text_input("Video Title")

if uploaded_file and channel_url and video_title:
    thumb = Image.open(uploaded_file).convert("RGB").resize((1328, 747))
    final = Image.new("RGB", (1440, 1144), "black")
    final.paste(thumb, (56, 57))

    # Get channel username from URL
    match = re.search(r"youtube\.com\/(?:@|channel\/)([\w-]+)", channel_url)
    channel_username = match.group(1) if match else "Unknown"

    # Load fonts
    font_title = ImageFont.truetype("DejaVuSans.ttf", 60)
    font_channel = ImageFont.truetype("DejaVuSans.ttf", 56)
    font_subs = ImageFont.truetype("DejaVuSans.ttf", 45)

    draw = ImageDraw.Draw(final)
    draw.text((66, 835), video_title, font=font_title, fill="white")

    # Draw channel box
    draw.rounded_rectangle((56, 947, 1384, 1082), radius=50, fill="#181818")

    # Get channel info from YouTube Data API (simulated)
    try:
        response = requests.get(f"https://yt-api.p.rapidapi.com/channel/info?handle=@{channel_username}",
            headers={
                "X-RapidAPI-Key": "demo",
                "X-RapidAPI-Host": "yt-api.p.rapidapi.com"
            },
            timeout=5
        )
        data = response.json()
        profile_pic_url = data.get("avatar", {}).get("url", "")
        subs = data.get("stats", {}).get("subscribersText", "1M subscribers")
        name = data.get("title", channel_username)
    except:
        profile_pic_url = "https://yt3.ggpht.com/ytc/AAUvwnhUv_demo=s88-c-k-c0x00ffffff-no-rj"
        subs = "1.39M subscribers"
        name = channel_username

    # Channel image
    try:
        pf_img = Image.open(BytesIO(requests.get(profile_pic_url).content)).convert("RGB").resize((87, 87))
    except:
        pf_img = Image.new("RGB", (87, 87), "gray")
    final.paste(pf_img, (93, 971))

    # Channel text
    draw.text((208, 980), name, font=font_channel, fill="white")
    draw.text((927, 988), subs, font=font_subs, fill="#B0B0B0")

    st.image(final, caption="Mockup Output", use_column_width=True)
    st.success("Mockup generated successfully!")