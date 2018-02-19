import os
import json
import logging
import requests
from time import sleep
from hashlib import md5

from django.conf import settings


logger = logging.getLogger(__name__)


def _save_by_url(path, url, ttl):
    if ttl < 0:
        logger.error("fail: {}".format(url))
        return

    file = open(path, 'wb')
    try:
        response = requests.get(url)
    except requests.ConnectionError:
        file.close()
        sleep(1)
        _save_by_url(path, url, ttl - 1)
        return

    if response.status_code == 200:
        file.write(response.content)
    file.close()


def _save_file(file_data: dict, path: str, file_name: str):
    file_path = os.path.join(path, file_name)

    if not os.path.isfile(file_path):
        _save_by_url(file_path, file_data['url'], settings.GET_FILE_TTL)
        return

    if md5(open(file_path, 'rb').read()).hexdigest() == file_data['md5']:
        return

    temp_path = os.path.join(path, 'temp_' + file_name)
    _save_by_url(temp_path, file_data['url'], settings.GET_FILE_TTL)
    os.remove(file_path)
    os.rename(temp_path, file_path)


def _data_to_files(data: dict):
    def handle_group_of_files(name, root, default_name):
        if name not in data:
            return

        for file in data[name]:
            _save_file(file, root, '{}.{}'.format(default_name, file['filetype']))
            sleep(1)

    handle_group_of_files('plugins', settings.PLUGINS_FILES_ROOT, settings.PLUGINS_DEFAULT_NAME)
    handle_group_of_files('theme_files', settings.THEMES_FILES_ROOT, settings.THEMES_DEFAULT_NAME)
    handle_group_of_files('content_editor_files', settings.EDITOR_FILES_ROOT, settings.EDITOR_DEFAULT_NAME)


def _get_additional_data(url):
    try:
        response = requests.get(url, {'token': settings.SETKA_LICENSE_KEY})
    except requests.ConnectionError:
        return None

    if response.status_code == 200:
        return json.loads(response.content)


def update_setka_build():
    content = _get_additional_data(settings.SETKA_CURRENT_BUILD_URL)
    if content:
        _data_to_files(content)


def update_setka_themes():
    content = _get_additional_data(settings.SETKA_CURRENT_THEME_URL)
    if content:
        _data_to_files(content)


def get_status_info():
    return _get_additional_data(settings.SETKA_COMPANY_STATUS_URL)
