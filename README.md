# translate-batches

Bulk translate text files using Google Cloud Translate and Amazon Translate

[![Support with PayPal](https://img.shields.io/badge/paypal-donate-yellow.png)](https://paypal.me/zacanger) [![Patreon](https://img.shields.io/badge/patreon-donate-yellow.svg)](https://www.patreon.com/zacanger) [![ko-fi](https://img.shields.io/badge/donate-KoFi-yellow.svg)](https://ko-fi.com/U7U2110VB)

----

This script translates a directory of files using either Amazon or Google. It
was originally written to automate translations from Chinese and Sinhala to
English to use as a base for a translation of a Buddhist text.

There are some variables in the script that need to be changed before running.
See the comments in the script. You will need AWS CLI and/or Google CLI (or a
service account) set up. See Google and Amazon's docs on how to do that.

Once configured, Call it with `./translate.py path/to/directory` where the
directory has a bunch of markdown files in the language you want to translate.
This will produce new files in that directory that can then be moved, renamed,
and eventually cleaned up and organized into readable text.

[LICENSE](./LICENSE.md)
