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
    noisy = img + img + gauss
    
    # normalize image to range [0,255]
    minv = np.amin(noisy)
    maxv = np.amax(noisy)
    noisy = (255 * (noisy - minv) / (maxv - minv)).astype(np.uint8)

    return Image.fromarray(noisy)

def recieve_image():
    reddit = praw.Reddit(client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent="user agent")

    subreddit = reddit.subreddit("nsfw")

    hot_posts = subreddit.hot(limit = 5)

    for post in hot_posts:
        if ".jpg" in post.url:
            with open('pic.jpg', 'wb') as f:
                f.write(requests.get(post.url).content)

def deep_fry_image():
    image = Image.open('pic.jpg')

    
    image = add_noise(image)
    image = ImageEnhance.Color(image).enhance(3)
    image = ImageEnhance.Contrast(image).enhance(3)
    image = ImageEnhance.Brightness(image).enhance(1.5)
    image = ImageEnhance.Sharpness(image).enhance(3)

    
    image.save("ced.jpg")


def main():
    recieve_image()
    deep_fry_image()

if __name__ == "__main__":
    main()