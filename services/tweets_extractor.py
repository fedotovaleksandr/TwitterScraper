import re
from datetime import datetime
from bs4 import BeautifulSoup
from model.account import Account
from model.tweet import Tweet


class TweetExtractorResult:
    tweets: [Tweet]
    min_position: str

    def __init__(self, tweets: [Tweet], minPosition: str):
        self.tweets = tweets
        self.min_position = minPosition


class TweetsExtractor:
    def extract_tweets(self, content: str, limit: int = None, search_min_pos: bool = True) -> TweetExtractorResult:
        tweets_list = []
        soup = BeautifulSoup(content, 'lxml')
        tweets = soup.find_all('div', class_='js-stream-tweet')
        for tweetContent in tweets:
            tweet = None
            try:
                tweet = self._extract_tweet(tweetContent)
            except Exception as e:
                continue

            if tweet:
                tweets_list.append(tweet)

            if limit and limit <= len(tweets_list):
                break
        min_pos = None
        if search_min_pos:
            min_pos = soup.find("div", class_="stream-container")["data-min-position"]
        return TweetExtractorResult(tweets_list, min_pos)

    def _extract_tweet(self, soup: BeautifulSoup) -> Tweet:
        stats_container = soup.find('div', class_='ProfileTweet-actionCountList')
        stats = self._extract_stats(stats_container)

        header_container = soup.select('div.stream-item-header')[0]
        account = self._extract_account(header_container)

        texts = soup.select('p.TweetTextSize.tweet-text')[0].findAll(text=True)

        tweet = Tweet()
        tweet.retweets = stats['retweet']
        tweet.likes = stats['favorite']
        tweet.replies = stats['reply']
        tweet.text = ''.join(texts)
        tweet.hashtags = re.findall(r"(#\w+)", tweet.text)
        tweet.date = datetime.utcfromtimestamp(
            int(header_container.find('span', class_='_timestamp').attrs['data-time'])
        )
        tweet.account = account

        return tweet

    def _extract_stats(self, stats_container: BeautifulSoup) -> dict:
        stats = {}

        for field in ['retweet', 'favorite', 'reply']:
            selector = 'span.ProfileTweet-action--%s > span.ProfileTweet-actionCount' % field
            stats[field] = int(stats_container.select(selector)[0].attrs['data-tweet-stat-count'])

        return stats

    def _extract_account(self, headerContainer: BeautifulSoup) -> Account:
        account_container = headerContainer.select('a.account-group')[0]
        account_id = int(account_container.attrs['data-user-id'])
        account_href = account_container.attrs['href']
        full_name = headerContainer.select('span.FullNameGroup > strong.fullname')[0].text

        return Account(account_id, full_name, account_href)
