import praw

import datastore


def rate_links(reddit, links):
    print('Rating links')


def get_risky_link(links):
    top_link = {'Score': 0}

    for link in links:
        if link['Score'] > top_link['Score']:
            top_link = link

    return top_link
