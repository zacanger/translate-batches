#!/usr/bin/env python3

import os
import sys

# google or amazon
SERVICE_TO_USE = "amazon"
# zh-TW == traditional chinese, see the docs for language codes
LANGUAGE_FROM = "zh-TW"
# en-US, en, etc., see the docs for language codes
LANGUAGE_TO = "en"

# fill in from google cloud console
GOOGLE_PROJECT_ID = "translation-301721"
GOOGLE_PROJECT_LOCATION = "global"

# fill in from your aws account
AMAZON_REGION = "us-east-1"

dir_to_translate = sys.argv[1]
files_to_translate = os.listdir(dir_to_translate)


def amazon_translate_text(text):
    import boto3
    from botocore.config import Config

    # this gets rate limited almost immediately,
    # so add in a bunch of retry attempts
    config = Config(retries=dict(max_attempts=20))

    translate = boto3.client(
        service_name="translate",
        region_name=AMAZON_REGION,
        use_ssl=True,
        config=config,
    )

    result = translate.translate_text(
        Text=text,
        SourceLanguageCode=LANGUAGE_FROM,
        TargetLanguageCode=LANGUAGE_TO,
    )

    return result.get("TranslatedText")


def google_translate_text(text):
    from google.cloud import translate

    client = translate.TranslationServiceClient()
    parent = (
        f"projects/{GOOGLE_PROJECT_ID}/locations/{GOOGLE_PROJECT_LOCATION}"
    )
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": LANGUAGE_FROM,
            "target_language_code": LANGUAGE_TO,
        }
    )

    tr = []
    for translation in response.translations:
        tr.append(translation.translated_text)
    return "".join(tr)


# chunk files to avoid hitting limites. google says "5000 code points", amazon
# says "5000 bytes". 1500 characters seems to be low enough to not freak amazon
# out.
def chunk_file(text):
    n = 1500
    chunks = [text[i : i + n] for i in range(0, len(text), n)]
    print(len(chunks), "chunks to process")
    return chunks


def write_translated_file(text, path):
    with open(path + SERVICE_TO_USE + ".md", "w") as dst:
        dst.write(text)
        dst.close()
        return


def translate_file(file_name):
    full_path = dir_to_translate + "/" + file_name
    with open(full_path) as source_file:
        source = source_file.read()
        splits = chunk_file(source)
        tr = []
        for s in splits:
            if SERVICE_TO_USE == "google":
                tr.append(google_translate_text(s))
            elif SERVICE_TO_USE == "amazon":
                tr.append(amazon_translate_text(s))
            else:
                raise ValueError("No valid service selected!")
        return write_translated_file("".join(tr), full_path)


def main():
    for file in files_to_translate:
        print("translating " + file)
        translate_file(file)


if __name__ == "__main__":
    main()
