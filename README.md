# Mangarock

Script to download, decrypt and parse comics from mangarock. Enjoy!

## Install

pip install -e git+https://github.com/italomaia/mangarock.py#egg=master

## Usage

```bash
> mangarock mrs-serie-74620  # download full comic
> mangarock mrs-serie-74620 -c 0  # download first chapter
```

## Dockerfile usage

Given you have docker installed:

```
> cd /path/to/mangarock-project-folder
> docker build . -t mangarock
> docker run --rm -v /path/where/comic/should/be/put:/home/nonroot mangarock mrs-serie-74620  # or
> docker run --rm -v /path/where/comic/should/be/put:/home/nonroot mangarock mrs-serie-74620 -c 0
```

## Note

**Images** are downloaded in [webp format](https://developers.google.com/speed/webp/),
which is new in might not open with all image viewers. As a last resort, you can
use your web browser to open it.

**MRI parser** is based in [this implementation](https://github.com/MinusGix/MangarockDownloader/blob/master/smallMangaRock.js).

**Series folder** are not compatible with the comic file types (cbz, cbr, etc) **yet**
because webp is simply not supported.