import praw
from reddit_objects import Reddit
import pprint

def main():
    reddit = Reddit()
    content_list = reddit.list_of_top_content_from_user(name='ion-tom')
    pprint.pprint(vars(content_list[0]))

if __name__ == '__main__':
    import configparser

    config = configparser.ConfigParser()
    config.read('config.ini')
    main()
