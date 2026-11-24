"""Naive RAG store for the Group 1 health knowledge base."""

from __future__ import annotations

import shutil
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

BASE_DIR = Path(__file__).resolve().parent
CORPUS_PATH = BASE_DIR / "data" / "health_reference.txt"
PERSIST_DIRECTORY = str(BASE_DIR / "chroma_db")
COLLECTION_NAME = "health_rag_group1"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def load_sections() -> list[Document]:
    """Turn each markdown heading into a document with a topic name."""
    text = CORPUS_PATH.read_text(encoding="utf-8")
    sections = []
    current_title = "Overview"
    current_lines: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current_lines:
                sections.append((current_title, "\n".join(current_lines).strip()))
            current_title = line.replace("## ", "", 1).strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_lines:
        sections.append((current_title, "\n".join(current_lines).strip()))

    documents = []
    for title, body in sections:
        if not body:
            continue
        documents.append(
            Document(
                page_content=f"{title}\n{body}",
                metadata={"source": "health_reference.txt", "topic": title},
            )
        )
    return documents


def build_vector_store(rebuild: bool = False) -> Chroma:
    """Create or open the local Chroma collection."""
    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
    persist = Path(PERSIST_DIRECTORY)
    if rebuild and persist.exists():
        shutil.rmtree(persist)

    if persist.exists():
        return Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=PERSIST_DIRECTORY,
        )

    splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=120)
    chunks = splitter.split_documents(load_sections())
    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIRECTORY,
    )


def search_health_kb(query: str, k: int = 4) -> list[dict]:
    """Return the top passages for a health question."""
    store = build_vector_store()
    hits = store.similarity_search_with_score(query, k=k)
    results = []
    for document, score in hits:
        results.append(
            {
                "topic": document.metadata.get("topic", "Health note"),
                "source": document.metadata.get("source", "health_reference.txt"),
                "score": float(score),
                "text": document.page_content,
            }
        )
    return results


def format_hits(hits: list[dict]) -> str:
    """Plain text the retrieval agent can hand to the reflection agent."""
    if not hits:
        return "No passages were retrieved."
    blocks = []
    for index, hit in enumerate(hits, start=1):
        blocks.append(
            f"[{index}] Topic: {hit['topic']} | Source: {hit['source']}\n{hit['text']}"
        )
    return "\n\n".join(blocks)
