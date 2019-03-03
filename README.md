# Mangarock

Script to download, decrypt and parse comics from mangarock. Enjoy!

## Install

pip install -e git+https://github.com/italomaia/mangarock.py#egg=master

## Usage

```fish
> mangarock mrs-serie-74620  # download full comic
> mangarock mrs-serie-74620 -c mrs-chapter-74622  # download one chapter
```

## Note

**Images** are downloaded in [webp format](https://developers.google.com/speed/webp/),
which is new in might not open with all image viewers. As a last resort, you can
use your web browser to open it.

**MRI parser** is based in [this implementation](https://github.com/MinusGix/MangarockDownloader/blob/master/smallMangaRock.js).

**Series folder** are not compatible with the comic file types (cbz, cbr, etc) **yet**
because webp is simply not supported. 