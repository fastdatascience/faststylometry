'''
MIT License

Copyright (c) 2023 Fast Data Science Ltd (https://fastdatascience.com)

Maintainer: Thomas Wood

Tutorial at https://fastdatascience.com/fast-stylometry-python-library/

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import os
import zipfile

import wget


def bar_custom(current, total, width=80):
    """
    Display a progress bar to track the download.
    :param current: Current bytes downloaded
    :param total: Total bytes.
    :param width: Width of the bar in chars.
    """
    print("Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total), end="\r")


def download_examples():
    """
    Download the example corpus
    """

    data_path = "data"
    is_folder_exists = os.path.exists(data_path)
    if not is_folder_exists:
        print(f"Creating folder {data_path} in current working directory.")
        # Create a new directory because it does not exist
        os.makedirs(data_path)

    if os.path.exists("data/train") and len(os.listdir("data/train")) > 0:
        print("data/train is not empty. Exiting the downloader.")  #
        return
    if os.path.exists("data/test") and len(os.listdir("data/test")) > 0:
        print("data/test is not empty. Exiting the downloader.")  #
        return

    url = 'https://raw.githubusercontent.com/fastdatascience/faststylometry/main/data/train_test.zip'

    local_file = "data/train_test.zip"
    print(f"Downloading {url} to {local_file} in current working directory...")

    wget.download(url, out=local_file, bar=bar_custom)

    print(f"Downloaded {url} to {local_file}.\nExtracting to {data_path}...")

    with zipfile.ZipFile(local_file, 'r') as zip_ref:
        zip_ref.extractall(data_path)

    print(f"Extracted contents of zip file to {data_path}.")
