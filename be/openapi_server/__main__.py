#!/usr/bin/env python3

import connexion

from openapi_server import encoder
from openapi_server import config
from flask_cors import CORS
from flask import send_from_directory, request, jsonify


def main():
    app = connexion.App(__name__, specification_dir='./openapi/')

    # disable CORS for all endpoints
    # specify allowed origins for more secure configuration
    CORS(
        app.app,
        methods=[
            "GET",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
            "OPTIONS"],
        send_wildcard=True)

    host = '0.0.0.0'
    port = 8080

    # this endpoint serve the uploaded video files
    @app.route('/videos/<path:subpath>/<filename>')
    def serve_video(subpath, filename):
        directory = '/tmp/mais/video/' + subpath
        return send_from_directory(directory, filename)

    # this endpoint respond to all preflight OPTIONS requests with a 200 success for the sake of CORS
    # (e.g. to allow DELETE requests from the UI when you don't use a reverse proxy)
    @app.app.before_request
    def before_request():
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'}
        if request.method.lower() == 'options':
            return jsonify(headers), 200

    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'AI Music Subtitles - OpenAPI 3.0'},
                pythonic_params=True)
    app.app.config.update(config.get_config())
    app.run(port=port, host=host)


if __name__ == '__main__':
    main()
