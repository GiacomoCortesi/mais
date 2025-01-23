## Setup


### Backend

Backend service expose REST API for CRUD operations on:
 - transcription
 - job
 - file

File storage is supported either locally or on AWS.

Note that if using local storage, realtime video and subtitles rendering won't be available.

When using AWS storage, the following env variables must be set:
```
export AWS_ACCESS_KEY_ID=<your-aws-key-id>
export AWS_SECRET_ACCESS_KEY=<your-aws-secret>
```
In order to authenticate and authorize requests to AWS.

Video and subtitles rendering use Remotion, follow [this guide](https://www.remotion.dev/docs/lambda/setup) for the initial setup.

To enable remotion, the following env variables must be set:
```
export REMOTION_APP_FUNCTION_NAME=<your-remotion-app-function-name>
export REMOTION_APP_SERVE_URL=<your-remotion-app-serve-url>
```

Where REMOTION_APP_SERVE_URL is the deployed remotion site.
REMOTION_APP_SERVE_URL can be retrieved by running:
```
npx remotion lambda sites ls
```

And REMOTION_APP_FUNCTION_NAME is the deployed remotion lambda function.
REMOTION_APP_FUNCTION_NAME can be retrieved by running:
```
npx remotion lambda functions ls
```

Note that you need to set aws credentials for npx remotion commands to work:
```
REMOTION_AWS_ACCESS_KEY_ID=<your-aws-key-id>
REMOTION_AWS_SECRET_ACCESS_KEY=<your-aws-secret>
```

In order to use the AI powered subtitles fix functionality, an openai token is required.
```
export OPENAI_API_TOKEN=<your-openai-api-token>
```

### Run With Docker
Build the api docker image

`docker build -t mais-api .`

Run the docker image

`docker run -p 80:80 --rm mais-api`
