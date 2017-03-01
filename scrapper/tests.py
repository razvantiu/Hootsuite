import datetime
import random
import string
import unittest

from time import time

import scrapper
import settings


class ScrapperTestCase(unittest.TestCase):
    def setUp(self):
        self.scrapper = scrapper.Scrapper(interval=settings.interval)

    def tearDown(self):
        self.scrapper = None

    def test_reddit_connection(self):
        assert self.scrapper.reddit.user.me().name == settings.username

    def test_mongo_connection(self):
        assert self.scrapper.mongo_client.server_info() is not None

    def test_subreddits_list(self):
        assert isinstance(self.scrapper.subreddits, list), 'subreddits must be list'

    def test_subreddits_length(self):
        assert len(self.scrapper.subreddits) > 0, 'subreddits must have at least one subreddit'

    def test_interval(self):
        assert isinstance(self.scrapper.interval, int), 'interval must be int'

    def test_interval_timestamp(self):
        now = datetime.datetime.now()
        a_hour_ago = now - datetime.timedelta(hours=1)
        a_hour_ago_timestamp, now_timestamp = self.scrapper.interval_timestamp(now, a_hour_ago)
        assert now_timestamp - a_hour_ago_timestamp == 3600

    def test_submission_save(self):
        subreddit_name = self.scrapper.subreddits[0]
        # get a random key
        submission_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in xrange(6))
        submission_title = 'TestSubmission'
        submission_timestamp = time()
        self.scrapper.submission_save(submission_id, subreddit_name,
                                      submission_title, submission_timestamp)

    def test_comment_save(self):
        subreddit_name = self.scrapper.subreddits[0]
        # get a random key
        comment_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in xrange(6))
        submission_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in xrange(6))
        comment_title = 'TestComment'
        comment_timestamp = time()
        self.scrapper.comment_save(comment_id, submission_id,
                                   subreddit_name, comment_title, comment_timestamp)


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(ScrapperTestCase('test_interval'))
    test_suite.addTest(ScrapperTestCase('test_interval_timestamp'))
    test_suite.addTest(ScrapperTestCase('test_subreddits_list'))
    test_suite.addTest(ScrapperTestCase('test_subreddits_length'))
    test_suite.addTest(ScrapperTestCase('test_reddit_connection'))
    test_suite.addTest(ScrapperTestCase('test_mongo_connection'))
    test_suite.addTest(ScrapperTestCase('test_submission_save'))
    test_suite.addTest(ScrapperTestCase('test_comment_save'))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())
