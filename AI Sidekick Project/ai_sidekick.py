from typing import TypedDict, Annotated, List, Dict, Any, Optional

from langgraph.graph import StateGraph, START, END

from langgraph.checkpoint.memory import MemorySaver

from pydantic import BaseModel, Field

from langchain.agents import Tool

from langgraph.prebuilt import ToolNode, tools_condition

from IPython.display import display, Image

from langgraph.graph.message import add_messages

from langchain_groq import ChatGroq

import textwrap

import gradio as gr

import uuid

from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

import asyncio

from datetime import datetime

from langchain_openai import ChatOpenAI

from tool_base import playwright_tools, tool_team

from dotenv import load_dotenv

load_dotenv(override=True)

class State(TypedDict):

  messages: Annotated[List[Any], add_messages]

  success_criteria: str

  given_feedback: Optional[str]

  met_sucess_criteria: bool

  required_user_input: bool

class EvaluatorFeedback(BaseModel):

  feedback: str = Field(description= "Feedback on the assistant's performance")

  met_success_criteria: bool = Field(description= "Whether the success criteria has been met or not")

  required_user_input: bool = Field(description= "True if more user input is required, or clarifications, or assistant is stuck")

class AI_Sidekick:
  
  def __init__(self):

    self.assistant=None

    self.evaluator=None

    self.tools = None

    self.graph = None

    self.sidekick_id = str(uuid.uuid4())

    self.memory = MemorySaver()

    self.browser=None

    self.playwright=None

  async def ai_sidekick_setup(self):

    self.tools, self.browser, self.playwright = await playwright_tools()

    self.tools += await tool_team() 

    self.assistant = ChatGroq(model='llama-3.3-70b-versatile').bind_tools(self.tools)

    self.evaluator = ChatOpenAI(model= 'gpt-4o').with_structured_output(EvaluatorFeedback)

    await self.build_graph()

  def ai_assistant(self, state:State)->Dict[str, Any]:

   system_prompt = f"""

                  You are an exceptional assistant who leverages tools to complete tasks effectively and efficiently.

                  You seamlessly work on a given task untill when you have additional questions or clarifications for the user or when the success criteria is met and indeed you are wielding powerful tools in your arsenal to help you accomplish the user's tasks successfully.

                  Owning these tools, you can browse the internet, navigate and retrieve web pages, you can even run Python code but note that you need to include a 'print()' statement, if you want to extract the output.

                  The current date and time is: {datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}

                  This is the success criteria:

                  {state['success_criteria']}.

                  Your task is to respond either a question regarding additional user input if and only required by clearly elaborating what is needed for current assignment being performed or with the final response post completion of the assignment at hand.

                  An example question or clarification you can ask can be in the following way:

                  Question: Please confirm whether you want a crisp summary or a detailed breakdown.

                  Otherwise if you are done, then respond with the final output, JUST THE FINAL OUTPUT, NOT ANYTHING ELSE.

                  """


   if(state.get('given_feedback')):

     system_prompt += f"""

                     Previously, you thought the assignment was completed, but the success criteria was not met, thus got rejected.

                     Here is the feedback provided and the reason behind the rejection:

                     {state['given_feedback']}

                     Now with the given feedback, reiterate on the assignment and have a question for the user if and ONLY IF REQUIRED.

                     Analyze what has to be refined to improve and optimize the outcome and post that make the changes accordingly thus STRICTLY ensuring that you meet the success criteria.

                     """

   found_system_message = False

   messages = state['messages']

   for message in messages:

    if isinstance(message, SystemMessage):

      message.content = system_prompt

      found_system_message = True

   if not found_system_message:

    messages = [SystemMessage(content = system_prompt)] + messages

    assistant_response = self.assistant.invoke(messages)


   return {

          'messages': [assistant_response]
   }


  def route_ai_assistant(self, state:State)-> str:

      recent_message = state['messages'][-1]

      if hasattr(recent_message, 'tool_calls') and recent_message.tool_calls:

        return 'tools'

      else:

       return 'Evaluator'
      
  def format_conversation(self, messages:List[Any])-> str:

    conversation = "Conversation History:\n\n"

    for message in messages:

     if isinstance(message, HumanMessage):

      conversation += f"User: {message.content}\n"

     elif isinstance(message, AIMessage):

      text = message.content or ['Tool use']

      conversation += f"Assistant: {text}\n"

    return conversation
  
  def ai_evaluator(self, state:State)-> Dict[str, Any]:

   recent_response = state['messages'][-1].content

   system_prompt = f"""

                   You are an honest evaluator who evaluates the completion of assigments or tasks by the assistant, meaning if the task or assignment has been completed successfully or not.

                   Your task is to evaluate the assistant's recent response based on the given criteria. Respond with your feedback and your conclusion on whether the success criteria has been met and if more input is required from the user.

                   """

   user_prompt = f"""

                You are evaluating a conversation between a user and the assistant and you decide on what action to take based on the last or recent response.

                The entire conversation with the assistant, with the user's orginal request and all replies is:

                {self.format_conversation(state['messages'])}

                The success criteria for this assignment is:

                {state['success_criteria']}

                The final/recent response from the assistant that your evaluating is:

                {recent_response}

                Respond with your genuine and honest feedback, and review whether the success criteria is met by the response and whether more input from the user is required, either because the assistant has a question, requires clarification or seems to be stuck and unable to continue without additional assistance.

                """

   if state['given_feedback']:

    user_prompt += f"""

                   Also note that from a prior iteration from the assistant, you provided this feedback : {state['given_feedback']}\n

                   """

    user_prompt += f"""

                   If you notice that the assistant is repeating the same error over and over, consider asking it to obtain more inputs from the user

                   which will aid the assistant to deliver the expected output.

                   """

   evaluator_messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]

   evaluator_response = self.evaluator.invoke(evaluator_messages)

   updated_state = {

                   'messages': {'role': 'Assistant', 'content': f"Feedback from the evaluator:{evaluator_response.feedback}"},

                   'met_success_criteria' : evaluator_response.met_success_criteria,

                   'given_feedback': evaluator_response.feedback,

                   'required_user_input': evaluator_response.required_user_input
   }

   return updated_state
  
  def route_ai_evaluator(self, state:State)->str:

   if state['met_success_criteria'] or state['required_user_input']:

    return 'END'

   else:

    return 'Assistant'  
   
  async def build_graph(self):

    graph_builder = StateGraph(State)
    
    graph_builder.add_node('Assistant', self.ai_assistant)

    graph_builder.add_node('tools', ToolNode(tools=self.tools))

    graph_builder.add_node('Evaluator', self.ai_evaluator)

    graph_builder.add_conditional_edges('Assistant', self.route_ai_assistant, {'tools':'tools', 'Evaluator':'Evaluator'})

    graph_builder.add_edge('tools', 'Assistant')

    graph_builder.add_conditional_edges('Evaluator', self.route_ai_evaluator, {'Assistant':'Assistant', 'END': END})

    graph_builder.add_edge(START, 'Assistant')

    self.graph = graph_builder.compile(checkpointer=self.memory)
         
async def execute_graph_superstep(self, user_input, success_criteria, conversation_history):

  config = {'configurable' : {'thread_id': self.sidekick_id}}

  initial_state = {
      
                   'messages' : user_input,

                   'success_criteria': success_criteria,

                   'given_feedback': None,

                   'met_success_criteria': False,

                   'required_user_input': False
  }
  
  response = await self.graph.ainvoke(initial_state, config = config)

  user = {'role': 'user', 'content' : user_input}

  assistant_reply = {'role': 'assistant', 'content': response['messages'][-2].content}

  evaluator_feedback = {'role': 'assistant', 'content': response['messages'][-1].content}

  return conversation_history + [user, assistant_reply, evaluator_feedback]

def cleanup(self):
  
  if self.browser:

    try:
      
      loop = asyncio.get_running_loop()

      loop.create_task(self.browser.close())

      if self.playwright:

        loop.create_task(self.playwright.stop())
  
    except RuntimeError:
      
      asyncio.run(self.browser.close())

      if self.playwright:

        asyncio.run(self.playwright.stop())


        