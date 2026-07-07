from langchain_groq import ChatGroq

from config.settings import GROQ_API_KEY


class ChatService:

    def __init__(self):

        self.llm = ChatGroq(

            groq_api_key=GROQ_API_KEY,

            model_name="llama-3.3-70b-versatile",

            temperature=0

        )

    def ask(self, prompt):

        response = self.llm.invoke(prompt)

        return response.content