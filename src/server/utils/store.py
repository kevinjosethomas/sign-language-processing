class Store:
    raw_word = ""
    raw_letters = []
    raw_transcription = []
    corrected_transcription = []
    transcription = []
    parsed = ""

    @classmethod
    def parse(cls, new_transcription: str):
        cls.parsed = new_transcription

    @classmethod
    def reset(cls):
        cls.raw_word = ""  # current word being parsed
        cls.raw_letters = []  # every letter in every frame
        cls.raw_transcription = []  # raw transcription, every word is an element
        cls.corrected_transcription = (
            []
        )  # corrected transcription, every word is an element
        cls.parsed = ""  # final parsed transcription
