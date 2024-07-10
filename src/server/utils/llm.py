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

    def gloss(self, transcription):

        raw_transcription = " ".join(transcription)
        response = LLM.EXPRESSIVE_CHAIN.invoke(
            {
                "transcription": raw_transcription,
            }
        )

        print(response.content.strip())

        return response.content.strip().split()
