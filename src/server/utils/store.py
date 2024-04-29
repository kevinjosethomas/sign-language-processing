class Store:
    raw_word = ""
    raw_letters = []
    raw_transcription = []
    transcription = []
    parsed = ""

    @classmethod
    def parse(cls, new_transcription: str):
        cls.parsed = new_transcription

    @classmethod
    def reset(cls):
        cls.raw_word = ""
        cls.raw_letters = []
        cls.raw_transcription = []
        cls.transcription = []
        cls.parsed = ""
