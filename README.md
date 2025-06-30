# TestAgenticAiCoursera
Result of coursera course to build your own AgenticAI with Python &amp; ChatGPT from Coursera

# File Documentation
ASimpleAgentFramework.ipynb -> agent structure based on "Game" framework principals reading files from folder and document them
AgentLoopWithFunctionCalling.ipynb -> a simple agent reading files from folder and document them

# GAME framework
The GAME framework provides a structured way to design AI agents, ensuring modularity and adaptability. It breaks agent design into four essential components:

G - Goals / Instructions: What the agent is trying to accomplish and its instructions on how to try to achieve its goals.
A - Actions: The tools the agent can use to achieve its goals.
M - Memory: How the agent retains information across interactions, which determines what information it will have available in each iteration of the agent loop.
E - Environment: The agent’s interface to the external world where it executes actions and gets feedback on the results of those actions.