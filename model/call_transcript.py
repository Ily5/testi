class CallTranscript:
    bad_call = "але ну да что вы хотите да да да что вы хотите але не знаю у меня еще один есть " \
               "я звоню другим не знаю даже как вот ну с меня потом выдирать"

    neutral_call = "ало да давайте попробуем понятия не имею если честно давайте на пятёрке " \
                   "остановимся будет везде средний результат ставить а я говорю давайте пять поставим " \
                   "потому что я не вижу смысла повторять этот вопрос"

    good_call = "да здравствуйте мария ну давайте пару минут можно нет ну в настоящий момент десять " \
                "ну как бы больше никаких у меня трений не было все хорошо я что-то не" \
                " поняла просто мне все понравилось наоборот все хорошо "


class Numbers:
    def __init__(self, number=None, transcript=None):
        self.number = number
        self.transcript = transcript

    def __repr__(self):
        return "%s:%s" % (self.number, self.transcript)


class Voice:
    def __init__(self, asr=None, tts=None):
        self.asr = asr
        self.tts = tts

    def __repr__(self):
        return "%s:%s" % (self.asr, self.tts)

