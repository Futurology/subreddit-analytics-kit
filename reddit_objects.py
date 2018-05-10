import praw
import psraw
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


class Reddit(object):
    """
    Provides functionality to interact with praw which wraps the Reddit API
    """

    def __init__(self, subreddit='futurology'):
        self.client_id = config['REDDITAPI']['client_id']
        self.client_secret = config['REDDITAPI']['client_secret']
        self.username = config['REDDITAPI']['username']
        self.password = config['REDDITAPI']['password']
        self.user_agent = config['REDDITAPI']['user_agent']
        self.subreddit = subreddit

        self.reddit = praw.Reddit(client_id=self.client_id,
                                  client_secret=self.client_secret,
                                  username=self.username,
                                  password=self.password,
                                  user_agent=self.user_agent)
        self.subreddit = self.reddit.subreddit(subreddit)

    def hot_posts(self, limit=5):
        """
        Top posts sorted by hot on the sub.
        :param limit: number of posts to return defaults to 5
        :return: generator containing post objects
        """
        return self.subreddit.hot(limit=limit)

    def new_posts(self, limit=5):
        """
        Top posts sorted by new on the sub.
        :param limit: number of posts to return defaults to 5
        :return: generator containing post objects
        """
        return self.subreddit.new(limit=limit)

    def get_user(self, name):
        user = self.reddit.redditor(name=name)
        return user

    def list_of_top_content_from_user(self, name):
        user = self.get_user(name)
        return [content for content in user.top()]
