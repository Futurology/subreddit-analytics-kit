import json
import urllib
from calendar import monthrange
# import pandas as pd
import time
import datetime


def main():
    ps = PushshiftAPI()
    ps.set_search_terms(subreddit='futurology',
                        start_date=datetime.date(2018, 3, 1),
                        end_date=datetime.date(2018, 3, 1),
                        )
    rquery = ps.run()
    print(rquery)


class PushshiftAPI:
    """
    Wrapper on pushshift api - https://github.com/pushshift/api
    """
    def __init__(self, search_term=None, comment_ids=None, size=25, fields=None, sort='desc',
                 sort_type='created_utc', aggregate_on=None, redditor=None, subreddit=None, start_date=None,
                 end_date=None, frequency=None):
        self.search_term = search_term
        self.comment_ids = comment_ids
        self.size = size
        self.fields = fields
        self.sort = sort
        self.sort_type = sort_type
        self.aggregate_on = aggregate_on
        self.redditor = redditor
        self.subreddit = subreddit
        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency
        self.url_start = 'https://api.pushshift.io/reddit/search/submission?'

    def reset_search_terms(self):
        """
        Resets the values of all search term to their defaults.
        :return: None
        """
        self.search_term = None
        self.comment_ids = None
        self.size = 25
        self.fields = None
        self.sort = 'desc'
        self.sort_type = 'created_utc'
        self.aggregate_on = None
        self.redditor = None
        self.subreddit = None
        self.start_date = None
        self.end_date = None
        self.frequency = None

    # I think we could abstract this if we want to be more pythonic.
    # Also, each field needs data sanatation / string conversion.
    def get_search_string(self):
        url = self.url_start
        if self.search_term:
            url = url + '&q=' + self.search_term
        if self.comment_ids:
            url = url + '&ids=' + str(self.comment_ids)
        if self.size:
            url = url + '&size=' + str(self.size)
        if self.fields:
            url = url + '&fields=' + self.fields
        if self.sort:
            url = url + '&sort=' + self.sort
        if self.sort_type:
            url = url + '&sort_type=' + self.sort_type
        if self.aggregate_on:
            url = url + '&aggs=' + self.aggregate_on
        if self.redditor:
            url = url + '&author=' + self.redditor
        if self.subreddit:
            url = url + '&subreddit=' + self.subreddit
        if self.start_date:
            url = url + '&after=' + self.start_date
        if self.end_date:
            url = url + '&before=' + self.end_date
        self.url = self.url_start
        return url

    def set_search_terms(self, **kwargs):
        # Just does a simple key value search.
        # Needs to have case conditions for keys that don't exist.
        for key, value in kwargs.iteritems():
            # print("%s = %s" % (key, value))
            self.key = value

        # self.search_term = str(search_term)

    # What does this do?
    def set_comment_ids(self, comment_ids):
        self.comment_ids = comment_ids

    # RUN THE search
    def run(self):
        Subm_Arr = []
        url = self.get_search_string()
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        rdata = data['data']
        for post in rdata:
            Subm_Arr.append(post)
        return Subm_Arr


"""
def getData(UTstart, UTend):
    url = 'https://api.pushshift.io/reddit/search/submission?&size=1000&after='+str(UTstart)+'&before='+str(UTend)+'&subreddit=futurology'
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    rdata = data['data']
    for post in rdata:
        Subm_Arr.append(post)


def getMonthlyData(month, year):
    days = monthrange(year, month)
    #print days[1]
    for day in range(1,days[1]):
        for hour in range(0,23):
            t_start = datetime.datetime(2018,month,day,hour,0)
            print('t_start: ' + str(t_start))
            ut_start = int(time.mktime(t_start.timetuple()))
            print('ut_start: ' + str(ut_start))
            t_end = datetime.datetime(2018,month,day,hour+1,0)
            ut_end = int(time.mktime(t_end.timetuple()))
            getData(ut_start, ut_end)
            print('Day: '+str(month)+'/'+str(day)+'/'+str(year)+', hour:'+str(hour))


getMonthlyData(1, 2018)
getMonthlyData(2, 2018)
getMonthlyData(3, 2018)

# #print Subm_Arr
# df_posts = pd.DataFrame(Subm_Arr)
# file_Name = "2018_01-03_Futurology.tsv"
# df_posts.to_csv(file_Name, sep='\t', header=True, encoding='utf-8')
"""

if __name__ == '__main__':
    main()
