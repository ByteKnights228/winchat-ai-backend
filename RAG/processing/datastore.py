from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

from .summarizer import SimpleLLMSummarizer


import os
import shutil
from typing import Union

import logging

logger = logging.getLogger("__main__")


class DataStore:
    file_extension = "*.txt"
    embeddings = OllamaEmbeddings(
        model="llama3",
    )

    RECIPES = ["chunking", "summarization"]

    def __init__(self, chroma_path: str, data_path: str, embeddings:  Union[OllamaEmbeddings, OpenAIEmbeddings] = None, recepie: list = ["chunking"], surmarizer: SimpleLLMSummarizer = None) -> None:

        if embeddings:
            self.embeddings = embeddings

        self.chroma_path = chroma_path
        self.data_path = data_path
        self.summarizer = surmarizer

        for ingredient in recepie:
            if ingredient not in self.RECIPES:
                raise ValueError(
                    f"Recipe {ingredient} not supported. Supported recipes are {self.RECIPES}")
            if ingredient == "summarization" and not self.summarizer:
                raise ValueError(
                    f"Summarization recipe requires a summarizer function.")

        self.recipe = recepie

        logger.info(
            f"DataStore initialized with chroma_path: {chroma_path}, data_path: {data_path}")

    def load_documents(self, file_extension: str = "*.txt") -> list[Document]:
        self.file_extension = file_extension
        loader = DirectoryLoader(self.data_path, glob=self.file_extension)
        documents = loader.load()
        self.documents = documents
        return documents

    def generate_data_store(self, file_extension: str = "*.txt", chunk_size: int = 300, chunk_overlap: int = 100) -> None:
        self.file_extension = file_extension
        documents = self.load_documents()
        for ingredient in self.recipe:
            if ingredient == "chunking":
                chunks = self.split_text(
                    documents, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

            if ingredient == "summarization":
                chunks = self.summarizer.summarize_list(documents)

        self.save_to_chroma(chunks)

    def sentence_split(self, documents: list[Document]) -> list[Document]:
        # Split the documents into sentences.
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["."],
            length_function=len,
        )

    def split_text(self, documents: list[Document], chunk_size: int = 300, chunk_overlap: int = 100) -> list[Document]:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            add_start_index=True,
        )
        chunks = text_splitter.split_documents(documents)
        logger.info(
            f"Split {len(documents)} documents into {len(chunks)} chunks.")

        return chunks

    def save_to_chroma(self, chunks: list[Document]) -> None:
        # Clear out the database first.
        if os.path.exists(self.chroma_path):
            shutil.rmtree(self.chroma_path)

        # Create a new DB from the documents.

        batches = self.create_batches(chunks, batch_size=10)
        logger.info(f"Processing {len(batches)} batches.")
        i = 0
        for batch in batches:
            i += 1
            db = Chroma.from_documents(
                batch, self.embeddings, persist_directory=self.chroma_path,
                collection_metadata={"hnsw:space": "cosine"}
            )
            logger.info(
                f"Batch {i}:  Saved {len(batch) * i} chunks to chroma.")

    def create_batches(self, chunks: list[Document], batch_size: int = 10) -> None:

        batches = []
        # create batches of size batch_size
        last_batch = len(chunks) % batch_size
        for i in range(0, len(chunks) - last_batch, batch_size):
            batch = chunks[i:i + batch_size]
            batches.append(batch)

        batches.append(chunks[-last_batch:])

        return batches

    def __repr__(self) -> str:
        return f"DataStore(chroma_path={self.chroma_path}, data_path={self.data_path})"

    def __str__(self) -> str:
        return f"DataStore(chroma_path={self.chroma_path}, data_path={self.data_path})"


if __name__ == "__main__":
    # Load environment variables. Assumes that project contains .env file with API keys
    load_dotenv()

    CHROMA_PATH = "data\store\chroma"
    DATA_PATH = "data\store\\test"
    data_store = DataStore(chroma_path=CHROMA_PATH,
                           data_path=DATA_PATH)
    # data_store.generate_data_store()
