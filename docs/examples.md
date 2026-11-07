# Examples

The default behavior is to embed the attachments from a given subdirectory to an input file with the same name 

**Example**

Let's have a video file `never-gonna-give-you-up.mkv` with a subdirectory `never-gonnna-give-you-up` mounted to the `/app/input` directory.

```text
/app/input/
├── never-gonna-give-you-up.mkv
└── never-gonna-give-you-up/
    ├── attachments/
    │   ├── Arial.ttf
    │   ├── ...
    │   └── COMIC.ttf
    ├── chapters.xml
    ├── tags.xml
    ├── track4_eng.ass
    ├── ...
    └── track8_jpn.ass
```

This will result in an output file `never-gonna-give-you-up (1).mkv` saved to the `/app/output` directory.

```text
/app/output/
├── never-gonna-give-you-up (1).mkv
```

!!! tip
    
    Use the [mkvexport](https://github.com/ToshY/mkvexport) tool to extract attachments with the above-mentioned tree structure.

## Modes

| Mode | Behaviour |
|---|---|
| `replace` (default) | Removes all existing subtitles, attachments, chapters and track tags from the input file, then adds the ones from the subdirectory. |
| `add` | Keeps everything in the input file and adds the subtitles, attachments and chapters from the subdirectory. |

## Tags

!!! note

    The `tags.xml` file is **not** imported.

    - Track statistics tags (`BPS`, `DURATION`, `NUMBER_OF_FRAMES`, `NUMBER_OF_BYTES`, `_STATISTICS_*`) are recalculated 
      by mkvmerge on every remux, so the output always contains correct values.
    - Global tags of the input file (e.g. `TITLE`, `COMMENT`) are kept in both modes. They are copied as-is, so edits 
      made in `tags.xml` are not applied.

## Basic

Add your files, video and attachments, to the input directory of the mounted container.

```sh
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  ghcr.io/toshy/mkvimport:latest
```

By default, it will find all files from the `/app/input` directory (recursively) and write the output to the `/app/output` directory.

## Specific subdirectory

Embed attachments for files in a single subdirectory and writing output to `/app/output/hits`.

```sh
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  ghcr.io/toshy/mkvimport:latest \
  -i "input/hits" \
  -o "output/hits"
```

## Multiple inputs

Embed attachments for files in multiple input subdirectories and writing output to `/app/output` (default).

```sh
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  ghcr.io/toshy/mkvimport:latest \
  -i "input/dir1" \
  -i "input/dir2" \
  -i "input/dir3" \
  -i "input/dir4" \
  -i "input/dir5"
```

## Multiple inputs and outputs

Embed attachments for files in multiple input subdirectories and writing output to specific output subdirectories respectively.

```sh
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  ghcr.io/toshy/mkvimport:latest \
  -i "input/dir1" \
  -i "input/dir2" \
  -i "input/dir3" \
  -i "input/dir4" \
  -i "input/dir5" \
  -o "output/dir1" \
  -o "output/dir2" \
  -o "output/dir3" \
  -o "output/dir4" \
  -o "output/dir5"
```

## Multiple inputs, outputs and mode

Embed attachments for files in multiple input subdirectories, with the `add` mode, and writing output to specific output subdirectories respectively.

```sh
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  ghcr.io/toshy/mkvimport:latest \
  -i "input/dir1" \
  -i "input/dir2" \
  -i "input/dir3" \
  -i "input/dir4" \
  -i "input/dir5" \
  -m "add" \
  -o "output/dir1" \
  -o "output/dir2" \
  -o "output/dir3" \
  -o "output/dir4" \
  -o "output/dir5"
```

## Multiple inputs, outputs and presets

Embed attachments for files in multiple input subdirectories, with `add`/`replace` modes, and writing output to specific output subdirectories respectively.

```sh
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  -v ${PWD}/preset/video-custom.json:/app/preset/video-custom.json \
  -v ${PWD}/preset/audio-custom.json:/app/preset/audio-custom.json \
  ghcr.io/toshy/mkvimport:latest \
  -i "input/dir1" \
  -i "input/dir2" \
  -i "input/dir3" \
  -i "input/dir4" \
  -i "input/dir5" \
  -m "add" \
  -m "replace" \
  -m "replace" \
  -m "add" \
  -m "add" \
  -o "output/dir1" \
  -o "output/dir2" \
  -o "output/dir3" \
  -o "output/dir4" \
  -o "output/dir5"
```
