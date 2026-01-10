import os
from typing import TypedDict, Annotated, Sequence
import operator
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# --- State Definition ---
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    legal_issue: str
    relevant_laws: list[str]
    draft: str
    critique: str

# --- LLM Setup ---
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)

# --- Nodes ---

def triage_node(state: AgentState):
    """Determines the legal domain and issue."""
    messages = state['messages']
    last_message = messages[-1]
    
    prompt = f"""
    You are a Legal Triage Agent. Analyze the user's situation and classify it.
    Exract the distinct legal issue (e.g., "Eviction for Personal Use - N12").
    If it's not a legal issue, say "NOT_LEGAL".
    
    User Input: {last_message.content}
    """
    response = llm.invoke(prompt)
    return {"legal_issue": response.content}

def research_node(state: AgentState):
    """
    (Placeholder) Queries MongoDB/Vector Store for laws.
    For MVP, we will simulate this or use a basic keyword lookup if DB isn't ready.
    """
    issue = state.get("legal_issue", "")
    print(f"DEBUG: Researching issue: {issue}")
    
    # TODO: Replace with actual Vector Search call
    found_laws = [
        "Residential Tenancies Act, 2006, S.O. 2006, c. 17, s. 48 (Notice by Landlord at end of period or term)",
        "Residential Tenancies Act, 2006, S.O. 2006, c. 17, s. 83 (Refusal of eviction)"
    ]
    
    return {"relevant_laws": found_laws}

def drafter_node(state: AgentState):
    """Drafts the legal document based on research."""
    issue = state.get("legal_issue")
    laws = state.get("relevant_laws")
    messages = state['messages']
    
    prompt = f"""
    You are an expert Legal Drafter. 
    Issue: {issue}
    Relevant Laws: {laws}
    User Context: {messages[-1].content}
    
    Draft a formal response letter or form content.
    Cite the laws provided. 
    Add a disclaimer at the top.
    """
    response = llm.invoke(prompt)
    return {"draft": response.content}

# --- Graph Definition ---
workflow = StateGraph(AgentState)

workflow.add_node("triage", triage_node)
workflow.add_node("research", research_node)
workflow.add_node("drafter", drafter_node)

workflow.set_entry_point("triage")
workflow.add_edge("triage", "research")
workflow.add_edge("research", "drafter")
workflow.add_edge("drafter", END)

app = workflow.compile()

if __name__ == "__main__":
    # Test run
    inputs = {"messages": [HumanMessage(content="My landlord gave me an N12 but I think he just wants to raise the rent.")]}
    for output in app.stream(inputs):
        for key, value in output.items():
            print(f"Finished Node: {key}")
