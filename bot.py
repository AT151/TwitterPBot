import config
import praw
import numpy as np
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import requests

def add_noise(image):
    img = np.array(image)

    row,col,ch= img.shape
    mean = 0
    var = 0.1
    sigma = var**0.5
    gauss = np.random.normal(mean,sigma,(row,col,ch))
    gauss = gauss.reshape(row,col,ch)
    noisy = img * 2 + gauss

    # normalize image to range [0,255]
    minv = np.amin(noisy)
    maxv = np.amax(noisy)
    noisy = (255 * (noisy - minv) / (maxv - minv)).astype(np.uint8)

    return Image.fromarray(noisy)

def add_text(image):
    x, y = image.size[0] / 5, image.size[1] / 4

    text = "Bottom Text"
    draw = ImageDraw.Draw(image)
    font_type = ImageFont.truetype("Arial.ttf", 128)  # 18 -> font size
    # thin border
    draw.text((x-1, y), text, font=font_type, fill="black")
    draw.text((x+1, y), text, font=font_type, fill="black")
    draw.text((x, y-1), text, font=font_type, fill="black")
    draw.text((x, y+1), text, font=font_type, fill="black")

    # thicker border
    draw.text((x-1, y-1), text, font=font_type, fill="black")
    draw.text((x+1, y-1), text, font=font_type, fill="black")
    draw.text((x-1, y+1), text, font=font_type, fill="black")
    draw.text((x+1, y+1), text, font=font_type, fill="black")

    draw.text((x, y), text, (255, 255, 255), font=font_type) 

def recieve_image():
    reddit = praw.Reddit(client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent="user agent")

    subreddit = reddit.subreddit("cats")

    hot_posts = subreddit.top(limit = 5)

    for post in hot_posts:
        if ".jpg" in post.url or ".png" in post.url:
            with open('pic.png', 'wb') as f:
                f.write(requests.get(post.url).content)

def deep_fry_image():
    image = Image.open('pic.png')


    add_text(image)
    image = add_noise(image)
    image = ImageEnhance.Color(image).enhance(3)
    image = ImageEnhance.Contrast(image).enhance(5)
    image = ImageEnhance.Brightness(image).enhance(1.5)
    
    image = ImageEnhance.Sharpness(image).enhance(3)
    

    image.save("fried.png")


def main():
    recieve_image()
    deep_fry_image()

if __name__ == "__main__":
    main()