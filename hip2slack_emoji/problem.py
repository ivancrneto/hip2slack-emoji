# coding: utf-8
import os
import random
import requests
import time
from bs4 import BeautifulSoup
from splinter.browser import Browser


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

    def get_all_the_things(self):
        req = requests.get('https://www.hipchat.com/emoticons')
        soup = BeautifulSoup(req.content)
        divs = soup.findAll('div', {'class': 'emoticon-block'})

        for div in divs:
            name = div.text.strip()[1:-1]
            img = div.find('img')
            img_url = img.attrs['src']
            filepath = download_file(img_url, filedir='/tmp/emojis')
            emoji = Emoji(name, filepath)
            self.emojis.append(emoji)
            print('Downloaded: {}...'.format(emoji))

    def upload_all_the_things(self):
        self.browser = Browser('chrome')
        browser = self.browser

        url = 'https://{}.slack.com/?redir=/customize/emoji'
        url = url.format(self.slack_team)
        browser.visit(url)

        browser.fill('email', self.slack_email)
        browser.fill('password', self.slack_pass)

        keep_me = browser.find_by_name('remember')[0]
        keep_me.uncheck()

        sign_in = browser.find_by_id('signin_btn')[0]
        sign_in.click()

        for emoji in self.emojis:
            browser.fill('name', emoji.name)
            browser.fill('img', emoji.imagepath)
            submit = browser.find_by_value('Save New Emoji')[0]
            submit.click()
            time.sleep(1 + random.randrange(1, 20) / 10)

    def yougotitdude(self):
        if getattr(self, 'browser', False):
            self.browser.quit()


def main(*args, **kwargs):
    importer = EmojiImporter()
    importer.get_all_the_things()
    importer.upload_all_the_things()
    importer.yougotitdude()


if __name__ == '__main__':
    main()
