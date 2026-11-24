"""Diagrams, report, and slides for the Group 1 health project."""

import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "Assignment2"))

from report_doc import render_report
from report_draw import INK, NAVY, PALE, SAND, TEAL, arrow, canvas, font, label, save, sequence_diagram, text_box

OUT = ROOT / "diagrams"
OUT.mkdir(exist_ok=True)

MEMBERS = [
    "Shataer Abulizi",
    "Mohammad Alkhalifa",
    "Morel Eware Tatchim",
    "Joseph Ghobrial",
    "Etienne Zonon",
]


def architecture():
    image, draw = canvas(1600, 980, "Group 1 architecture: health research crew")
    text_box(draw, (40, 110, 300, 250), "Research analyst", "Asks a general health question and reads a sourced brief. Does not receive a diagnosis.", SAND)
    text_box(draw, (360, 110, 680, 250), "Streamlit client", "Sends the question, shows the route, the brief, and the retrieved passages.", PALE)
    text_box(draw, (740, 100, 1120, 270), "Planner  (level 1)", "Classifies the question: emergency, in-corpus research, needs a current public source, or out of scope. Writes the worker order. Does not answer from memory.", (226, 239, 241))
    text_box(draw, (1180, 110, 1540, 250), "Session memory", "JSON log of the question, the route, the topics used, and the final brief.", SAND)
    arrow(draw, (300, 180), (360, 180))
    arrow(draw, (680, 180), (740, 180))
    arrow(draw, (1120, 180), (1180, 180))

    workers = [
        (40, 400, 340, 620, "Retrieval worker", "Naive RAG tool over the local health notes in Chroma. Writes the first brief."),
        (380, 400, 700, 620, "Web-search worker", "Designed, not started in the prototype. Would search public health pages for a current schedule or notice."),
        (740, 400, 1060, 620, "Summarizer", "Designed. Merges retrieval and search notes into one analyst brief. The prototype lets the retrieval worker write that brief."),
        (1100, 400, 1540, 620, "Reflection worker", "Scores faithfulness, safety, uncertainty, and usefulness. Rewrites once if the total is under 4."),
    ]
    for box in workers:
        text_box(draw, box[:4], box[4], box[5], PALE)
    arrow(draw, (930, 270), (190, 400), TEAL)
    arrow(draw, (930, 270), (540, 400), TEAL)
    arrow(draw, (930, 270), (900, 400), TEAL)
    arrow(draw, (930, 270), (1300, 400), TEAL)
    text_box(draw, (40, 720, 700, 900), "Chroma collection health_rag_group1", "Chunks of data/health_reference.txt. Embedding model all-MiniLM-L6-v2. The retrieval tool is the only writer and the only reader.", SAND)
    arrow(draw, (190, 620), (300, 720), TEAL)
    label(draw, (760, 760), "Level 2 workers do not call each other.", font(20, True), NAVY)
    label(draw, (760, 810), "The reflector reads the brief. It does not get a search tool.", font(18), INK)
    label(draw, (760, 860), "An emergency question never reaches the workers.", font(18), INK)
    save(image, OUT / "architecture.png")


def workflows():
    image, draw = canvas(1600, 1100, "Workflow of each agent")
    rows = [
        (120, "Planner", "Read the question. If it matches an emergency phrase, stop and return the emergency notice. If it is outside health, refuse. Otherwise order retrieval, then reflection. Add web search only when the question needs a date or a local schedule."),
        (300, "Retrieval worker", "Call the RAG tool once. Read the four passages. Write a short brief that names each topic it used. If the passages do not contain the answer, say so. Do not add a dose or a diagnosis."),
        (480, "Web-search worker", "Designed only. Build a narrow query. Open public pages from the allowed sources. Keep a sentence only with its URL. Drop pages that are not a health authority. Hand the notes to the summarizer."),
        (660, "Summarizer", "Designed only. Merge the retrieval brief and the search notes. One answer, the supporting points, the limits. The prototype skips this agent and lets the retrieval worker produce that shape."),
        (840, "Reflection worker", "Score four checks, each 0 or 1: faithfulness, safety, uncertainty, usefulness. The metric is the sum out of 4. The pass mark is 4. Below 4, rewrite once from the same passages and score again."),
    ]
    for y, title, body in rows:
        text_box(draw, (40, y, 280, y + 140), title, "Level 1" if title == "Planner" else "Level 2", SAND if title == "Planner" else PALE)
        text_box(draw, (320, y, 1540, y + 140), "Steps", body, (255, 255, 255))
    save(image, OUT / "workflows.png")


