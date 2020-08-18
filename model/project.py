class Project:

    def __init__(self, name=None, description=None, not_before=None, not_after=None, delay=None, count=None, channel=None,
                 flag=None, api_url=None, start_unit=None, record_path=None,caller_id=None, before_call_unit=None,
                 after_call_unit=None, routing_channel_limit=None, total_channel_limit=None, tts=None, asr=None):
        self.name = name
        self.description = description
        self.not_before = not_before
        self.not_after = not_after
        self.delay = delay
        self.count = count
        self.channel = channel
        self.flag = flag
        self.api_url = api_url
        self.start_unit = start_unit
        self.record_path = record_path
        self.caller_id = caller_id
        self.before_call_unit = before_call_unit
        self.after_call_unit = after_call_unit
        self.routing_channel_limit = routing_channel_limit
        self.total_channel_limit = total_channel_limit
        self.tts = tts
        self.asr = asr


