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

    PROMPT = ChatPromptTemplate.from_messages(  # The alphabets that the software often gets confused between are: A, S, T, N and M; G and H; D and I; F and W; P and Q; R and U.
        [
            (
                "system",
                "You are an LLM meant to fix typos in given phrases. I will send you a phrase, please correct it. "
                "Do not rephrase anything, do not add punctuation, do not add or remove words, only correct typos. "
                "Please output nothing but the corrected phrase.",
            ),
            ("human", "{transcription}"),
        ]
    )
    CHAIN = PROMPT | llm

    @classmethod
    def fix(cls):

        Store.transcription.append(Store.raw_word)
        Store.raw_word = ""

        raw_transcription = " ".join(Store.raw_transcription)
        response = LLM.CHAIN.invoke(
            {
                "transcription": raw_transcription,
            }
        )

        Store.transcription = response.content.strip().upper().split()
