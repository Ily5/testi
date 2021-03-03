import time
from media_helper import MediaHelper

# token = ""
result = []
times = []

mh = MediaHelper()


def rtest():
    token = mh.auth()
    resp = mh.get_calls(token)
    print(resp)
    while resp < 200:
        try:
            mh.init_dialog_with_recog(token)
            resp = mh.get_calls(token)
            print(resp)
            time.sleep(3)
        except TimeoutError:
            mh.init_dialog_with_recog(token)
            print("timer", times)
            print("channel limit", result)
    print(times)
    print(result)


if __name__ == '__main__':
    rtest()
