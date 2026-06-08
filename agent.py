from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest

from model_embeddings import model, embeddings
from documents import loadPDF

# Give it a query, and wait for a response
async def getResponse(fileName : str, query : str):
    # Get the vector store
    vectorStore = loadPDF(fileName, embeddings)

    # Define the customPrompt function
    @dynamic_prompt
    def customPrompt(request : ModelRequest) -> str:
        # Get the latest query
        finalMsg = request.state["messages"][-1]
        query = finalMsg.content

        # Retrieve the chunks
        relevantDocs = vectorStore.similarity_search(query, k=5, filter={"id": fileName})
        context = "\n\n".join(
            (f"Content: {doc.page_content}")
            for doc in relevantDocs
        )

        # Return the prompt
        prompt = f"""
            You are a helpful assistant answering questions about a PDF.

            Use ONLY the context below to answer.
            If the answer is not in the context, say "I don't know".

            Context:
            {context}
            """
        return prompt

    # Initialize the agent
    agent = create_agent(model, tools=[], middleware=[customPrompt])

    # Pass the query into our agent
    for event in agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        stream_mode="values",
    ):
        finalMsg = event["messages"][-1].content

    return finalMsg