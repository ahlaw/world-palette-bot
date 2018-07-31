import credentials
import os
import requests
import shutil
import time
import tweepy

import palette_finder as PF

auth = tweepy.OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_SECRET)
api = tweepy.API(auth)


def get_object():
    api_url = 'https://api.unsplash.com/photos/random/'
    parameters = {
        'client_id': credentials.API_ID,
        'orientation': 'landscape',
        'w': '1080',
        'h': '720'
    }
    response = requests.get(api_url, timeout=5, params=parameters)
    data = response.json()
    return data


def download_image(link):
    save_file = '/tmp/tmp_img.jpg'
    response = requests.get(link, timeout=5, stream=True)
    if response.status_code == 200:
        with open(save_file, 'wb') as outfile:
            shutil.copyfileobj(response.raw, outfile)
    return save_file


def tweet():
    data = get_object()
    link = data["urls"]["custom"]
    img_file = download_image(link)
    palette_file = PF.get_palette(img_file)
    tweet_img = PF.format_images([img_file, palette_file])
    api.update_with_media(tweet_img)
    os.remove(img_file)
    os.remove(palette_file)
    os.remove(tweet_img)

if __name__ == "__main__":

    INTERVAL = 60 * 60 * 12

    while True:
        tweet()
        time.sleep(INTERVAL)
