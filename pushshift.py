import requests
import datetime
import time


def main():
    # # Setting search in init - only works with perfectly formatted terms
    # ps = PushshiftAPI(subreddit='futurology',
    #                   start_date=datetime.date(2018, 3, 1),
    #                   end_date=datetime.date(2018, 3, 7),
    #                   )
    # print(ps.run())
    # ps = PushshiftAPI()

    # Setting search in set_search-terms_with_kwargs()
    ps = SubmissionPushshiftAPI()
    ps.set_search_terms_with_kwargs(subreddit='futurology',
                                    start_date=datetime.date(2018, 3, 1),
                                    end_date=datetime.date(2018, 3, 7),
                                    )
    print(ps.run())

    ## Setting search with class methods
    # ps = CommentsPushshiftAPI()
    # ps.set_subreddit('futurology')
    # ps.set_start_date(datetime.date(2018, 3, 1))
    # ps.set_end_date(datetime.date(2018, 3, 7))
    # print(ps.run())


class BasePushshiftAPI(object):
    """
    Wrapper on pushshift api - https://github.com/pushshift/api
    """
    def __init__(self, **kwargs):
        self.search_text = None
        self.num_results = None
        self.fields = None
        self.sort = None
        self.sort_type = None
        self.aggregate_on = None
        self.redditor = None
        self.subreddit = None
        self.start_date = None
        self.end_date = None
        self.agg_frequency = None

        self.url_start = None
        self.url = self.get_search_string()

        self.set_search_terms_with_kwargs(**kwargs)

    def reset_search_terms(self):
        """
        Sets all search terms to None
        :return: None
        """
        for key in self.__dict__.keys():
            self.__setattr__(key, None)

    @staticmethod
    def get_term_map():
        """
        A dict containing friendly term name to API term name mappings in a dict.
        :return: dict
        """
        mapping = {'search_text': 'q',
                   'num_results': 'size',
                   'fields': 'fields',
                   'sort': 'sort',
                   'sort_type': 'sort_type',
                   'aggregate_on': 'aggs',
                   'redditor': 'author',
                   'subreddit': 'subreddit',
                   'start_date': 'after',
                   'end_date': 'before',
                   'agg_frequency': 'frequency'
                   }
        return mapping

    def get_search_string(self):
        url = self.url_start
        term_map = self.get_term_map()
        for key, value in self.__dict__.items():
            if key in term_map.keys() and value:
                url = f'{url}&{term_map[key]}={value}'
        return url

    def set_search_terms_with_kwargs(self, **kwargs):
        # Just does a simple key value search.
        # Needs to have case conditions for keys that don't exist.
        for key, value in kwargs.items():
            # print("%s = %s" % (key, value))
            try:
                var_set_function = getattr(self, 'set_' + key)
                var_set_function(value)
            except AttributeError:
                print(key + ' has no set method.')
        self.url = self.get_search_string()

    def run(self):
        self.url = self.get_search_string()
        return requests.get(self.url).json()['data']

    def set_search_text(self, search_text):
        self.search_text = f'"{search_text}"'

    def set_size(self, num_results):
        self.num_results = str(num_results)

    def set_fields(self, fields):
        self.fields = fields

    def set_sort(self, fields):
        self.fields = fields

    def set_sort_type(self, sort_type):
        self.sort_type = sort_type

    def set_aggregate_on(self, aggregate_on):
        self.aggregate_on = aggregate_on

    def set_redditor(self, redditor):
        self.redditor = redditor

    def set_subreddit(self, subreddit):
        self.subreddit = subreddit

    def set_start_date(self, start_date):
        if isinstance(start_date, datetime.date):
            self.start_date = str(int(time.mktime(start_date.timetuple())))
        else:
            self.start_date = start_date
        self.url = self.get_search_string()

    def set_end_date(self, end_date):
        if isinstance(end_date, datetime.date):
            self.end_date = str(int(time.mktime(end_date.timetuple())))
        else:
            self.end_date = end_date
        self.url = self.get_search_string()

    def set_agg_frequency(self, agg_frequency):
        self.agg_frequency = agg_frequency


class CommentsPushshiftAPI(BasePushshiftAPI):
    """
    Wrapper on pushshift api - https://github.com/pushshift/api
    """

    def __init__(self, **kwargs):
        self.comment_ids = None

        BasePushshiftAPI.__init__(self, **kwargs)

        self.url_start = 'https://api.pushshift.io/reddit/comment/search?'
        self.url = self.get_search_string()

    def get_term_map(self):
        """
        A dict containing friendly term name to API term name mappings in a dict.
        :return: dict
        """
        super_mapping = BasePushshiftAPI.get_term_map()
        mapping = {'comment_ids': 'ids'
                   }
        return {**super_mapping, **mapping}

    def set_comment_ids(self, comment_ids):
        self.comment_ids = comment_ids

class SubmissionPushshiftAPI(BasePushshiftAPI):
    """
    Wrapper on pushshift api - https://github.com/pushshift/api
    """

    def __init__(self, **kwargs):
        self.submission_ids = None
        self.exclude_text = None
        self.self_text_search = None
        self.self_text_exclude = None
        self.score = None
        self.num_comments = None
        self.over_18 = None
        self.is_video = None
        self.locked = None
        self.stickied = None
        self.spoiler = None
        self.contest_mode = None

        BasePushshiftAPI.__init__(self, **kwargs)

        self.url_start = 'https://api.pushshift.io/reddit/search/submission/?'
        self.url = self.get_search_string()

    def get_term_map(self):
        """
        A dict containing friendly term name to API term name mappings in a dict.
        :return: dict
        """
        super_mapping = BasePushshiftAPI.get_term_map()
        mapping = {'submission_ids': 'ids',
                   'exclude_text': 'q:not',
                   'title': 'title',
                   'exclude_title': 'title:not',
                   'self_text_serch': 'selftext',
                   'self_text_exclude': 'selftext:not',
                   'score': 'score',
                   'num_comments': 'num_comments',
                   'over_18': 'over_18',
                   'is_video': 'is_video',
                   'locked': 'locked',
                   'stickied': 'stickied',
                   'spoiler': 'spoilder',
                   'contest_mode': 'contest_mode'
                   }
        return {**super_mapping, **mapping}

    def set_submission_ids(self, submission_ids):
        self.submission_ids = submission_ids

    def set_exclude_text(self, exclude_text):
        self.exclude_text = f'"{exclude_text}"'

    def set_self_text_search(self, self_text_search):
        self.self_text_search = f'"{self_text_search}"'

    def set_self_text_exclude(self, self_text_exclude):
        self.self_text_exclude = f'"{self_text_exclude}"'

    def set_score(self, score):
        self.score = str(score)

    def set_num_comments(self, num_comments):
        self.num_comments = str(num_comments)

    def set_over_18(self, over_18):
        self.over_18 = over_18

    def set_is_video(self, is_video):
        self.is_video = is_video

    def set_locked(self, locked):
        self.locked = locked

    def set_stickied(self, stickied):
        self.stickied = stickied

    def set_spoiler(self, spoiler):
        self.spoiler = spoiler

    def set_conetst_mode(self, contest_mode):
        self.contest_mode = contest_mode


if __name__ == '__main__':
    main()
