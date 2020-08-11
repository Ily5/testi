class RecordEntity:

    def __init__(self, name=None, value=None, desc=None):
        self.name = name
        self.value = value
        self.desc = desc


class RecordEntityFile:

    def __init__(self, f=None, f_txt=None, f_flag=None, f_lang=None):
        self.f = f
        self.f_txt = f_txt
        self.f_flag = f_flag
        self.f_lang = f_lang