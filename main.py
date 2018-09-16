import os
import connexion

from injector import Binder
from flask_injector import FlaskInjector
from connexion.resolver import RestyResolver


def configure(binder: Binder) -> Binder:

    return binder
app = connexion.App(__name__, specification_dir='swagger/')
app.add_api('api_doc.yaml', resolver=RestyResolver('api'))
FlaskInjector(app=app.app, modules=[configure])

if __name__ == '__main__':
    app.run(port=9090, debug=True)
