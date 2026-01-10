from agent_graph import app as graph
from langchain_core.messages import HumanMessage
import json
import uuid

def test_scenario(province, query, expected_keywords):
    print(f"\n\n==================================================")
    print(f"🧪 TESTING SCENARIO: {province}")
    print(f"📝 Query: \"{query}\"")
    print(f"==================================================")
    
    # 1. Run the Graph (with unique thread_id to avoid leakage)
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    initial_state = {"messages": [HumanMessage(content=query)]}
    
    final_state = graph.invoke(initial_state, config=config)
    
    # 2. Extract Response
    last_message = final_state["messages"][-1].content
    
    # 3. Parse JSON (Simulate Frontend)
    try:
        data = json.loads(last_message)
        explanation = data.get("explanation", "")
        citations = data.get("citations", [])
        
        print("\n✅ STATUS: SUCCESS (Valid JSON)")
        print(f"📄 Explanation Preview: {explanation[:150]}...")
        print(f"📚 Citations found: {len(citations)}")
        for c in citations:
            print(f"   - {c}")
            
        # 4. Keyword Verification
        print("\n🔎 Verifying Legitimate Legal Content:")
        missing = []
        for kw in expected_keywords:
            if kw.lower() in str(data).lower():
                print(f"   ✅ Found keyword: '{kw}'")
            else:
                print(f"   ❌ MISSING keyword: '{kw}'")
                missing.append(kw)
        
        if not missing:
            print(f"\n🎉 PASSED: {province} is using REAL DATA.")
        else:
            print(f"\n⚠️ WARNING: {province} might be hallucinating or missing context.")
            
    except json.JSONDecodeError:
        print("\n❌ FAILED: Response was not valid JSON.")
        print(f"Raw Output: {last_message}")

if __name__ == "__main__":
    print("🚀 STARTING COMPLETENESS VERIFICATION 🚀")
    print("Checking if we are really reading the full acts...")

    # Scenario 1: Ontario (Eviction)
    test_scenario(
        "ONTARIO", 
        "I live in Ontario. My landlord wants to kick me out for his son to move in.", 
        ["N12", "Bad Faith", "Section 48", "Compensation"]
    )

    # Scenario 2: BC (Rent)
    test_scenario(
        "BRITISH COLUMBIA", 
        "I am in BC. My landlord increased my rent by 10% this year.", 
        ["RTB", "Limit", "Notice", "Section 42", "Section 43"] 
    )

    # Scenario 3: Alberta (Mold/Maintenance) - The one we just fixed
    test_scenario(
        "ALBERTA", 
        "I live in Alberta. There is black mold in my basement suite and the landlord won't fix it.", 
        ["Breach", "Public Health", "14 days", "damages", "Section 16"]
    )

    # Scenario 4: Multi-Turn "Nudge" Test (Simulating a clueless user)
    print(f"\n\n==================================================")
    print(f"🧪 TESTING SCENARIO: Multi-Turn Nudge (Politeness & Context)")
    print(f"==================================================")
    
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    # Turn 1: Vague
    print("\n🗣️ User: 'I have a problem with my landlord.'")
    resp1 = graph.invoke({"messages": [HumanMessage(content="I have a problem with my landlord.")]}, config=config)
    last_msg1 = resp1["messages"][-1].content
    print(f"🤖 Agent: {last_msg1}")
    
    if "province" in last_msg1.lower() or "territory" in last_msg1.lower():
        print("   ✅ PASS: Agent asked for Location.")
    else:
        print("   ⚠️ FAIL: Agent did not ask for location.")

    # Turn 2: Location provided
    print("\n🗣️ User: 'I live in Toronto.'")
    resp2 = graph.invoke({"messages": [HumanMessage(content="I live in Toronto.")]}, config=config)
    last_msg2 = resp2["messages"][-1].content
    print(f"🤖 Agent: {last_msg2}")
    
    # Turn 3: Issue provided
    print("\n🗣️ User: 'He won't fix the AC.'")
    resp3 = graph.invoke({"messages": [HumanMessage(content="He won't fix the AC.")]}, config=config)
    last_msg3 = resp3["messages"][-1].content
    
    try:
        data = json.loads(last_msg3)
        print("\n✅ STATUS: Final Response is Valid JSON (Actionable)")
        print(f"📄 Explanation: {data.get('explanation', '')[:100]}...")
    except:
        print(f"❌ FAIL: Final response was not JSON. Got: {last_msg3}")
