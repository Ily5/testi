import time
from media_helper import MediaHelper
import logging
import sys, getopt
from test_3.fixture.api import APIClientV3


# token = ""
result = []
times = []

mh = MediaHelper()
# logging.getLogger('').handlers = []
logging.basicConfig(filename=None, level=logging.INFO,
                    format='%(asctime)s  - %(levelname)s - %(message)s')


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
    mh.set_voice('stc_test_asr')
    channel_limit = int(sys.argv[1])
    delay = float(sys.argv[2])
    token = mh.auth()
    resp = mh.get_calls(token)
    logging.info("started with - " + str(resp))
    logging.info("set calls limit - " + str(channel_limit))
    while resp < channel_limit:
        try:
            mh.init_dialog_with_recog(token, delay)
            resp = mh.get_calls(token)
            # print("call count - " + str(resp))
            logging.info("call count - " + str(resp))
            mh.get_la()
            # print(mh.get_la)
            time.sleep(0.5)
        except TimeoutError:
            mh.init_dialog_with_recog(token, delay)

# set total channel limit


def test_media_server_alternative():
    # set total channel limit = 100 , default 1000
    channel_limit = int(sys.argv[1])
    delay = float(sys.argv[2])
    # mh.set_voice(sys.argv[3])
    token = mh.auth()
    resp = mh.get_calls(token)
    if resp < 200:
        mh.push_dialogs(token, 500)
    ac = mh.get_active_calls(token)
    logging.info("started with - " + str(ac))
    logging.info("set calls limit - " + str(channel_limit))
    # while resp < channel_limit:
    while True:
        try:
            # mh.init_dialog_with_recog(token, delay)
            ac = mh.get_active_calls(token)
            resp = mh.get_calls(token)
            # print("call count - " + str(resp))
            logging.info("active call count - " + str(ac))
            logging.info("call count - " + str(resp))
            mh.get_la()

            # print(mh.get_la)
            time.sleep(3)
        except TimeoutError:
            mh.init_dialog_with_recog(token, delay)


def debug():
    token = mh.auth()
    s = mh.get_calls(token)
    mh.get_active_calls(token)


if __name__ == '__main__':
    # test_media_server()
    test_media_server_alternative()
    # debug()