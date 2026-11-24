"""
Two-agent prototype for Group 1.

Demonstrates the worker that has the naive RAG tool, then the reflection agent.
The other three agents (planner, web search, summarizer) are specified in the
report and are not started here.
"""

from __future__ import annotations

import os

from crewai import Agent, Crew, Process, Task
from crewai.tools import tool
from dotenv import load_dotenv

from memory_store import remember
from rag_store import format_hits, search_health_kb
from router import EMERGENCY_MESSAGE, is_emergency

load_dotenv()


@tool("Search health knowledge base")
def search_health_knowledge_base(query: str) -> str:
    """Search the local health notes and return the most relevant passages with topic names."""
    return format_hits(search_health_kb(query, k=4))


def _model_name() -> str:
    return os.getenv("LLM_MODEL", "groq/openai/gpt-oss-20b")


def build_crew(question: str) -> Crew:
    model = _model_name()
    retriever = Agent(
        role="Health retrieval analyst",
        goal=(
            "Answer a research analyst's health question using only passages "
            "returned by the health knowledge-base tool."
        ),
        backstory=(
            "You prepare short research briefs. You never invent doses, "
            "diagnoses, or clinic addresses. You name the topic of each passage you use."
        ),
        tools=[search_health_knowledge_base],
        llm=model,
        verbose=True,
        allow_delegation=False,
    )
    reflector = Agent(
        role="Reflection reviewer",
        goal=(
            "Score the brief for faithfulness, safety, uncertainty, and usefulness, "
            "then rewrite it once if any score is weak."
        ),
        backstory=(
            "You do not search again. You judge the brief against the passages "
            "already quoted in it. You protect the reader from unsupported medical advice."
        ),
        tools=[],
        llm=model,
        verbose=True,
        allow_delegation=False,
    )
    retrieve_task = Task(
        description=(
            "Question from the research analyst:\n"
            f"{question}\n\n"
            "Use the health knowledge-base tool once. Then write a brief with:\n"
            "1. A direct answer in plain language.\n"
            "2. Two to four supporting points, each tied to a topic name from the tool.\n"
            "3. A limit: what this knowledge base cannot decide.\n"
            "If the passages do not contain the answer, say so. Do not use outside facts."
        ),
        expected_output="A sourced health research brief.",
        agent=retriever,
    )
    reflect_task = Task(
        description=(
            "Review the brief from the retrieval analyst. Score each item 1 or 0:\n"
            "- Faithfulness: every factual sentence is supported by a retrieved topic.\n"
            "- Safety: no diagnosis, no dose, no invented emergency instruction.\n"
            "- Uncertainty: missing information is admitted.\n"
            "- Usefulness: a research analyst can brief a reader from it.\n"
            "The metric is the sum out of 4. The pass threshold is 4.\n"
            "If the score is below 4, rewrite the brief so it passes.\n"
            "End with the four scores, the total, and the final brief."
        ),
        expected_output="Scores out of 4 and a final brief.",
        agent=reflector,
        context=[retrieve_task],
    )
    return Crew(
        agents=[retriever, reflector],
        tasks=[retrieve_task, reflect_task],
        process=Process.sequential,
        verbose=True,
    )


def run_research(question: str) -> dict:
    """Route emergencies away from the crew, otherwise run retrieval then reflection."""
    question = question.strip()
    if not question:
        raise ValueError("Enter a health question.")
    if is_emergency(question):
        result = {"route": "emergency", "answer": EMERGENCY_MESSAGE, "passages": []}
        remember({"question": question, **result})
        return result

    passages = search_health_kb(question, k=4)
    if not os.getenv("GROQ_API_KEY") and not os.getenv("MISTRAL_API_KEY"):
        answer = (
            "No model key was found, so the two agents did not run. "
            "Add GROQ_API_KEY or MISTRAL_API_KEY to the .env file. "
            "The passages below are what the retrieval tool would return."
        )
        result = {"route": "retrieval_only", "answer": answer, "passages": passages}
        remember({"question": question, "route": result["route"], "topics": [p["topic"] for p in passages]})
        return result

    crew_result = build_crew(question).kickoff()
    result = {
        "route": "retrieve_then_reflect",
        "answer": str(crew_result),
        "passages": passages,
    }
    remember(
        {
            "question": question,
            "route": result["route"],
            "topics": [item["topic"] for item in passages],
            "answer": result["answer"],
        }
    )
    return result
