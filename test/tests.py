import os
import sys
sys.path.append("../")
import unittest
from unittest import TestCase
import urllib2
from gitwatch import *

class GithubRepoTextCase(TestCase):

    def get_valid_data(self):
        return {
            "id": 123,
            "name": "test-repo",
            "description": "This is a Test",
            "full_name": "tester/test_repo",
            "private": False,
            "owner": {
                "login": "tester"
            }
        }

    def test_invalid_data(self):
        repo = GithubRepo({"name":"test"})
        self.assertFalse(repo.valid)
        repo = GithubRepo(self.get_valid_data())
        self.assertTrue(repo)

    def test_print(self):
        repo = GithubRepo(self.get_valid_data())
        self.assertEqual(str(repo), "test-repo (tester)")
        repo.private = True
        self.assertEqual(str(repo), "*test-repo (tester)")

def get_test_info_manager():
    manager = InformationManager(".test-file")
    manager.remove()
    return manager

class AccessTokenTestCase(TestCase):

    def setUp(self):
        self.manager = get_test_info_manager()

    def tearDown(self):
        self.manager.remove()
        self.assertFalse(os.path.exists(self.manager.file_path()))

    def test_no_file(self):
        self.assertFalse(os.path.exists(self.manager.file_path()))
        f = self.manager._get_or_create_auth_file()
        f.close()
        self.assertTrue(os.path.exists(self.manager.file_path()))

    def test_pickle_token(self):
        token = self.manager.load_token()
        self.assertEqual(self.manager.load_token(), "", "Token should default to be None")
        self.manager.save_token("12345")
        self.assertEqual(self.manager.load_token(), "12345")

    def test_pickle_username(self):
        self.assertEqual(self.manager.load_username(), "", "User name should default to None")
        self.manager.save_username("tester")
        self.assertEqual(self.manager.load_username(), "tester")

    def test_pickle_unknown_key(self):
        self.assertEqual(self.manager._load_key("unknown"), None, "No value for unknown key")
        self.manager._save("unknown", "Please Save!")
        self.assertEqual(self.manager._load_key("unknown"), None, "Save should not occur for unknown key")

    def test_save_and_load(self):
        self.assertEqual("", self.manager.load_username())
        self.manager.save_username("tester")
        self.assertEqual("tester", self.manager.load_username(), "Reloading instantly should return the name")
        self.manager = InformationManager(".test-file")
        self.assertEqual("tester", self.manager.load_username(), "Reloading instantly should return the name")


class AuthTokenHTTPHandler(urllib2.BaseHandler):
    def __init__(self):
        self.handler_order = 100

    def http_open(self, req):
        if req.get_full_url() == "https://api.github.com/authorizations":
            response_file = "test_data/bad_auth_response.json"
            if req.headers["Authorization"] == "Basic dGVzdGVyOnRlc3QxMjM=":
                response_file = "test_data/good_auth_response.json"
            resp = urllib2.addinfourl(open(response_file, "r"), "mock message", req.get_full_url())
            resp.code = 200
            resp.msg = "OK"
            return resp

    https_open = http_open

class SubscriptionHTTPHandler(urllib2.BaseHandler):
    def __init__(self):
        self.handler_order = 100

    def http_open(self, req):
        if req.get_full_url() == "blah":
            response_file = "test_data/bad_subscription_response.json"
            resp = urllib2.addinfourl(open(response_file, "r"), "mock message", req.get_full_url())
            resp.code = 200
            resp.msg = "OK"
            return resp


auth_http_opener = urllib2.build_opener(AuthTokenHTTPHandler)
subscription_http_opener = urllib2.build_opener(SubscriptionHTTPHandler)


class GitWatchTestCase(TestCase):

    def setUp(self):
        self.manager = get_test_info_manager()

    def tearDown(self):
        self.manager.remove()
        self.assertFalse(os.path.exists(self.manager.file_path()))

    def test_init(self):
        git_watch = GitWatch(self.manager)
        self.assertEqual(git_watch.token, "")
        self.assertEqual(git_watch.username, "")

        self.manager.save_token("12345")
        self.manager.save_username("spember")
        git_watch = GitWatch(self.manager)
        self.assertEqual(git_watch.token, "12345")
        self.assertEqual(git_watch.username, "spember")

    def test_load_info(self):
        git_watch = GitWatch(self.manager)

        #mock creds
        git_watch.username = "spember"
        git_watch.password = "secret"

    def test_get_auth_token(self):

        git_watch = GitWatch(self.manager)
        urllib2.install_opener(auth_http_opener)

        token = git_watch.get_auth_token("tester", "test123")
        self.assertEqual(token, "testToken123", "On a correct response, should return the token")

        token = git_watch.get_auth_token("tester", "test456")
        self.assertEqual(token, None, "On a bad response, get_auth_token should return None")
        urllib2._opener = None

    def test_build_subscription_url(self):

        git_watch = GitWatch(self.manager)

        self.assertIsNone(git_watch.build_subscription_url(1), "Should return None if missing parameters ")
        git_watch.username = "spember"
        self.assertIsNone(git_watch.build_subscription_url(1), "Should return None if missing parameters ")
        git_watch.username = ""
        git_watch.token = "testToken123"
        self.assertIsNone(git_watch.build_subscription_url(1), "Should return None if missing parameters ")

        git_watch.token = "testToken123"
        git_watch.username = "tester"

        #now, test for real
        page = 1
        self.assertEqual("https://api.github.com/users/tester/subscriptions?access_token=testToken123&page={0}&per_page={1}".format(page, git_watch.subscription_page_size),
                         git_watch.build_subscription_url(page))
        git_watch.subscription_page_size=100
        self.assertEqual("https://api.github.com/users/tester/subscriptions?access_token=testToken123&page={0}&per_page={1}".format(page, git_watch.subscription_page_size),
                         git_watch.build_subscription_url(page))


    def test_get_current_subscriptions(self):
        self.assertEqual(1,1)


if __name__ == '__main__':
    unittest.main()




