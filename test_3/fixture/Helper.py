import os
import requests
import wave
import contextlib


class FileHelper(object):
    """
    1. Получение uuid звонка
        а. Коннект к базе
        б. Получаем uuid нужного звонка (тот который длиннее)
    2. Скачивание и запись звонка в файл
        - создание метода получения и записи файла
    3. Получение свойств файла
    4. Сравнение с эталонным файлом
    """

    def __init__(self, path_to_file, api_helper):
        self.api_helper = api_helper
        self.path_to_file = path_to_file

    def create_file_of_response(self, file_name, api_response):
        full_path_to_file = self.path_to_file + file_name
        with open(r'{path}'.format(path=full_path_to_file), 'wb') as file:
            file.write(api_response.content)

        return file_name

    def get_file_properties(self, file_name):
        full_path_to_file = self.path_to_file + file_name
        size = os.path.getsize(full_path_to_file)

        with contextlib.closing(wave.open(full_path_to_file, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)

        # os.remove(full_path_to_file)
        return {'size': size, 'duration': duration}

    def get_call_file_properties(self, create_file_name, call_uuid):
        path = self.api_helper.path_end_point['download_call_audio'] + str(call_uuid)
        response = self.api_helper.request_send(path=path)
        self.create_file_of_response(file_name=create_file_name, api_response=response)
        return self.get_file_properties(file_name=create_file_name)
