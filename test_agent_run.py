import os
from marketing_agents import Agent, Runner

# Set dummy key for import/test if not present
if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = "mock-key"

agent = Agent(name="TestAgent", instructions="Say hello")
try:
    res = Runner.run_sync(agent, "hello")
    print("SUCCESS")
    for item in res.new_items:
        print("TYPE:", type(item))
        if hasattr(item, 'agent'):
            print("AGENT:", item.agent.name)
        if hasattr(item, 'raw_item'):
            print("RAW ITEM:", dir(item.raw_item))
            if hasattr(item.raw_item, 'content'):
                print("CONTENT:", item.raw_item.content)
except Exception as e:
    print("ERROR:", e)