def component():
    image, draw = canvas(1500, 780, "UML component view of the prototype")
    text_box(draw, (40, 140, 320, 320), "Streamlit UI", "Required interface: IQuestion.\nProvided interface: IBrief.", PALE)
    text_box(draw, (400, 140, 720, 320), "Safety router", "Provided interface: IRoute.\nValues: emergency or research.", PALE)
    text_box(draw, (800, 120, 1140, 340), "Retrieval agent\n+ RAG tool", "Required: IRoute, IVectorRead.\nProvided: IDraft.", PALE)
    text_box(draw, (1220, 140, 1460, 320), "ChromaDB", "Provided: IVectorRead.\nExternal store.", SAND)
    arrow(draw, (320, 220), (400, 220))
    arrow(draw, (720, 220), (800, 220))
    arrow(draw, (1140, 220), (1220, 220))
    text_box(draw, (400, 460, 760, 660), "Reflection agent", "Required: IDraft.\nProvided: IReviewedBrief.\nNo tool.", PALE)
    text_box(draw, (860, 460, 1220, 660), "Session memory", "Required: IReviewedBrief.\nJSON file, external to the model.", SAND)
    arrow(draw, (970, 340), (580, 460), TEAL)
    arrow(draw, (760, 560), (860, 560))
    label(draw, (40, 700), "IQuestion, IRoute, IDraft, and IReviewedBrief are internal. IVectorRead and the JSON file are external.", font(18), NAVY)
    save(image, OUT / "component.png")


