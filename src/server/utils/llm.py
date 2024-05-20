import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from utils.store import Store

load_dotenv()


class LLM:
    llm = ChatOpenAI(
        # model="gpt-3.5-turbo-0125",
        model="gpt-4o",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )

    RECEPTIVE_PROMPT = ChatPromptTemplate.from_messages(  # The alphabets that the software often gets confused between are: A, S, T, N and M; G and H; D and I; F and W; P and Q; R and U.
        [
            (
                "system",
                "You are meant to fix typos in given phrases. I will send you a phrase, please correct it. "
                "Do not rephrase anything, do not add punctuation, do not add or remove words, only correct typos. "
                "Please output nothing but the corrected phrase.",
            ),
            ("human", "{transcription}"),
        ]
    )
    RECEPTIVE_CHAIN = RECEPTIVE_PROMPT | llm

    EXPRESSIVE_PROMPT = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are meant to convert text from English to ASL Gloss grammar. Do not change meaning or move periods. I will send you a phrase, please rephrase it "
                "it to follow ASL grammar order: object, then subject, then verb. Remove words like IS and ARE that are not present in ASL. "
                "Replace I with ME. Do not add classifiers. Everything should be English text. Please output nothing but the rephrased phrase.",
            ),
            ("human", "{transcription}"),
        ]
    )
    EXPRESSIVE_CHAIN = EXPRESSIVE_PROMPT | llm

    @classmethod
    def fix(cls):

        Store.raw_word = ""
        current_length = len(Store.raw_transcription)

        raw_transcription = " ".join(Store.raw_transcription)
        response = LLM.RECEPTIVE_CHAIN.invoke(
            {
                "transcription": raw_transcription,
            }
        )

        Store.raw_transcription = (
            response.content.strip().upper().split()
            + Store.raw_transcription[current_length:]
        )

    def gloss(self, transcription):

        raw_transcription = " ".join(transcription)
        response = LLM.EXPRESSIVE_CHAIN.invoke(
            {
                "transcription": raw_transcription,
            }
        )

        print(response.content.strip())

        return response.content.strip().split()
