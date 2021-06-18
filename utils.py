from zipfile import ZipFile

import requests


def download_file(url):
    """
        download file from url, return file name from url
    """
    r = requests.get(url, allow_redirects=True)
    filename = get_filename_from_url(url)
    open(filename, 'wb').write(r.content)
    return filename


def get_filename_from_url(url):
    """
        return file name from url, last split after "/"
    """
    if not url:
        return None
    url_split = url.split("/")
    return url_split[len(url_split) - 1]


def unzip(filename, path=None):
    """
        unzip the file in the current repository
    """
    zp = ZipFile(filename)
    zp.extractall(path)
    zp.close()
