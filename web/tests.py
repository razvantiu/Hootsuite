import unittest

from time import time

from pymongo import MongoClient

import webserver
import settings


class WebServerTestCase(unittest.TestCase):
    def setUp(self):
        self.client = webserver.app.test_client()

    def tearDown(self):
        self.client = None

    def test_invalid_param_subreddit(self):
        response = self.client.get('/items?from=0&to=' + str(time()))
        assert response.status_code == 400

    def test_invalid_param_from(self):
        response = self.client.get('/items?subreddit=AskReddit&from=test&to=' + str(time()))
        assert response.status_code == 400

    def test_invalid_param_to(self):
        response = self.client.get('/items?subreddit=AskReddit&from=0&to=test')
        assert response.status_code == 400

    def test_valid_request(self):
        response = self.client.get('/items?subreddit=AskReddit&from=0&to=' + str(time()))
        assert response.status_code == 200

    def test_post_method(self):
        response = self.client.post('/items?subreddit=AskReddit&from=0&to=' + str(time()))
        assert response.status_code == 405

    @staticmethod
    def test_mongo_connection():
        mongo_client = MongoClient(settings.database_ip, settings.database_port)
        assert mongo_client.server_info() is not None


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(WebServerTestCase('test_invalid_param_subreddit'))
    test_suite.addTest(WebServerTestCase('test_invalid_param_from'))
    test_suite.addTest(WebServerTestCase('test_invalid_param_to'))
    test_suite.addTest(WebServerTestCase('test_valid_request'))
    test_suite.addTest(WebServerTestCase('test_post_method'))
    test_suite.addTest(WebServerTestCase('test_mongo_connection'))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())
