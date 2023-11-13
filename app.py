import base64
from utils import format_as_doc, format_docs, llm
import pandas as pd
import streamlit as st

from langchain.embeddings import HuggingFaceEmbeddings

from langchain.vectorstores import Chroma

from langchain.document_loaders import DataFrameLoader
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema import StrOutputParser
from langchain.prompts import PromptTemplate


# Load the dataset from the data folder
@st.cache_data
def load_data(url="https://storage.googleapis.com/swe-workshop-23/organizations.json"):
    df = pd.read_json(url)
    df["content"] = df.apply(format_as_doc, axis=1)
    return df


@st.cache_resource
def vectorize_data(df):
    loader = DataFrameLoader(df[["title", "content"]], page_content_column="content")
    documents = loader.load()
    embeddings = HuggingFaceEmbeddings()
    docsearch = Chroma.from_documents(documents, embeddings)
    return docsearch


prompt = PromptTemplate.from_template(
    """You are a student organization recommendation assistant. Given the user's \
    interests and some relevent search results from the campus student \
    organization directory, recommend a student organization on campus.

User Interests: {interests}

Search Results:
=============
{context}
=============

Given the users interests and some relvent search results from the campus student organization directory, the recommended organization is """
)


df = load_data()
docsearch = vectorize_data(df)
retriever = docsearch.as_retriever(search_kwargs={"k": 3})

chain = (
    {"context": retriever | format_docs, "interests": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


# Create a Streamlit app
st.title("Interests-based Prompt Generator")

# Create a text input field
user_interests = st.text_input("Enter your interests")

# Create a button
if st.button("Submit"):
    # Indicate the response is loading
    with st.spinner("Generating response..."):
        # Call the language model with the user's input
        response = chain.invoke(user_interests)

    st.write(response)

    # get club image if we can
    try:
        # grab the referenced club from the vector store
        club_doc = docsearch.similarity_search(response, k=1)[0]
        # grab the image from the dataframe
        image = df[df["title"] == club_doc.metadata["title"]]["picture_data"].values[0]
        # decode the image from base64
        image = base64.b64decode(image)
        # display the image
        st.image(image, use_column_width=True)
    except:
        pass