MARKUP = """
# Health enquiry research assistant
# COMP 248 team project  |  Group 1  |  Field: health enquiries
# Section: 25F, AI Systems Design (ESC 402). Confirm the section number on the dropbox before upload.

## Cover

Team members: Shataer Abulizi, Mohammad Alkhalifa, Morel Eware Tatchim, Joseph Ghobrial, Etienne Zonon.

The main actor is a research analyst. The system helps that person research and summarize general health questions. It is not a clinician, and it is not a medical device.

## Table of contents

1. Rationale and scope
2. Research
3. Agents
4. Naive RAG
5. Reflection
6. Knowledge base and data model
7. Diagrams
8. Responsible AI
9. Prototype
10. Conclusion
11. Assumptions
12. References
13. Appendix: meeting register

## 1. Rationale and scope

A research analyst gets broad health questions from the public: how a cold differs from influenza, when fever needs a clinic, what a blood-pressure reading is for. The answers exist, but they are spread across fact sheets. The analyst needs a short brief with the passage it came from, not a chatbot that invents a dose.

The scope is general, non-urgent health explanation. In scope: colds and influenza, fever, emergency warning signs, blood pressure, diabetes in outline, vaccination in outline, medication safety, mental-health help-seeking, hand hygiene, food, activity, and sleep. Out of scope: a personal diagnosis, a dose, a prescription, a clinic address, and any question that describes a possible emergency. Those last questions receive a fixed notice to contact local emergency or crisis services. They are not summarized.

The design allows five agents. The prototype runs two of them: the retrieval worker, which has the RAG tool, and the reflection worker.

## 2. Research

### 2.1 Source chosen for the field

The production source is MedlinePlus, from the U.S. National Library of Medicine, supported by World Health Organization fact sheets for the same public topics. Both are written for a general reader, they name their reviewers, and they are stable enough to cite. A web search of the open internet was rejected as the primary source. Commercial pages and forums mix advertising with advice, and a research brief that quotes them is hard to defend.

The prototype does not download those sites at runtime. data/health_reference.txt is an original course corpus written along those public themes, with a section per topic. That choice keeps the demonstration offline and avoids copying a fact sheet into the repository. The retrieval tool points at a topic title inside this file. A later build can replace the file with a licensed extract of MedlinePlus without changing the agent.

### 2.2 Measures for the naive RAG tool

Four measures, taken from the RAGAS set, which is a common evaluation for retrieval-augmented answers.

Faithfulness. Each sentence in the brief is supported by a retrieved passage. This is the measure that matters most in health. A fluent unsupported sentence is a failure even if the reader likes it.

Answer relevancy. The brief addresses the analyst's question rather than a neighbouring topic. A question about fever should not come back as a vaccination leaflet.

Context precision. Of the four passages returned, how many are actually useful. Naive RAG with a small embedding model will sometimes return a neighbour. The measure makes that visible.

Context recall. The passages cover the facts the corpus does contain for that question. A brief can be faithful and still miss half of the relevant section if recall is poor.

The prototype does not compute RAGAS automatically. It stores the topics that were retrieved, so a person can score a set of questions by hand. The reflection worker is a live, coarse version of faithfulness and safety, not a replacement for a labeled test set.

## 3. Agents

The hierarchy has two levels. The planner is level 1. The other four agents are level 2 workers. Workers do not delegate to each other. The planner does not answer the health question itself.

TABLE
Agent | Level | LLM | Tools | Responsibility
Planner | 1 | A strong instruction model, temperature 0.1. Default in the lab environment: groq/openai/gpt-oss-20b. Mistral is the alternate. | None | Route the question and name the worker order. Routing errors are expensive, so this is the model with the best instruction following the team can afford. No tool, because a planner with a search tool starts doing the workers' jobs.
Retrieval worker | 2 | Same model family, temperature 0 | Naive RAG over Chroma | One search of the health notes, then a brief that names topics. Temperature 0 keeps the brief close to the passages.
Web-search worker | 2 | Same model, temperature 0 | A search tool limited to public-health domains | Current notices and local vaccine schedules, which a frozen corpus cannot know. Not started in the prototype.
Summarizer | 2 | Same model, temperature 0.2 | None | Merge retrieval notes and search notes into one brief. Not started. The prototype's retrieval worker writes that shape directly, because there is only one source.
Reflection worker | 2 | Same model, temperature 0 | None | Score the brief and rewrite it once if the score is under 4. No tool, so it cannot wander off and fetch a new page to justify a weak sentence.
ENDTABLE

Why one model family. Two vendors would mean two keys, two failure modes, and two data-processing agreements. The planner and the workers can still be different sizes later. The interface stays a model name in .env.

Why the web-search worker exists in the design and not in the code. A question such as "what is this year's influenza vaccine advice in my province" cannot be answered from the local file. Pretending the file is enough would be a grounding failure. Leaving the worker on the diagram, and off the demo, is the honest cut. The assignment asks the prototype to show one tool-using agent and the reflective agent, not all five.

IMAGE workflows.png | Figure 1. One workflow per agent. The planner is level 1. The other four are level 2.

## 4. Naive RAG

The tool is naive RAG: split, embed, retrieve a fixed number of chunks, stuff them into the prompt. There is no reranker, no query rewrite, and no agent loop inside the tool.

The corpus is split with RecursiveCharacterTextSplitter, chunk size 900, overlap 120. Embeddings are all-MiniLM-L6-v2, the same local model used in the course labs. Chroma persists at chroma_db under the collection health_rag_group1. The tool returns four passages with the topic title and the file name.

Naive is the right first design because the corpus is small and the questions are topical. A 900-character chunk usually holds one health point in full. Overlap 120 keeps a sentence that sits on a boundary. The trade-off is familiar: a question that uses different words from the notes can miss the section, and four passages can include a neighbour. Context precision is how the team would see that. A reranker is the first upgrade if precision is poor. It is not in this build, because the assignment asks for naive RAG.

The retrieval agent may call the tool once. A second call with a rephrased query would be a different pattern, and it would make the reflection step harder to audit.

## 5. Reflection

The metric is a four-point checklist. Each item is 1 or 0.

Faithfulness. Every factual sentence is tied to a retrieved topic.
Safety. No diagnosis, no dose, no invented emergency instruction.
Uncertainty. The brief says when the notes do not contain the answer.
Usefulness. An analyst can brief a reader from it without adding medical claims.

The score is the sum, from 0 to 4. The pass threshold is 4. Any failed item fails the brief. An average would let a useful but unsafe sentence through, which is the wrong trade in this field.

The workflow is introspective and short. The reflector reads the draft and the topics already inside it. It does not search. If the score is below 4, it rewrites once, using only the same passages, and reports the new scores. One rewrite is the limit. A longer loop burns time and tends to sand the brief down into vagueness. If the second score is still below 4, the brief is returned with the scores visible so the analyst can see the weakness. The system does not hide a failed check.

Why not a model-graded percentage. A 0.73 from another model is difficult to explain in a presentation, and it moves when the grader model moves. Four named checks can be defended one by one. The cost is that the same model family writes the brief and marks it, so it can be generous. The stored passages let a person audit the score. A sample of briefs should be rescored by the team before the demonstration.

## 6. Knowledge base and data model

There are two stores. They are not interchangeable.

Vector store. Chroma collection health_rag_group1. One row per chunk.

TABLE
Field | Meaning
chunk_id | Identity inside Chroma
topic | Section title, such as Fever and when to seek care
source | health_reference.txt
text | The chunk
embedding | MiniLM vector, stored by Chroma, not by the agents
ENDTABLE

Who uses it. Only the retrieval worker, through the RAG tool. The planner, the summarizer, and the reflector do not query it. The web-search worker, if it is built, must not write pages into this collection during a session. Mixing live web text into the trusted notes would make faithfulness impossible to explain. A reviewed page could be added later, offline, as a new source file.

Session memory. data/session_memory.json. One object per run.

TABLE
Field | Meaning
saved_at | When the run was stored
question | The analyst's question, as typed
route | emergency, retrieval_only, or retrieve_then_reflect
topics | Topic titles returned by Chroma
answer | The final brief, when the crew ran
ENDTABLE

Who uses it. The Streamlit path appends a record after every run, including an emergency refusal. The agents do not read it back in this prototype. It is the audit log and the seed of a longer memory. It is not a medical record. The analyst's name is not stored.

The emergency router is not a store. It is a word list in router.py. Putting it in code, rather than in the vector store, means a phrasing change is a reviewed edit. It also means the refusal does not depend on retrieval. A missed nearest-neighbour must not be what decides whether chest pain gets a literature summary.

IMAGE architecture.png | Figure 2. Planner above four workers. Chroma is the retrieval worker's store. Session memory is outside the model.

## 7. Diagrams

### 7.1 Components

IMAGE component.png | Figure 3. Components that the prototype actually runs, with the interfaces between them.

IQuestion and IBrief are the analyst's edge. IRoute is the safety decision. IVectorRead is the external Chroma interface. IDraft is the retrieval worker's brief. IReviewedBrief is what the reflector returns and what the session log stores. Internal interfaces stay inside the process. Chroma and the JSON file are external because they outlive the request.

### 7.2 Interaction

IMAGE sequence.png | Figure 4. Sequence for a non-emergency question. An emergency question returns on the third message and does not call Chroma or the crew.

The analyst is outside the crew. Streamlit calls the router first. Only a research route builds the crew. The retrieval agent calls the tool, which reads Chroma. The reflector runs second, with the draft as its context, and does not call the tool. The log is written after the brief exists. This matches the CrewAI process in crew_prototype.py: two tasks, sequential, no delegation.

## 8. Responsible AI

Privacy. The questions are health questions. The session log keeps the question text, so a person who types a name or a diagnosis into the box will have that text on disk. The interface should say not to type identifying details. The log has no account id. The corpus has no patient data. Prompts sent to Groq or Mistral leave the machine. A deployment inside a clinic would need a model the health organization is allowed to use, and it would need to stop sending free-text symptoms to a course API key. This prototype is for the course demonstration, on general questions.

Fairness. The notes are in English, they follow North American and WHO public themes, and they are short. They under-serve people who need another language, a pediatric detail, or a condition the file does not mention. The brief is required to say when the file has no answer, which is the protection against inventing a culturally specific rule. Pregnancy, infants, and a weakened immune system are named as cases that need a clinician, because a general adult sentence is the wrong default there.

Explainability. Every brief should name the topic it used, and the screen shows the passages with their distance scores. The reflection scores are part of the answer, not a hidden log. An analyst can disagree with the brief by reading the same passage.

Health safety. No diagnosis, no dose, no treatment plan for a named person. Emergency phrasing is routed away from the model. The corpus itself tells the reader that the notes are not a medical device. This is the constraint that outranks a complete answer.

Accountability. The research analyst remains the person who speaks to the public. The system prepares a brief. It does not publish one. The team can explain each design cut: naive RAG, one rewrite, no web tool in the demo, emergency list in code.

## 9. Prototype

The prototype is a Streamlit application, app.py. The crew is built with CrewAI. The RAG tool uses LangChain's Chroma integration and SentenceTransformer embeddings. The two agents are the retrieval analyst, which owns the tool, and the reflection reviewer, which has no tool.

Run it from the Team_project folder.

pip install -r requirements.txt
copy .env.example to .env and set GROQ_API_KEY, or set MISTRAL_API_KEY and LLM_MODEL=mistral/mistral-small-latest
streamlit run app.py

Without a key, the page still retrieves passages and says the crew did not run. With a key, the crew writes the brief and the reflector appends the four scores. An emergency question, for example a message about chest pain, returns the fixed notice and does not call the model.

What was left out on purpose. The planner's full classification is a word-list emergency check plus a default research route. The web-search worker and the separate summarizer are in the design and not in the process. Building them would have broken the assignment's prototype limit of one tool-using agent and the reflective agent.

## 10. Conclusion

Group 1's system is a two-level crew for a research analyst working on general health questions. The planner routes. One worker retrieves from a small trusted corpus with naive RAG. One worker reflects with a four-point score and a single rewrite. Two further workers, web search and a separate summarizer, are specified so the design is complete, and they are not in the demo. The knowledge is split into a vector store the retrieval tool alone can read, and a session log that records the route and the topics. The safety choice is to refuse emergencies and to refuse unsupported medical detail, even when that makes the brief shorter.

## 11. Assumptions

The section code on the group page is 25F / ESC 402. The upload name may need a numeric section. The suggested file name is COMP248_project_health_team1, with the section inserted once it is confirmed.

The corpus is a teaching summary aligned with MedlinePlus and WHO themes. It is not those organizations' text, and it is not complete.

The default model is the Groq model already used in the week 9 labs. A Mistral model name is supported through LLM_MODEL. No API key is stored in the repository.

The emergency list is a keyword list. It will miss paraphrases and it will sometimes fire on a question that only mentions chest pain as a topic. The team accepts the false alarms. A missed emergency is the worse error, but a keyword list is not a clinical triage system, and the screen should not be used as one.

Peer scores and the meeting register in the appendix have to describe the work the five members actually did. The rows below are a blank register for the team to complete. They are not a claim that a meeting occurred.

## 12. References

MedlinePlus, U.S. National Library of Medicine. Consumer health topics used as the intended production source.

World Health Organization. Fact sheets used as the second public source for the same themes.

Lewis, P. et al. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. 2020. The naive RAG pattern used by the tool.

Es, S. et al. RAGAS: Automated Evaluation of Retrieval Augmented Generation. 2023. Source of faithfulness, answer relevancy, context precision, and context recall.

CrewAI documentation. Sequential process, agents, and tools, as used in crew_prototype.py.

LangChain documentation. Chroma vector store and recursive character splitter.

Sentence-Transformers, all-MiniLM-L6-v2. Local embedding model.

## 13. Appendix 1. Meeting register

Complete this table from the meetings the team actually held. Do not leave the sample rows in the uploaded report if those meetings did not happen.

TABLE
Date and time | Attended | Subjects | Assignments
To be filled | To be filled | To be filled | To be filled
To be filled | To be filled | To be filled | To be filled
To be filled | To be filled | To be filled | To be filled
ENDTABLE

Roster: Shataer Abulizi, Mohammad Alkhalifa, Morel Eware Tatchim, Joseph Ghobrial, Etienne Zonon.
"""


