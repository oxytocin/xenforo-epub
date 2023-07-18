## Intro

This repository contains a python script to scrape fanfiction threads on xenforo forums (e.g. Thousand Roads, Serebii) and output an ebook.

## Requirements

- Pandoc
- Python 3 with the packages "requests" and "beautiful soup 4"

## Limitations

Any posts made by the thread author are included in the ebook, even if they are not story chapters (e.g. review responses). I don't know of any way to exclude non-story posts.

## Usage

`scraper.py thread_url output_filename`

The output filename should end in .epub for an ebook.
