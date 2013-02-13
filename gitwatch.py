#!/usr/bin/env python
import optparse
import os
import sys
import inspect
import json
import urllib2
import base64
import getpass
import pickle
import traceback
import string
import argparse

_version = 0.1
_name = "gitwatch"

class GithubRepo(object):
    """
    Representation of a Github Repo
    """

    def __init__(self, json=None):
        self.valid = True
        if json:
            self.parse(json)

    def parse(self, json):
        try:
            self.name = json["name"]
            self.full_name = json["full_name"]
            self.private = json["private"]
            self.id = json["id"]
            self.description = json["description"]
            self.owner = json["owner"]["login"]
        except KeyError as ke:
            self.valid = False
        return self.valid

    def __str__(self):
        return "{0}{1} ({2})".format("*" if self.private else "", self.name, self.owner)

class InformationManager(object):
    """
    Wrapper around a dictionary that is pickled into the same folder as this script. Contains methods for storing and
    retrieving the current user name and auth token.
    """
    TOKEN_KEY = "token"
    USERNAME_KEY = "username"

    def __init__(self, token_name=".github_token"):
        self.pickled_token_file_name=token_name

    def file_path(self):
        return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) +"/" +self.pickled_token_file_name

    def _dump_data(self, data):
        f = open(self.file_path(), "w")
        pickle.dump(data, f)
        f.close()

    def _create_auth_file(self, token=""):
        self._dump_data({self.TOKEN_KEY:token, self.USERNAME_KEY:""})

    def _get_or_create_auth_file(self, action="r"):
        if not os.path.exists(self.file_path()):
            self._create_auth_file()
        return open(self.file_path(), action)

    def _load_data(self):
        f = self._get_or_create_auth_file()
        data = pickle.load(f)
        f.close()
        return data

    def _load_key(self, key):
        """Loads a key value"""
        return self._load_data().get(key, None)

    def _save(self, key, value):
        """Pickles the token value"""
        #self._create_auth_file(token)
        data = self._load_data()
        if data.has_key(key):
            data[key] = value
            self._dump_data(data)

    def save_token(self, token):
        self._save(self.TOKEN_KEY, token)

    def load_token(self):
        return self._load_key(self.TOKEN_KEY)

    def load_username(self):
        return self._load_key(self.USERNAME_KEY)

    def save_username(self, username):
        self._save(self.USERNAME_KEY, username)

    def remove(self):
        if os.path.exists(self.file_path()):
            os.remove(self.file_path())


class GitWatch(object):

    github_api_url_root = "https://api.github.com/"
    subscriptions = []
    subscription_page_size = 30

    def __init__(self, alternate_manager=None):
        self.token = None
        self.username = None
        self.subscriptions = []

        if alternate_manager:
            self.info_manager = alternate_manager

        else:
            self.info_manager = InformationManager()
        self.token = self.info_manager.load_token()
        self.username = self.info_manager.load_username()

    def clear(self):
        self.info_manager.remove()

    def setup(self):
        if self.token == "":
            username, password = self.obtain_credentials(self.username)
            if username != self.username:
                self.info_manager.save_username(username)
                self.username = username
            self.token = self.get_auth_token(self.username, password)
        if self.token:
            self.info_manager.save_token(self.token)
            print "Setup Complete. Welcome {0}".format(self.username)

    def obtain_credentials(self, username=None):
        """
        Simple prompt for obtain a github username and password
        """
        if username:
            print "Using stored username {0}".format(username)
        else:
            username = raw_input("GitHub Username: ")
        password = getpass.getpass(prompt="Password: ")
        return (username, password)

    def get_auth_token(self, username, password):
        """
        Given a simple username and password, queries GitHub, looking for the username and password
        """
        #token for accessing our private repo (API)
        token = None
        data = self.open_http_json_request(self.build_http_auth_request(self.github_api_url_root + "authorizations", username, password))
        for d in data:
            if d.has_key("app") and d["app"].get("name", "") == "token for accessing our private repo (API)":
                token = d["token"]
        return token

    def load_subscriptions(self, data):
        for d in data:
            self.subscriptions.append(GithubRepo(d))

    def get_subscriptions(self, page=1):
        response_data = self.open_http_json_request(self.build_subscription_url(page))
        if len(response_data) >= self.subscription_page_size:
            page += 1
            print "Fetching page {0}".format(page)
            return response_data + self.get_subscriptions(page)
        else:
            return response_data


    def build_subscription_url(self, page):
        url = None
        if self.username and self.token:
            url = "{0}users/{1}/subscriptions?access_token={2}&page={3}&per_page={4}".format(self.github_api_url_root,
                    self.username, self.token, page, self.subscription_page_size)
        return url


    def unwatch_repos(self, repo_numbers):
        repo_numbers =  map(int, repo_numbers.split(" "))
        to_remove = []
        for num in repo_numbers:
            to_remove.append(self.subscriptions[num - 1])
        for repo in to_remove:
            print "Unsubscribing from: {0}".format(repo.name)
            result = self.open_http_delete_request(self.build_subscription_delete_url(repo))
            print "Received a " +str(result.code)
            if int(result.code) == 204:
                self.subscriptions.remove(repo)
            else:
                print "Something went wrong"

    def build_subscription_delete_url(self, subscription):
        url = None
        if self.token:
            url = "{0}repos/{1}/{2}/subscription?access_token={3}".format(self.github_api_url_root,
                    subscription.owner, subscription.name, self.token)
        return url

    def build_http_auth_request(self, url, username, password):
        request = urllib2.Request(url)
        base64str = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64str)
        return request

    def open_http_json_request(self, url):
        data = []
        try:
            data = json.load(urllib2.urlopen(url))
        except urllib2.HTTPError as e:
            print "Unable to connect to {0}: {1}".format(url, traceback.format_exc(0))
        except urllib2.URLError:
            print "Unknown URL '{0}'. Please test your internet connection and try again.".format(
                    url.get_full_url() if isinstance(url, urllib2.Request) else url
                )
        return data

    def open_http_delete_request(self, url):
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request(url)
        request.get_method = lambda: 'DELETE'
        return opener.open(request)

    def main(self):
        self.setup()
        if self.token:
            self.load_subscriptions(self.get_subscriptions())
            running = True
            while running:
                print "Your current subscriptions (A '*' denotes a private repo):\n"
                for pos in xrange(len(self.subscriptions)):
                    print "\t{0}: {1}: {2}".format(pos+1, self.subscriptions[pos], self.subscriptions[pos].description)
                choice = string.lower(raw_input("Enter number of repo to unsubscribe, or (q)uit to quit: "))
                if choice == "q" or choice == "quit":
                    running = False
                else:
                    self.unwatch_repos(choice)

#def pretty_print(json_data):
#    print json.dumps(json_data, sort_keys=True, indent=4, separators=(",", ":"))

parser = argparse.ArgumentParser(description='Allows you to view and unwatch your subscribed Github repositories.')
parser.add_argument('-v', '--version', action='version', version="{0} v{1}".format(_name, _version))
parser.add_argument('-c', '--clear', action="store_const", const="clear", help="Deletes the cached username and auth token. Will require you to re-enter your username and password.")


if __name__ == '__main__':
    gw = GitWatch()
    args = parser.parse_args()
    if args.clear:
        print("Removing auth token cache..."),
        gw.clear()
        gw = GitWatch()
        print("Done!")
    gw.main()



