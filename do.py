#!/usr/bin/env python3

import argparse
import json
import logging
from time import sleep
from math import ceil
from datetime import datetime
from splinter import Browser

DATE_FORMAT = '%Y%m%d'

def login(username, password):
    print('logging in...')
    browser.visit('https://www.instagram.com/accounts/login/')
    browser.fill('username', username)
    browser.fill('password', password + '\n')
    # if not browser.is_element_present_by_text('Watch All', wait_time=60):
    #     raise Exception('Invalid credentials or expect element not present!')
    sleep(60)
    print('done')


def logout():
    print('logging out')
    browser.visit('https://www.instagram.com/accounts/logout/')
    # sleep(3)
    print('done')


def get_post_id(link):
    return link[28:link.rfind('/')]


def get_username(link):
    return link[26:link.rfind('/')]


def get_user_id():
    cc = 0
    for elem in browser.find_by_tag('header'):
        if cc == 1:
            user_link = elem.find_by_tag(
                'div').first.find_by_tag('a').first['href']
            return user_link[26:user_link.rfind('/')]
            break
        else:
            cc += 1
    return None


def is_user_in_following(user_id):
    for user in following:
        if user == user_id:
            return True
    return False


def screenshot():
    browser.screenshot(name='error')
    with open('error.html', 'w+') as f:
        f.write(browser.html)
    # driver.save_screenshot('your_screenshot.png')


def scroll_down(times):
    for _ in range(times):
        browser.driver.execute_script(
            'window.scrollTo(0, document.body.scrollHeight);')
        sleep(1)


def follow_and_like_by_tag(tag, no):
    print('following and liking {} accounts by tag {}'.format(no, tag))
    # browser.visit('https://www.instagram.com/explore/')
    browser.visit('https://www.instagram.com/explore/tags/' + tag + '/')
    if not browser.is_element_present_by_text('Most recent', wait_time=10):
        return
    # for _ in range(ceil(no / 10)):
    #    scroll_down(times=1)
    c = 0
    for a in browser.find_by_tag('a'):
        if '/p/' not in a['href']:
            continue
        if c < 9:
            c += 1
            continue
        if c > no + 9:
            break
        print(c)
        try:
            post_id = get_post_id(a['href'])
            print(post_id)
            a.click()
            if 'Sorry, this page' in browser.html:
                browser.back()
            if not browser.is_element_present_by_text('Close', wait_time=10):
                browser.back()
            if browser.is_element_present_by_text('Follow'):
                browser.find_by_text('Follow').first.click()
                user_id = get_user_id()
                following[user_id] = {
                    'followed_on': datetime.now().strftime(DATE_FORMAT),
                    'liked_posts': {}
                    }
                if browser.is_element_present_by_css('.coreSpriteHeartOpen'):
                    browser.find_by_css('.coreSpriteHeartOpen').first.click()
                    following[user_id]['liked_posts'][post_id] = {
                        'liked_on': datetime.now().strftime(DATE_FORMAT),
                        'tag': tag
                    }
                    c += 1
                print(following[user_id])
                sleep(30)
            if browser.is_element_present_by_text('Follow'):
                browser.find_by_text('Close').first.click()
            else:
                browser.back()
        except Exception as ex:
            print(ex)


def get_followers():
    browser.visit('https://www.instagram.com/{}/'.format(args.username))
    if not browser.is_element_present_by_text(' followers', wait_time=10):
        print('followers element not present!')
        return
    a = browser.find_link_by_partial_text(' followers').first
    count = int(a.find_by_tag('span').first.html.replace(',', ''))
    a.click()
    if not browser.is_element_present_by_text('Followers', wait_time=10):
        print('Followers element not present!')
        return
    sleep(1)
    ul = browser.find_by_tag('ul').last
    for _ in range(ceil(count / 10)):
        li = ul.find_by_tag('li').last
        li.click()
        scroll_down(times=1)
    lis = ul.find_by_tag('li')
    print('{} followers'.format(len(lis)))
    for li in lis:
        user_id = get_username(li.find_by_tag('div').first.find_by_tag(
            'div').first.find_by_tag('a').first['href'])
        followers.append(user_id)


