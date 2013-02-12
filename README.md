# gitwatch

I realized the other day that I was subscribed to ~100 Github repos. That in itself isn't a problem, but I was being
inundated with email notifications, often for things I didn't particularly care about. I couldn't find a way to bulk
unwatch from those I wasn't currently active in, so I figured I'd write a small tool to help me. Thus, git-watch.

This small command line utility will allow a user to view the full list of repos that they're watching, and unsubscribe
from them at will.

### Installation

Download gitwatch and place it on your path. Mark it as executable

### Usage

First, you must supply your username and password. This information is used to obtain an access
token from Github, at which point the username and access token are saved for later use.

After discovering the access token, the repositories the user is currently subscribed to will be listed. Each repo will be
labeled with a number. After listing the repos, the user will be prompted to either quit (by typing q or quit) or
entering one or many numerical values corresponding to the numerical labels for each repo. Those repos selected will be
unsubscribed from, at which point the list will be redisplayed (although sans those repos chosen in the previous step).


### Requirements

Python 2.x (although I've only tested it on 2.7 on a Mac OS X Mountain Lion)