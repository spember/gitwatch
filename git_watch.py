#!/usr/bin/env python
import optparse
import os
import json
import urllib2
import base64
import getpass
import pickle
import traceback


"""
{
        "archive_url":"https://api.github.com/repos/cantinac/matchMedia.js/{archive_format}{/ref}",
        "assignees_url":"https://api.github.com/repos/cantinac/matchMedia.js/assignees{/user}",
        "blobs_url":"https://api.github.com/repos/cantinac/matchMedia.js/git/blobs{/sha}",
        "branches_url":"https://api.github.com/repos/cantinac/matchMedia.js/branches{/branch}",
        "clone_url":"https://github.com/cantinac/matchMedia.js.git",
        "collaborators_url":"https://api.github.com/repos/cantinac/matchMedia.js/collaborators{/collaborator}",
        "comments_url":"https://api.github.com/repos/cantinac/matchMedia.js/comments{/number}",
        "commits_url":"https://api.github.com/repos/cantinac/matchMedia.js/commits{/sha}",
        "compare_url":"https://api.github.com/repos/cantinac/matchMedia.js/compare/{base}...{head}",
        "contents_url":"https://api.github.com/repos/cantinac/matchMedia.js/contents/{+path}",
        "contributors_url":"https://api.github.com/repos/cantinac/matchMedia.js/contributors",
        "created_at":"2013-01-16T16:46:33Z",
        "description":"matchMedia polyfill for testing media queries in JS",
        "downloads_url":"https://api.github.com/repos/cantinac/matchMedia.js/downloads",
        "events_url":"https://api.github.com/repos/cantinac/matchMedia.js/events",
        "fork":true,
        "forks":0,
        "forks_count":0,
        "forks_url":"https://api.github.com/repos/cantinac/matchMedia.js/forks",
        "full_name":"cantinac/matchMedia.js",
        "git_commits_url":"https://api.github.com/repos/cantinac/matchMedia.js/git/commits{/sha}",
        "git_refs_url":"https://api.github.com/repos/cantinac/matchMedia.js/git/refs{/sha}",
        "git_tags_url":"https://api.github.com/repos/cantinac/matchMedia.js/git/tags{/sha}",
        "git_url":"git://github.com/cantinac/matchMedia.js.git",
        "has_downloads":true,
        "has_issues":false,
        "has_wiki":true,
        "homepage":"",
        "hooks_url":"https://api.github.com/repos/cantinac/matchMedia.js/hooks",
        "html_url":"https://github.com/cantinac/matchMedia.js",
        "id":7649549,
        "issue_comment_url":"https://api.github.com/repos/cantinac/matchMedia.js/issues/comments/{number}",
        "issue_events_url":"https://api.github.com/repos/cantinac/matchMedia.js/issues/events{/number}",
        "issues_url":"https://api.github.com/repos/cantinac/matchMedia.js/issues{/number}",
        "keys_url":"https://api.github.com/repos/cantinac/matchMedia.js/keys{/key_id}",
        "labels_url":"https://api.github.com/repos/cantinac/matchMedia.js/labels{/name}",
        "language":"JavaScript",
        "languages_url":"https://api.github.com/repos/cantinac/matchMedia.js/languages",
        "merges_url":"https://api.github.com/repos/cantinac/matchMedia.js/merges",
        "milestones_url":"https://api.github.com/repos/cantinac/matchMedia.js/milestones{/number}",
        "mirror_url":null,
        "name":"matchMedia.js",
        "notifications_url":"https://api.github.com/repos/cantinac/matchMedia.js/notifications{?since,all,participating}",
        "open_issues":0,
        "open_issues_count":0,
        "owner":{
            "avatar_url":"https://secure.gravatar.com/avatar/adfc1989e9ddae0da22ee68335c904f8?d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-org-420.png",
            "events_url":"https://api.github.com/users/cantinac/events{/privacy}",
            "followers_url":"https://api.github.com/users/cantinac/followers",
            "following_url":"https://api.github.com/users/cantinac/following",
            "gists_url":"https://api.github.com/users/cantinac/gists{/gist_id}",
            "gravatar_id":"adfc1989e9ddae0da22ee68335c904f8",
            "id":259899,
            "login":"cantinac",
            "organizations_url":"https://api.github.com/users/cantinac/orgs",
            "received_events_url":"https://api.github.com/users/cantinac/received_events",
            "repos_url":"https://api.github.com/users/cantinac/repos",
            "starred_url":"https://api.github.com/users/cantinac/starred{/owner}{/repo}",
            "subscriptions_url":"https://api.github.com/users/cantinac/subscriptions",
            "type":"Organization",
            "url":"https://api.github.com/users/cantinac"
        },
        "private":false,
        "pulls_url":"https://api.github.com/repos/cantinac/matchMedia.js/pulls{/number}",
        "pushed_at":"2012-07-27T15:55:36Z",
        "size":136,
        "ssh_url":"git@github.com:cantinac/matchMedia.js.git",
        "stargazers_url":"https://api.github.com/repos/cantinac/matchMedia.js/stargazers",
        "statuses_url":"https://api.github.com/repos/cantinac/matchMedia.js/statuses/{sha}",
        "subscribers_url":"https://api.github.com/repos/cantinac/matchMedia.js/subscribers",
        "subscription_url":"https://api.github.com/repos/cantinac/matchMedia.js/subscription",
        "svn_url":"https://github.com/cantinac/matchMedia.js",
        "tags_url":"https://api.github.com/repos/cantinac/matchMedia.js/tags{/tag}",
        "teams_url":"https://api.github.com/repos/cantinac/matchMedia.js/teams",
        "trees_url":"https://api.github.com/repos/cantinac/matchMedia.js/git/trees{/sha}",
        "updated_at":"2013-01-16T16:47:19Z",
        "url":"https://api.github.com/repos/cantinac/matchMedia.js",
        "watchers":0,
        "watchers_count":0
    }
"""

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
        except KeyError as ke:
            self.valid = False
        return self.valid

    def __str__(self):
        return "{0}{1}".format(self.name, "*" if self.private else "")

