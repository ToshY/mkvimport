## Requirements

- 🐋 [Docker](https://docs.docker.com/get-docker/)

## Pull image

```sh
docker pull ghcr.io/toshy/mkvimport:latest
```

## Run container

### 🐋 Docker

Run with `docker`.

```sh
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  ghcr.io/toshy/mkvimport:latest -h
```

### 🐳 Compose

Create a `compose.yaml` file.

```yaml
services:
  mkvimport:
    image: ghcr.io/toshy/mkvimport:latest
    volumes:
      - ./input:/app/input
      - ./output:/app/output
```

Run with `docker compose`.

```sh
docker compose run -u $(id -u):$(id -g) --rm mkvimport -h
```

## Volumes

The following volume mounts are **required**: 

- `/app/input`
- `/app/output`
