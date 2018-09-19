from datetime import datetime
import unittest
from services.tweets_extractor import TweetsExtractor

tweets_template = '''<div class="stream-container  " data-max-position="max_position" data-min-position="{min_position}"
> <li class="js-stream-item stream-item stream-item " data-item-id="1041441861913772033" 
id="stream-item-tweet-1041441861913772033" data-item-type="tweet"> <div class="tweet js-stream-tweet 
js-actionable-tweet js-profile-popup-actionable dismissible-content original-tweet js-original-tweet focus" 
data-tweet-id="1041441861913772033" data-item-id="1041441861913772033" 
data-permalink-path="/teknoteacher/status/1041441861913772033" data-conversation-id="1041441861913772033" 
data-tweet-nonce="1041441861913772033-82312372-c022-466f-9c10-bf922d64ab61" data-tweet-stat-initialized="true" 
data-screen-name="teknoteacher" data-name="Alan O'Donohoe" data-user-id="48846301" data-you-follow="false" 
data-follows-you="false" data-you-block="false" data-component-context="tweet"> <div class="context"> </div> <div 
class="content"> <div class="stream-item-header"> <a class="account-group js-account-group js-action-profile 
js-user-profile-link js-nav" href="{account_href}" data-user-id="{account_id}"> <img class="avatar 
js-action-profile-avatar" src="https://pbs.twimg.com/profile_images/881257883572326400/3h4RIEKv_bigger.jpg" alt=""> 
<span class="FullNameGroup"> <strong class="fullname show-popup-with-id u-textTruncate "
 data-aria-label-part="">{account_name}</strong><span>‏</span><span class="UserBadges"></span><span 
class="UserNameBreak">&nbsp;</span></span><span class="username u-dir u-textTruncate" dir="ltr" 
data-aria-label-part="">@<b>teknoteacher</b></span></a> <small class="time"> <a 
href="/teknoteacher/status/1041441861913772033" class="tweet-timestamp js-permalink js-nav js-tooltip" title="2:41 PM 
- 16 Sep 2018" data-conversation-id="1041441861913772033"><span class="_timestamp js-short-timestamp " 
data-aria-label-part="last" data-time="{date}" data-time-ms="1537134063000" data-long-form="true">Sep 16</span></a> 
</small> <div class="ProfileTweet-action ProfileTweet-action--more js-more-ProfileTweet-actions"> <div 
class="dropdown"> <button class="ProfileTweet-actionButton u-textUserColorHover dropdown-toggle js-dropdown-toggle" 
type="button" aria-haspopup="true"> <div class="IconContainer js-tooltip" title="More"> <span class="Icon 
Icon--caretDownLight Icon--small"></span> <span class="u-hiddenVisually">More</span> </div> </button> <div 
class="dropdown-menu is-autoCentered"> <div class="dropdown-caret"> <div class="caret-outer"></div> <div 
class="caret-inner"></div> </div> <ul> <li class="copy-link-to-tweet js-actionCopyLinkToTweet"> <button type="button" 
class="dropdown-link">Copy link to Tweet</button> </li> <li class="embed-link js-actionEmbedTweet" 
data-nav="embed_tweet"> <button type="button" class="dropdown-link">Embed Tweet</button> </li> </ul> </div> </div> 
</div> </div> <div class="js-tweet-text-container"> <p class="TweetTextSize  js-tweet-text tweet-text" lang="en" 
data-aria-label-part="0">{text}</p> </div> <div class="stream-item-footer"> <div 
class="ProfileTweet-actionCountList u-hiddenVisually"> <span class="ProfileTweet-action--reply u-hiddenVisually"> 
<span class="ProfileTweet-actionCount" data-tweet-stat-count="{replies}"> <span 
class="ProfileTweet-actionCountForAria" id="profile-tweet-action-reply-count-aria-1041441861913772033" 
data-aria-label-part="">14 replies</span> </span> </span> <span class="ProfileTweet-action--retweet 
u-hiddenVisually"> <span class="ProfileTweet-actionCount" data-tweet-stat-count="{retweets}"> <span 
class="ProfileTweet-actionCountForAria" id="profile-tweet-action-retweet-count-aria-1041441861913772033" 
data-aria-label-part="">14 retweets</span> </span> </span> <span class="ProfileTweet-action--favorite 
u-hiddenVisually"> <span class="ProfileTweet-actionCount" data-tweet-stat-count="{likes}"> <span 
class="ProfileTweet-actionCountForAria" id="profile-tweet-action-favorite-count-aria-1041441861913772033" 
data-aria-label-part="">97 likes</span> </span> </span> </div> <div class="ProfileTweet-actionList js-actions" 
role="group" aria-label="Tweet actions"> <div class="ProfileTweet-action ProfileTweet-action--reply"> <button 
class="ProfileTweet-actionButton js-actionButton js-actionReply" data-modal="ProfileTweet-reply" type="button" 
aria-describedby="profile-tweet-action-reply-count-aria-1041441861913772033"> <div class="IconContainer js-tooltip" 
title="Reply"> <span class="Icon Icon--medium Icon--reply"></span> <span class="u-hiddenVisually">Reply</span> </div> 
<span class="ProfileTweet-actionCount "> <span class="ProfileTweet-actionCountForPresentation" 
aria-hidden="true">14</span> </span> </button> </div> <div class="ProfileTweet-action ProfileTweet-action--retweet 
js-toggleState js-toggleRt"> <button class="ProfileTweet-actionButton  js-actionButton js-actionRetweet" 
data-modal="ProfileTweet-retweet" type="button" 
aria-describedby="profile-tweet-action-retweet-count-aria-1041441861913772033"> <div class="IconContainer js-tooltip" 
title="Retweet"> <span class="Icon Icon--medium Icon--retweet"></span> <span class="u-hiddenVisually">Retweet</span> 
</div> <span class="ProfileTweet-actionCount"> <span class="ProfileTweet-actionCountForPresentation" 
aria-hidden="true">14</span> </span> </button><button class="ProfileTweet-actionButtonUndo js-actionButton 
js-actionRetweet" data-modal="ProfileTweet-retweet" type="button"> <div class="IconContainer js-tooltip" title="Undo 
retweet"> <span class="Icon Icon--medium Icon--retweet"></span> <span class="u-hiddenVisually">Retweeted</span> 
</div> <span class="ProfileTweet-actionCount"> <span class="ProfileTweet-actionCountForPresentation" 
aria-hidden="true">14</span> </span> </button> </div> <div class="ProfileTweet-action ProfileTweet-action--favorite 
js-toggleState"> <button class="ProfileTweet-actionButton js-actionButton js-actionFavorite" type="button" 
aria-describedby="profile-tweet-action-favorite-count-aria-1041441861913772033"> <div class="IconContainer 
js-tooltip" title="Like"> <span role="presentation" class="Icon Icon--heart Icon--medium"></span> <div 
class="HeartAnimation"></div> <span class="u-hiddenVisually">Like</span> </div> <span 
class="ProfileTweet-actionCount"> <span class="ProfileTweet-actionCountForPresentation" aria-hidden="true">97</span> 
</span> </button><button class="ProfileTweet-actionButtonUndo ProfileTweet-action--unfavorite u-linkClean 
js-actionButton js-actionFavorite" type="button"> <div class="IconContainer js-tooltip" title="Undo like"> <span 
role="presentation" class="Icon Icon--heart Icon--medium"></span> <div class="HeartAnimation"></div> <span 
class="u-hiddenVisually">Liked</span> </div> <span class="ProfileTweet-actionCount"> <span 
class="ProfileTweet-actionCountForPresentation" aria-hidden="true">97</span> </span> </button> </div> </div> </div> 
</div> </div> </li> '''

