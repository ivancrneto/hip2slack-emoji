# coding: utf-8
import os
import requests
from bs4 import BeautifulSoup


def download_file(url, filedir=None):
    local_filename = url.split('/')[-1]
    if filedir:
        if not os.path.isdir(filedir):
            os.makedirs(filedir)
        local_filename = '{}/{}'.format(filedir, local_filename)

    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
    return local_filename


class Emoji(object):

    def __init__(self, name, imagepath):
        self.name = name
        self.imagepath = imagepath

    def __str__(self):
        return '{} - {}'.format(self.name, self.imagepath)

    def __repr__(self):
        return str(self)


class EmojiImporter(object):

    def __init__(self):
        self.slack_team = os.environ.get('SLACK_TEAM')
        self.slack_email = os.environ.get('SLACK_EMAIL')
        self.slack_pass = os.environ.get('SLACK_PASS')

        if not all((self.slack_team, self.slack_email, self.slack_pass)):
            raise ValueError(
                'Make sure to set SLACK_TEAM, SLACK_EMAIL and SLACK_PASS '
                'environment variables')

        self.emojis = []

    def all_the_things(self):
        req = requests.get('https://www.hipchat.com/emoticons')
        soup = BeautifulSoup(req.content)
        divs = soup.findAll('div', {'class': 'emoticon-block'})

        for div in divs:
            name = div.text.strip()[1:-1]
            img = div.find('img')
            img_url = img.attrs['src']
            filepath = download_file(img_url, filedir='/tmp/emojis')
            self.emojis.append(Emoji(name, filepath))

        print(self.emojis)


if __name__ == '__main__':
    importer = EmojiImporter()
    importer.all_the_things()
