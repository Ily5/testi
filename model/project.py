class Project:

    def __init__(self, name, description, not_before, not_after, delay, count, channel,
                 flag, api_url, start_unit, record_path,caller_id, before_call_unit,
                 after_call_unit, routing_channel_limit, total_channel_limit, tts):
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


