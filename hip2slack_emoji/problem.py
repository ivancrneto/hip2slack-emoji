# coding: utf-8
import os
import getpass
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

    def __init__(self, slack_team=None, slack_email=None, slack_pass=None):
        self.slack_team = slack_team or os.environ.get('SLACK_TEAM')
        self.slack_email = slack_email or os.environ.get('SLACK_EMAIL')
        self.slack_pass = slack_pass or os.environ.get('SLACK_PASS')

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

        url = 'https://{}.slack.com/?redir=/customize/emoji&no_sso=1'
        url = url.format(self.slack_team)
        browser.visit(url)

        browser.fill('email', self.slack_email)
        browser.fill('password', self.slack_pass)

        keep_me = browser.find_by_name('remember')[0]
        keep_me.uncheck()

        sign_in = browser.find_by_id('signin_btn')[0]
        sign_in.click()

        for emoji in self.emojis:
            if self.deal_with_it(emoji):
                print('Uploaded: {}...'.format(emoji))
            else:
                print('We had problems uploading {}...'.format(emoji))

    def deal_with_it(self, emoji):
        browser = self.browser

        def fill_and_submit(emoji):
            browser.fill('name', '')
            browser.fill('name', emoji.name)
            if (browser.is_element_present_by_css(
                    '.c-alert__icon.c-icon--warning') and not
                    emoji.name.endswith('2')):
                emoji.name += '2'
                browser.fill('name', '')
                browser.fill('name', emoji.name)

            browser.fill('img', emoji.imagepath)
            submit = browser.find_by_xpath(
                '//button[contains(text(), "Save")]')[0]

            submit.click()
            time.sleep(1 + random.randrange(1, 20) / 10)

        if not browser.is_element_present_by_css(
                'button[emoji-type="emoji"]', wait_time=10):
            raise Exception('Add emoji button not found')
        initial_buttons = browser.find_by_css('button[emoji-type="emoji"]')
        for btn in initial_buttons:
            if btn.visible:
                btn.click()

        fill_and_submit(emoji)
        errors = browser.find_by_css('.c-alert.c-alert--level_error')
        for error in errors:
            text = error.text

            if any(['is already in use by another emoji' in text,
                    'Mind trying a different name' in text]):
                # for now appending 2 to emoji name and trying again
                emoji.name += '2'
                fill_and_submit(emoji)
                errors = browser.find_by_css('.c-alert.c-alert--level_error')
                errors += browser.find_by_css('.c-alert__icon.c-icon--warning')
                if errors:
                    return False
                else:
                    break

        success = browser.find_by_css('.alert.alert_success')
        for s in success:
            if 'Your new emoji has been saved' in s.text:
                return True

    def yougotitdude(self):
        if getattr(self, 'browser', False):
            self.browser.quit()


def main(*args, **kwargs):
    slack_team = os.environ.get('SLACK_TEAM')
    slack_email = os.environ.get('SLACK_EMAIL')
    slack_pass = os.environ.get('SLACK_PASS')

    if not slack_team:
        slack_team = input('Your Slack team as in http://<team>.slack.com/: ')
    if not slack_email:
        slack_email = input('Your Slack email: ')
    if not slack_pass:
        slack_pass = getpass.getpass('Your Slack password: ')

    importer = EmojiImporter(slack_team, slack_email, slack_pass)
    importer.get_all_the_things()
    importer.upload_all_the_things()
    importer.yougotitdude()


if __name__ == '__main__':
    main()