class InformationManager(object):
    TOKEN_KEY = "token"
    USERNAME_KEY = "username"

    def __init__(self, token_path=".github_token"):
        self.pickled_token_path=token_path

    def file_path(self):
        return os.getcwd() +"/" +self.pickled_token_path

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

    def __init__(self, alternate_manager=None):
        self.token = None
        self.username = None

        if alternate_manager:
            self.info_manager = alternate_manager

        else:
            self.info_manager = InformationManager()
        self.token = self.info_manager.load_token()
        self.username = self.info_manager.load_username()


    def setup(self):
        if self.token == "":
            username, password = self.obtain_credentials(self.username)
            if username != self.username:
                self.info_manager.save_username(username)
                self.username = username
            self.token = self.get_auth_token(self.username, password)
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

    def get_subscriptions(self):
        data = self.open_http_json_request(self.build_subscription_url())
        return data

    def build_subscription_url(self):
        url = None
        if self.username and self.token:
            url = "{0}users/{1}/subscriptions?access_token={2}".format(self.github_api_url_root,
                    self.username, self.token)
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
            print "Unable to connect to {0}: {1}".format(url.get_full_url(), traceback.format_exc(0))
        return data

    def main(self):
        self.setup()




def main():
    #https://api.github.com/users/:user/subscriptions
    #908ee2ce2ce2e93a1d19254bcb2872db7d64ffe1

    """
        -check authtoken for existing token
        -check if current token is valid
        -otherwise login
    """
    """
    manager = InformationManager()
    token = manager.load_token()
    if token:
        print "Using token of {0}, no need to re-login".format(token)
    else:
        username, password = obtain_credentials()
        print "Attempting login for user " +str(username)
        token = get_auth_token(username, password)
        if (token == None):
            print "No token found!"
            return False
        else:
            print "Token: " +str(token)
            manager.save_token(token)
    print "Looking for subscriptions:"
    data = get_subscriptions(token)
    print "Here are your subscriptions:"
    for x in xrange(len(data)):
        print "{2}, {0}, '{1}'".format(data[x]['name'], data[x]['description'], x)
    """

#def pretty_print(json_data):
#    print json.dumps(json_data, sort_keys=True, indent=4, separators=(",", ":"))


if __name__ == '__main__':
    GitWatch().main()