def unfollow(unfaithful):
    if not unfaithful:
        return
    for f in unfaithful:
        browser.visit('https://www.instagram.com/{}/'.format(args.username))
    if not browser.is_element_present_by_text(' following', wait_time=10):
        return
    a = browser.find_link_by_partial_text(' following').first
    count = int(a.find_by_tag('span').first.html.replace(',', ''))
    a.click()
    if not browser.is_element_present_by_text('Following', wait_time=10):
        return
    sleep(1)
    print('{} unfaithful'.format(len(unfaithful)))
    ul = browser.find_by_tag('ul').last
    for c in range(ceil(count / 10)):
        lis = ul.find_by_tag('li')
        for li in list(lis)[c*10:c*10+10]:
            user_id = get_username(li.find_by_tag('div').first.find_by_tag('div').first.find_by_tag('a').first['href'])
            if user_id in unfaithful:
                print('unfollowing {}'.format(user_id))
                li.find_by_tag('div').first.find_by_tag('div').last.find_by_tag('button').first.click()
                following[user_id]['unfollowed_on'] = datetime.now().strftime(DATE_FORMAT)
                sleep(30)
        lis.last.click()
        scroll_down(times=1)


def unfollow_unfaithful(unfaithful):
    if not unfaithful:
        return
    browser.visit('https://www.instagram.com/{}/'.format(args.username))
    if not browser.is_element_present_by_text(' following', wait_time=10):
        return
    a = browser.find_link_by_partial_text(' following').first
    count = int(a.find_by_tag('span').first.html.replace(',', ''))
    a.click()
    if not browser.is_element_present_by_text('Following', wait_time=10):
        return
    sleep(1)
    print('{} unfaithful'.format(len(unfaithful)))
    ul = browser.find_by_tag('ul').last
    for c in range(ceil(count / 10)):
        lis = ul.find_by_tag('li')
        for li in list(lis)[c*10:c*10+10]:
            user_id = get_username(li.find_by_tag('div').first.find_by_tag('div').first.find_by_tag('a').first['href'])
            if user_id in unfaithful:
                print('unfollowing {}'.format(user_id))
                li.find_by_tag('div').first.find_by_tag('div').last.click()
                sleep(2)
                browser.find_by_text('Unfollow').first.click()
                following[user_id]['unfollowed_on'] = datetime.now().strftime(DATE_FORMAT)
                sleep(2)
        lis.last.click()
        scroll_down(times=1)


parser = argparse.ArgumentParser()
parser.add_argument('--username', default='')
parser.add_argument('--password', default='')
parser.add_argument('--tag', required=False)
parser.add_argument('--unfollow', action='store_true', required=False)
parser.add_argument('--days', type=int, default=32)
parser.add_argument('--no', type=int, default=10)
parser.add_argument('--file', default='db.json')
args = parser.parse_args()

print(args)

initial = []
followers = []
following = {}

try:
    with open(args.file, 'r') as f:
        db = json.loads(f.read())
        if 'initial' in db:
            initial = db['initial']
        if 'followers' in db:
            followers = db['followers']
        if 'following' in db:
            following = db['following']
except Exception as ex:
    logging.exception(ex)

print('{} initial'.format(len(initial)))
print('{} followers'.format(len(followers)))
print('{} following'.format(len(following)))

try:
    with Browser('chrome', headless=False, executable_path='./chromedriver.exe') as browser:
        if args.tag:
            login(username=args.username, password=args.password)
            follow_and_like_by_tag(tag=args.tag, no=args.no)
            logout()
        elif args.unfollow:
            login(username=args.username, password=args.password)
            if not len(followers):
                get_followers()
            unfaithful = []
            for f in following:
                if f not in followers and f not in initial:
                    now = datetime.now()
                    if 'followed_on' not in following[f]:
                        following[f]['followed_on'] = now.strftime(DATE_FORMAT)
                    elif (now - datetime.strptime(following[f]['followed_on'], DATE_FORMAT)).days > args.days:
                        unfaithful.append(f)
            unfollow_unfaithful(unfaithful)
            logout()
except Exception as ex:
    logging.exception(ex)
finally:
    print('{} following'.format(len(following)))
    with open(args.file, 'w') as f:
        if len(followers):
            db['followers'] = followers
        if len(following):
            db['following'] = following
        if len(db):
            f.write(json.dumps(db, indent=2))
