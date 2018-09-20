# TwitterScraper [![Build Status](https://travis-ci.com/fedotovaleksandr/TwitterScraper.svg?branch=master)](https://travis-ci.com/fedotovaleksandr/TwitterScraper)

This is microservice based on open search Open Twitter API (https://twitter.com/search-home).

### Description & sandbox 

This repo configured to automatic CI\CD with Travis and Heroku
Sandbox:
https://twitter-scraper-api.herokuapp.com/ui

CI:
https://travis-ci.com/fedotovaleksandr/TwitterScraper

##### This service provides two api:

1)Get tweets by a hashtag. Get the list of tweets with the given hashtag.
Optional parameters: 
limit: integer, specifies the number of tweets to retrieve, default should be `30`

Example request:

```curl -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://localhost:xxxx/hashtags/Python?limit=40```

Example response:

```
[
    {
        "account": {
           "fullname": "Raymond Hettinger",
           "href": "/raymondh",
           "id": 14159138
        },
        "date": "12:57 PM - 7 Mar 2018",
        "hashtags": ["#python"],
        "likes": 169,
        "replies": 13,
        "retweets": 27,
        "text": "Historically, bash filename pattern matching was known
               as \"globbing\".  Hence, the #python module
               called \"glob\".\n\n
               >>> print(glob.glob('*.py')\n\n
               If the function were being added today, it would probably
               be called os.path.expand_wildcards('*.py') which would be
               less arcane."
    },
  
]
```

2)Get user tweets. Get the list of tweets that user has on his feed in json format. Optional parameters: 
limit: integer, specifies the number of users to retrieve, default should be 30

Example request:

curl -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://localhost:xxxx/users/twitter?limit=20

Example response:

 ```
[
    {
        "account": {
            "fullname": "Twitter",
            "href": "/Twitter",
            "id": 783214
        },
        "date": "2:54 PM - 8 Mar 2018",
        "hashtags": ["#InternationalWomensDay"],
        "likes": 287,
        "replies": 17,
        "retweets": 70,
        "text": "Powerful voices. Inspiring women.\n\n#InternationalWomensDay
                 https://twitter.com/i/moments/971870564246634496"
    },
     ...
] 
```

### Requirments

#### Docker
`docker>=17.12`
`docker-compose>=1.19`

* OR alternative

 `venv` with `python3.6`

### Installation

1) ```docker-compose build```
2) ```docker-compose up -d```

* OR alternative

```(venv) sh install.sh```

### Tests
Simple to run

```docker-compose exec app sh test.sh```

* OR alternative
```(venv) sh test.sh```

### Possible improvements

- make exception handling better 
- implement cache layer 
