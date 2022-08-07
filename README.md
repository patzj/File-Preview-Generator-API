# File Preview Generator API

A containerized service for generating file previews of supported files. This uses the [preview-generator](https://github.com/algoo/preview-generator) python library to generate the file previews and [Celery](https://docs.celeryq.dev/en/stable/) to spawn worker(s) to do the processing. This isolates the _"task"_ of generating the file previews from the web server receiving the requests.

## Basic Usage

This requires a running `Docker` [Engine](https://docs.docker.com/engine/) _(or [Daemon](https://docs.docker.com/engine/reference/commandline/dockerd/))_ and [Compose](https://docs.docker.com/compose/) tool.

```sh
$ docker-compose up -d
```

## Requesting for Preview

This will return a `task_id` that can be used to check the status of the process and download the result of the process.

```sh
curl -F "file=@/path/to/image.jpg" localhost:5000/generate
```

## Checking the Status

A `SUCCESS` status indicates that the preview is ready to be downloaded. Please see Celery [Built-in States](https://docs.celeryq.dev/en/stable/userguide/tasks.html#built-in-states) for more info.

```sh
curl localhost:5000/status/<task_id>
```

## Downloading the Preview

As stated from the [Checking the Status](#checking-the-status) section, the file is ready to be downloaded once the status is `SUCCESS`.

```sh
curl -o preview.jpg localhost:5000/download/<task_id>
```
