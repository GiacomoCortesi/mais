#!/usr/bin/env python3

import connexion

from openapi_server import config
from openapi_server.logging.config import setup_logging
from openapi_server import log
from starlette.middleware.cors import CORSMiddleware
from pathlib import Path
from connexion.middleware import MiddlewarePosition

def create_app():
    # create the connexion app
    app = connexion.App(__name__, specification_dir='./openapi/')
    # add CORS middleware to:
    # - allow all methods
    # - allow all headers
    # - allow all origins
    # It also respond to all preflight OPTIONS requests
    # (e.g. to allow DELETE requests from the UI when you don't use a reverse proxy)
    app.add_middleware(CORSMiddleware, position=MiddlewarePosition.BEFORE_ROUTING, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'], allow_credentials=True)

    app.add_api('openapi.yaml',
                arguments={'title': 'AI Music Subtitles - OpenAPI 3.0'},
                pythonic_params=True)
    app.app.config.update(config.get_config())
    return app


def main():
    setup_logging()

    host = '0.0.0.0'
    port = 8080

    app = create_app()
    log.info("MAIS application started")

    app.run(f"openapi_server.{Path(__file__).stem}:create_app", port=port, host=host, reload=True, factory=True)


if __name__ == '__main__':
    main()
