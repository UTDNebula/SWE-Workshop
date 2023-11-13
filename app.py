import base64
import pandas as pd
import streamlit as st

from langchain.embeddings.fastembed import FastEmbedEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import DataFrameLoader
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema import StrOutputParser
from langchain.prompts import PromptTemplate

from utils import format_as_doc, format_docs, llm


# Load the dataset from the data folder
@st.cache_data
def load_data(url="https://storage.googleapis.com/swe-workshop-23/organizations.json"):
    # TODO: load the data from the url
    pass


@st.cache_resource
def vectorize_data(df):
    # TODO: vectorize the data
    pass


# TODO: provide a prompt template
prompt = PromptTemplate.from_template("")


df = load_data()
docsearch = vectorize_data(df)
retriever = docsearch.as_retriever(search_kwargs={"k": 3})

chain = (
    # TODO: create the chain
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

    # TODO: bonus! add the organization's logo
