import time

import datastore

RISKY_WORDS = [
    'risky',
]

LINK_WORDS = [
    'link',
    'click',
    'website',
    'url',
]


def is_risky(comment):
    text = comment.body.lower()

    for adjective in RISKY_WORDS:
        for noun in LINK_WORDS:
            risk_text = adjective + ' ' + noun
            if risk_text in text:
                return True

    return False


def scan_for_risky_links(db, reddit, scan_time):
    subreddit = reddit.subreddit('all')
    start_time = time.time()

    for comment in subreddit.stream.comments():
        if is_risky(comment):
            datastore.insert_link(db, comment.parent_id)
        elapsed_time = time.time() - start_time
        if elapsed_time/3600 >= scan_time:
            break