def build_slides():
    presentation = Presentation()
    presentation.slide_width = Inches(13.333)
    presentation.slide_height = Inches(7.5)
    navy = RGBColor(0x1B, 0x3A, 0x4B)

    slides = [
        ("Health enquiry assistant", "COMP 248  |  Group 1  |  Health enquiries\n" + "\n".join(MEMBERS)),
        ("The job", "A research analyst needs a short, sourced brief on a general health question.\nThe system is not a clinician and does not give a dose or a diagnosis.\nEmergencies are refused and pointed to local emergency or crisis services."),
        ("Five agents, two levels", "Planner, level 1: route the question. No tools.\nRetrieval worker: naive RAG over the local health notes.\nWeb-search worker: designed, not in the demo.\nSummarizer: designed, not in the demo.\nReflection worker: score the brief, rewrite once if needed."),
        ("Naive RAG", "Source themes: MedlinePlus and WHO fact sheets.\nThe demo corpus is an original course file, one section per topic.\nChroma collection health_rag_group1, MiniLM embeddings, four passages.\nMeasures: faithfulness, answer relevancy, context precision, context recall."),
        ("Reflection", "Four checks, each 0 or 1: faithfulness, safety, uncertainty, usefulness.\nThe metric is the sum out of 4. The pass mark is 4.\nOne rewrite, from the same passages. No new search.\nA failed check stays visible to the analyst."),
        ("Knowledge and responsibility", "Chroma is read only by the retrieval tool.\nThe session log stores the question, the route, and the topics. No patient record.\nEnglish public-health notes will miss people and conditions. The brief must say when it has no answer.\nThe analyst, not the crew, is accountable for what is said to the public."),
        ("Prototype", "Streamlit front end.\nCrewAI runs the retrieval agent and the reflection agent.\nThe retrieval agent is the only one with a tool.\nWithout an API key the page still shows the retrieved passages.\nWith a key, the brief includes the four scores."),
        ("What we are showing today", "One question the corpus can answer, with passages on screen.\nOne question the corpus cannot answer, and the refusal.\nOne emergency phrase, stopped before the model.\nThe design cuts: no web agent in the demo, one rewrite, naive RAG."),
    ]

    for title, body in slides:
        layout = presentation.slide_layouts[6]
        slide = presentation.slides.add_slide(layout)
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        bar = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.333), Inches(0.4))
        bar.fill.solid()
        bar.fill.fore_color.rgb = navy
        bar.line.fill.background()
        title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.7), Inches(12), Inches(1))
        title_run = title_box.text_frame.paragraphs[0].add_run()
        title_run.text = title
        title_run.font.size = Pt(36)
        title_run.font.bold = True
        title_run.font.color.rgb = navy
        title_run.font.name = "Calibri"
        body_box = slide.shapes.add_textbox(Inches(0.6), Inches(2.0), Inches(12), Inches(4.8))
        frame = body_box.text_frame
        frame.word_wrap = True
        for line_index, line in enumerate(body.split("\n")):
            paragraph = frame.paragraphs[0] if line_index == 0 else frame.add_paragraph()
            run = paragraph.add_run()
            run.text = line
            run.font.size = Pt(24)
            run.font.color.rgb = RGBColor(0x21, 0x25, 0x29)
            run.font.name = "Calibri"
            paragraph.space_after = Pt(12)

    destination = ROOT / "COMP248_project_health_team1_slides.pptx"
    presentation.save(destination)
    print(destination)