expected_hashtags = ['#test1', '#test2']
expected_text = 'some text ' + ' '.join(expected_hashtags) + ' some text'

expected_data = {
    'min_position': 'expected_min_position',
    'text': '<b>%s</b>' % expected_text,
    'likes': 1,
    'replies': 2,
    'retweets': 3,
    'date': 1537134063,
    'account_id': 123,
    'account_name': 'expected full name',
    'account_href': '/href_expected'

}


class TweetsExtractorTestCase(unittest.TestCase):
    def setUp(self):
        self.extractor = TweetsExtractor()

    def test_extract_tweets(self):
        test_data = tweets_template.format(**expected_data)
        result = self.extractor.extract_tweets(test_data, True)
        self.assertEqual(expected_data['min_position'], result.min_position)
        tweet = result.tweets[0]
        self.assertEqual(expected_data['likes'], tweet.likes)
        self.assertEqual(expected_data['replies'], tweet.replies)
        self.assertEqual(expected_data['retweets'], tweet.retweets)

        self.assertEqual(expected_text, tweet.text)
        self.assertEqual(expected_hashtags, tweet.hashtags)

        self.assertEqual(datetime.utcfromtimestamp(expected_data['date']), tweet.date)

        self.assertEqual(expected_data['account_id'], tweet.account.id)
        self.assertEqual(expected_data['account_href'], tweet.account.href)
        self.assertEqual(expected_data['account_name'], tweet.account.fullname)
