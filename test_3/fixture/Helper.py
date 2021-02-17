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

    def __init__(self, path_to_file):
        self.path_to_file = path_to_file

    def create_file_of_response(self, file_name, api_response):
        full_path_to_file = self.path_to_file + file_name
        with open(fr'{full_path_to_file}', 'wb') as file:
            api_response: requests.Response
            file.write(api_response.content)
            # file.close()

        return file_name

    def get_file_properties(self, file_name):
        full_path_to_file = self.path_to_file + file_name
        size = os.path.getsize(full_path_to_file)

        with contextlib.closing(wave.open(full_path_to_file, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)

        os.remove(full_path_to_file)
        return {'size': size, 'duration': duration}



