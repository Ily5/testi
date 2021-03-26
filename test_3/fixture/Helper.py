import os
import datetime
import gc
import wave
import contextlib
import librosa
import paramiko
from pandas import DataFrame


class FileHelper(object):
    def __init__(self, path_to_file, api_helper):
        self.api_helper = api_helper
        self.path_to_file = path_to_file

    def create_file_of_response(self, file_name, api_response) -> str:
        full_path_to_file = self.path_to_file + file_name
        with open(r"{path}".format(path=full_path_to_file), "wb") as file:
            file.write(api_response.content)

        return file_name

    def get_file_properties(self, file_name: str) -> dict:
        full_path_to_file = self.path_to_file + file_name
        size = os.path.getsize(full_path_to_file)

        with contextlib.closing(wave.open(full_path_to_file, "r")) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
        rms_sum, cent_sum = self.comparison_audio_files(full_path_to_file)

        os.remove(full_path_to_file)
        return {
            "size": size,
            "duration": duration,
            "rms_sum": rms_sum,
            "cent_sum": cent_sum,
        }

    def get_call_file_properties(self, create_file_name, call_uuid) -> dict:
        path = self.api_helper.path_end_point["download_call_audio"] + str(call_uuid)
        response = self.api_helper.request_send(path=path)
        self.create_file_of_response(file_name=create_file_name, api_response=response)
        return self.get_file_properties(file_name=create_file_name)

    @staticmethod
    def comparison_audio_files(file_name):
        y, sr = librosa.load(file_name, sr=8000)
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


class SshHelper:
    def __init__(self, username, hosts):
        self.username = username
        self.hosts = hosts

    def client(self, host):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(hostname=host, username=self.username)
        client.exec_command("sudo su")
        return client

    def get_count_lines_in_log(self, host, log_name, grep_text):
        log_name = self.log_name(log_name)
        command = f"cat /var/log/ivr/{log_name} |  grep {grep_text} | wc -l"
        client = self.client(host)
        result = client.exec_command(command)
        res_end = result[1].read() + result[2].read()
        client.close()
        return int(str(res_end, encoding="utf-8"))

    def get_last_n_line_log(self, host: str, log_name: str, n: int, add_command=""):
        log_name = self.log_name(log_name)
        if add_command != "":
            add_command = " | " + add_command

        client = self.client(host)
        command = f"tail -n {str(n)} /var/log/ivr/{log_name}{add_command}"
        result = client.exec_command(command)
        res_end = result[1].read() + result[2].read()
        client.close()
        return str(res_end, encoding="utf-8")

    @staticmethod
    def log_name(log_name):
        if "online" in log_name:
            log_name = "logic-executor-online.log"
        elif "offline" in log_name:
            log_name = "logic-executor-offline.log"
        elif "media" in log_name:
            log_name = "media-server.log"
        return log_name


class CreateReportAsr:

    @staticmethod
    def create_asr_result_to_csv(result_all: list, file_name: str):
        result_final_good = []
        detect_good = []
        file_good = []
        result_final_bad = []
        detect_bad = []
        file_bad = []

        for result in result_all:
            if 'None' in result[1]:
                file_bad.append(result[0])
                detect_bad.append('')
            else:
                file_good.append(result[0])
                detect_good.append(result[1])

        result_final_good.append(file_good)
        result_final_good.append(detect_good)

        result_final_bad.append(file_bad)
        result_final_bad.append(detect_bad)
        print(f"\n {datetime.datetime.now()} - Start create with detect report")
        df = DataFrame(result_final_good).transpose()
        df.columns = ['filename', 'detected']
        df.to_csv(f"{datetime.datetime.now().date()}_{file_name}_with_detect", sep='\t', header=True, index=False)
        print(f"\n {datetime.datetime.now()} - Finish create with detect report")
        print(df.memory_usage())
        del df

        print(f"\n {datetime.datetime.now()} - Start create without detect report")
        df = DataFrame(result_final_bad).transpose()
        df.columns = ['filename', 'detected']
        df.to_csv(f"{datetime.datetime.now().date()}_{file_name}_without_detect", sep='\t', header=True, index=False)
        print(f"\n {datetime.datetime.now()} - Finish create without detect report")
        print(df.memory_usage())
        print("DIR     ", os.path.abspath(os.curdir))
        print("SCRIPT     ", os.path.abspath(__file__))
        del df
        gc.collect()
