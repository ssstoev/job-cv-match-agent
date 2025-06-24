import os
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]] # messages can be either AI or human message


llm = ChatOpenAI(model='gpt-4o')

def process_node(state: AgentState): 
    '''This node solves the request you input'''
    response = llm.invoke(state['messages'])
    state['messages'].append(AIMessage(content=response.content))
    print(f'AI response: {response.content}')

graph = StateGraph(AgentState)
graph.add_node('process', process_node)
graph.add_edge(START, 'process')
graph.add_edge('process', END)
agent = graph.compile()

# conversation_history = []

# with open("[SAMPLE] CV.txt", "r") as f:
#     cv_text = f.read()

# with open("[SAMPLE] job_description.txt", "r") as f:
#     jd_text = f.read()

# user_input = f"""
#     You are a professional recruiter. ANSWER WITH 1 SENTENCE.

#     Resume:
#     {cv_text}

#     Job Description:
#     {jd_text} 

#     Evaluate the match and return:
#     - Score from 0–100
#     - Strengths
#     - Weaknesses
#     - Suggestions
#     """

# while user_input != 'exit':
#     conversation_history.append(HumanMessage(content=user_input))
#     result = agent.invoke({'messages': conversation_history})
#     print("result['messages']: ", result['messages'])
#     conversation_history = result['messages']
#     user_input = input('Enter: ')

# with open('chat_history.txt', 'w') as file:
#     file.write('Your Conversation History:\n')
#     for message in conversation_history:
#         if isinstance(message, HumanMessage):
#             file.write(f'User: {message.content}\n')
#         elif isinstance(message, AIMessage):
#             file.write(f'AI: {message.content}\n\n')
#     file.write('Conversation END')

def run_agent(conversation: List[Union[HumanMessage, AIMessage]]) -> List[Union[HumanMessage, AIMessage]]:
    result = agent.invoke({'messages': conversation})
    return result['messages']