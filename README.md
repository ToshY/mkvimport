<h1 align="center"> 📺 MKVimport </h1>

<div align="center">
    <img src="https://img.shields.io/github/v/release/toshy/mkvimport?label=Release&sort=semver" alt="Current bundle version" />
    <img src="https://img.shields.io/github/actions/workflow/status/toshy/mkvimport/codestyle.yml?branch=main&label=Black" alt="Black">
    <img src="https://img.shields.io/github/actions/workflow/status/toshy/mkvimport/codequality.yml?branch=main&label=Ruff" alt="Ruff">
    <img src="https://img.shields.io/github/actions/workflow/status/toshy/mkvimport/statictyping.yml?branch=main&label=Mypy" alt="Mypy">
    <img src="https://img.shields.io/github/actions/workflow/status/toshy/mkvimport/security.yml?branch=main&label=Security%20check" alt="Security check" />
</div>

## 📝 Quickstart

A command-line utility for embedding attachments (subtitles, fonts and chapters) to MKV files.

## 🧰 Requirements

* 🐋 [Docker](https://docs.docker.com/get-docker/)

## 🎬 Usage

MKVimport requires 2 volumes to be mounted: `/app/input` and `/app/output`.

### 🐋 Docker

```shell
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
      - ./input:/input
      - ./output:/output
```

Then run it.

```shell
docker compose run -u $(id -u):$(id -g) --rm mkvimport -h
```

## 🛠️ Contribute

### Requirements

* ☑️ [Pre-commit](https://pre-commit.com/#installation).
* 🐋 [Docker Compose V2](https://docs.docker.com/compose/install/)
* 📋 [Task 3.37+](https://taskfile.dev/installation/)

### Pre-commit

Setting up `pre-commit` code style & quality checks for local development.

```shell
pre-commit install
```

## ❕ License

This repository comes with a [MIT license](./LICENSE).
