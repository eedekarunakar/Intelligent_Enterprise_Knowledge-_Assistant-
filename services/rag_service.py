from rag.prompt_template import SYSTEM_PROMPT


class RAGService:

    def __init__(

        self,

        retriever,

        chat_service

    ):

        self.retriever = retriever

        self.chat = chat_service

    def ask(self, question):

        docs = self.retriever.similarity_search(question)

        context = ""

        sources = []

        for doc in docs:

            context += doc.page_content + "\n\n"

            sources.append(

                doc.metadata.get(

                    "source",

                    "Unknown"

                )

            )

        prompt = SYSTEM_PROMPT.format(

            context=context,

            question=question

        )

        answer = self.chat.ask(prompt)

        return answer, list(set(sources))