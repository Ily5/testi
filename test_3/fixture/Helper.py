import os

import numpy as np
import wave
import contextlib

import librosa


# import librosa.display


class FileHelper(object):

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
        rms_sum, cent_sum = self.comparison_audio_files(full_path_to_file)

        os.remove(full_path_to_file)
        return {'size': size, 'duration': duration, 'rms_sum': rms_sum, 'cent_sum': cent_sum}

    def get_call_file_properties(self, create_file_name, call_uuid):
        path = self.api_helper.path_end_point['download_call_audio'] + str(call_uuid)
        response = self.api_helper.request_send(path=path)
        self.create_file_of_response(file_name=create_file_name, api_response=response)
        return self.get_file_properties(file_name=create_file_name)

    @staticmethod
    def comparison_audio_files(file_name):
        y, sr = librosa.load(file_name, sr=8000)
        s = np.abs(librosa.stft(y))
        rms = librosa.feature.rms(y=y)
        cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        cent_sum = 0
        for cen in cent:
            for x in cen:
                cent_sum += x

        rms_sum = 0
        for rm in rms:
            for x in rm:
                rms_sum += x

        return rms_sum, cent_sum

    @staticmethod
    def get_percent(first, second):
        return abs(first / second - 1) * 100
