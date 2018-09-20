import os
import connexion
import requests
from injector import Binder, singleton
from flask_injector import FlaskInjector
from connexion.resolver import RestyResolver
from services.json_encoder import ApiJSONEncoder
from services.query_bus import QueryBus, IQueryBus
from services.tweets_handler import TweetsHandler
from services.twitter_client import TwitterClient, ITwitterClient, TwitterClientHeaderDecorator
from services.user_handler import UserTweetsHandler


def configure(binder: Binder) -> Binder:
    binder.bind(TwitterClient, to=TwitterClient(requests), scope=singleton)
    binder.bind(ITwitterClient, to=TwitterClientHeaderDecorator(binder.injector.get(TwitterClient)), scope=singleton)
    binder.bind(
        IQueryBus,
        to=QueryBus([
            binder.injector.get(TweetsHandler),
            binder.injector.get(UserTweetsHandler)
        ]),
        scope=singleton
    )
    return binder


app = connexion.App(__name__, specification_dir='swagger/')
app.add_api('api_doc.yaml', resolver=RestyResolver('api'))
app.app.json_encoder = ApiJSONEncoder
FlaskInjector(app=app.app, modules=[configure])

if __name__ == '__main__':
    app.run(port=os.environ.get('APP_PORT', 80), debug=bool(os.environ.get('FLASK_DEBUG', False)))
