result = [('nn.dump', '{"msisdn": "55555", "call_result": "онлайн"}'), ('nv.bridge', '{"kwargs": {"msisdn": "555555", "channel": null}}'), ('nv.synthesize', '{"args": ["И следующий текст вы должны слышать уже на фоне музыки", false]}'), ('nv.background', '{"args": ["Office_local"]}'), ('nv.synthesize', '{"args": ["Сейчас начнется проигрываться шум офиса на фоне", false]}'), ('nv.listen', '{"utterance": "перебивание", "context": null, "entities": {}, "intents": {}}'), ('nv.synthesize', '{"args": ["Перебивание. Эта часть текста не должна попасть в результаты распознавания", false]}'), ('nv.listen', '{"detect_policy": [null, null, 5], "entities": null, "entities_exclude": null, "intents": null, "intents_exclude": null, "context": null, "use_neuro_api": false, "params": {"no_input_timeout": 5000, "recognition_timeout": 30000, "speech_complete_timeout": 5000, "asr_complete_timeout": 5000}}'), ('nv.listen', '{"utterance": "распознавание пока произносится этот синтезированный тис как можно говорить и смотреть результаты распознавания", "context": null, "entities": {}, "intents": {}}'), ('nv.play_random_sound', '{"path": "9f714079-c69f-4fea-82c0-f41294be23fd.wav", "text": "ага", "name": "office"}'), ('nv.synthesize', '{"args": ["Распознование. Пока произносится этот синтезированный тескт нужно говорить и смотреть результаты распознования", false]}'), ('nv.listen', '{"detect_policy": [null, null, 300], "entities": null, "entities_exclude": null, "intents": null, "intents_exclude": null, "context": null, "use_neuro_api": false, "params": {"no_input_timeout": 5000, "recognition_timeout": 30000, "speech_complete_timeout": 5000, "asr_complete_timeout": 5000}}'), ('nv.synthesize', '{"args": ["Простой синтез для тестов", false]}'), ('nv.say', '{"args": ["hello", null]}'), ('nn.call', '{"args": ["55555"], "kwargs": {"channel_name": null, "script_id": null, "date_added": "2020-12-02 13:26:25", "transport": "sip", "use_default_prefix": false, "date_end": null, "params": {"entry_point": "main_online", "on_success_call": "after_call", "on_failed_call": "after_call", "proto_additional": {"P-Asserted-Identity": "<tel:neuro.net>"}}}}'), ('nn.dump', '{"msisdn": "55555"}')]
# ____ nv say
# for res in result:
#     if 'nv.say' in res:
#         assert any('hello' in d for d in res)
# if not any('nv.say' in d for d in result):
#     assert False
# ____ nv background
# for res in result:
#     if 'nv.background' in res:
#         assert any('Office_local' in d for d in res)
# if not any('nv.background' in d for d in result):
#     assert False
# ____ nv play random sound
# for res in result:
#     if 'nv.random_sound' in res:
#         assert any('ага' or 'min_delay' in d for d in res)
# if not any('nv.random_sound' in d for d in result):
#     assert False
# nv synth
# count = 0
# for res in result:
#     if 'nv.synthesize' in res:
#         count +=1
#         assert len(res[1]) > 20
# assert count == 5
# if not any('nv.synthesize' in d for d in result):
#     assert False
# nv listen / перебивание
# for res in result:
#     if 'nv.listen' in res:
#         for r in res:
#             if "распознавание" in r:
#                 assert "распознавание" or "пока" in r
#             elif "перебивание" in r.lower:
#                 assert "перебивание" in r
# if not any('nv.listen' in d for d in result):
#     assert False
# ____ nv bridge
# for res in result:
#     if 'nv.bridge' in res:
#         assert '555555' in res[1]
# if not any('nv.bridge' in d for d in result):
#     assert False
#
#
# # #
# for res in result:
#     if 'nv.listen' in res:
#         for r in res:
#             if "utterance" in r:
#                 assert "перебивание" in r
# if not any('nv.listen' in d for d in result):
#     assert False
import  os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
print(ROOT_DIR)