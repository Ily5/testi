import time
from media_helper import MediaHelper

import sys, getopt

# token = ""
result = []
times = []

mh = MediaHelper()


#
# def rtest():
#     token = mh.auth()
#     resp = mh.get_calls(token)
#     print(resp)
#     while resp < 200:
#         try:
#             mh.init_dialog_with_recog(token)
#             resp = mh.get_calls(token)
#             print("call count - " + str(resp))
#             time.sleep(3)
#         except TimeoutError:
#             mh.init_dialog_with_recog(token)
#             print("timer", times)
#             print("channel limit", result)
#     print(times)
#     print(result)

def test_media_server():
    channel_limit = int(sys.argv[1])
    delay = float(sys.argv[2])
    token = mh.auth()
    resp = mh.get_calls(token)
    print(resp)
    print(channel_limit)
    while resp < channel_limit:
        try:
            mh.init_dialog_with_recog(token, delay)
            resp = mh.get_calls(token)
            print("call count - " + str(resp))
            mh.get_la()
            # print(mh.get_la)
            time.sleep(3)
        except TimeoutError:
            mh.init_dialog_with_recog(token, delay)


def debug():
    print(sys.argv[1])


if __name__ == '__main__':
    # test_media_server()
    test_media_server()
