import logging
import json
import sys

import praw

import datastore
import link_scanner as scanner
import link_rater as rater

SCAN_TIME_HOURS = 0.01


def main():
    # Connect to Reddit
    auth = json.load(open('auth.json'))
    reddit = praw.Reddit(username=auth['reddit']['username'],
                         password=auth['reddit']['password'],
                         client_id=auth['reddit']['app_id'],
                         client_secret=auth['reddit']['secret'],
                         user_agent=auth['reddit']['user_agent']
                         )
    logger.info("Connected to Reddit as: %s", str(reddit.user.me()))

    # Connect to datastore and empty
    db = datastore.connect_datastore()
    datastore.clear_datastore(db)
    logger.info('Connected to datastore')

    # Collect links for SCAN_TIME_HOURS
    logger.info('Scanning for links for %f hours', SCAN_TIME_HOURS)
    scanner.scan_for_risky_links(db, reddit, SCAN_TIME_HOURS)

    # Go through each discovered link and score it based on upvotes
    links = datastore.get_all_links(db)
    logger.info('Rating %i links', len(links))
    if not links:
        logger.info('Terminating due to no risky links being found')
        return
    links = rater.rate_links(reddit, links)

    # Get riskiest click and post it as Risky Click of the Day
    top_link = rater.get_risky_link(links)
    print('The Risky click of the day is: %s', top_link['Link'])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s: %(message)s',
                        filename='logs.log',
                        filemode='w')
    logging.getLogger().addHandler(logging.StreamHandler())
    logger = logging.getLogger(__name__)
    main()
