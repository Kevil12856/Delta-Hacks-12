import asyncio
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from agent_graph import app

load_dotenv()

async def run_test(test_name, inputs, thread_id):
    print(f"\n--- {test_name} ---")
    config = {"configurable": {"thread_id": thread_id}}
    
    # Process inputs
    async for output in app.astream(inputs, config=config):
        for node_name, state in output.items():
            print(f"Node: {node_name}")
            if "messages" in state:
                print(f"Response: {state['messages'][-1].content}")
            if "user_intent" in state:
                print(f"Intent: {state['user_intent']}")
            if "topic" in state:
                print(f"Topic: {state['topic']}")
            if "jurisdiction" in state:
                print(f"Jurisdiction: {state['jurisdiction']}")

async def main():
    # Test 1: Missing Jurisdiction
    print("\nTEST 1: Missing Jurisdiction Check")
    await run_test(
        "Start Conversation", 
        {"messages": [HumanMessage(content="My landlord is raising my rent.")]}, 
        "test-thread-101"
    )
    
    # Test 2: Provide Jurisdiction (Ontario)
    print("\nTEST 2: Provide Jurisdiction (Ontario)")
    await run_test(
        "Provide Jurisdiction",
        {"messages": [HumanMessage(content="I live in Ontario.")]},
        "test-thread-101"
    )

    # Test 3: Immigration (New Knowledge Base)
    print("\nTEST 3: Immigration Question (In DB)")
    await run_test(
        "Immigration Query",
        {"messages": [
            HumanMessage(content="I live in Ontario."),
            HumanMessage(content="How do I apply for a study permit extension?")
        ]},
        "test-thread-102"
    )

    # Test 4: Criminal Law (Now Supported)
    print("\nTEST 4: Criminal Law (Supported)")
    await run_test(
        "Criminal Query",
        {"messages": [
            HumanMessage(content="I live in Ontario."),
            HumanMessage(content="I was arrested for shoplifting. What is the maximum penalty?")
        ]},
        "test-thread-103"
    )

    # Test 5: Form Finding (Smart Tool)
    print("\nTEST 5: Find Form N12")
    await run_test(
        "Find Form",
        {"messages": [
            HumanMessage(content="I live in Ontario."),
            HumanMessage(content="Get me the N12 form.")
        ]},
        "test-thread-104"
    )

    # Test 6: Lawyer Finder (Smart Tool)
    print("\nTEST 6: Find a Lawyer")
    await run_test(
        "Find Lawyer",
        {"messages": [
            HumanMessage(content="I live in Ontario."),
            HumanMessage(content="I need to hire a criminal lawyer in Toronto.")
        ]},
        "test-thread-105"
    )

if __name__ == "__main__":
    asyncio.run(main())