def build_peer_form():
    markup = """
# COMP 248 peer evaluation form  |  draft for Etienne Zonon
# Fill this in yourself before you upload it. It is confidential.

Date: complete on the day you submit
Term: Fall
Name: Etienne Zonon
Student number: 301559049
Section: 25F / ESC 402 (confirm)
Group: 1

## What I contributed

Replace this paragraph with the work you actually did. A starting point, if it is true, is the health-enquiry design, the retrieval and reflection prototype, and the written report. Do not leave this paragraph unchanged if the team divided the work differently.

## Scores

Write a percentage for each person, including yourself. Use 100 only if that person did the share the team agreed. Use 0 if they did not contribute. Use a number in between if they contributed less than the team agreed. Do not submit a score you cannot stand behind.

TABLE
Team member | Evaluation out of 100 percent
Shataer Abulizi | 
Mohammad Alkhalifa | 
Morel Eware Tatchim | 
Joseph Ghobrial | 
Etienne Zonon | 
ENDTABLE
"""
    render_report(markup, ROOT / "EtienneZonon_peer_evaluation_DRAFT.docx", OUT)


if __name__ == "__main__":
    architecture()
    workflows()
    component()
    sequence_diagram(
        OUT / "sequence.png",
        "Research question sequence",
        ["Analyst", "Streamlit", "Router", "Retriever", "Chroma", "Reflector"],
        [
            (0, 1, "health question"),
            (1, 2, "classify"),
            (2, 1, "research, or emergency stop"),
            (1, 3, "ask for a brief"),
            (3, 4, "RAG search, k=4"),
            (4, 3, "passages and topics"),
            (3, 5, "draft plus topics"),
            (5, 1, "scores and final brief"),
            (1, 0, "show brief and passages"),
        ],
    )
    render_report(MARKUP, ROOT / "COMP248_project_health_team1_report.docx", OUT)
    build_slides()
    build_peer_form()
