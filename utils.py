from langchain.llms import HuggingFaceTextGenInference

from io import BytesIO
from PIL import Image
from base64 import b64decode

llm = HuggingFaceTextGenInference(
    inference_server_url="https://hvxgjd4o670aom-8080.proxy.runpod.net/",
    max_new_tokens=512,
    do_sample=True,
    top_k=5,
)


def format_docs(docs):
    """Combine multiple documents, separated by three newlines"""
    return "\n\n\n".join([d.page_content for d in docs])


def format_as_doc(row):
    """Format a row of the dataset as a document, combining multiple data fields into a single page"""
    return f"Title: {row['title']}\nCategories: {', '.join(row['categories'])}\nDescription: {row['description']}\n"

def decode_image(encoded_image):
    return Image.open(BytesIO(b64decode(encoded_image)))