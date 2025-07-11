from dotenv import load_dotenv

from playwright.async_api import async_playwright

from langchain_community.agent_toolkits import PlayWrightBrowserToolkit

import os

import requests

from langchain.agents import Tool

from langchain_community.agent_toolkits import FileManagementToolkit

from langchain_community.tools.wikipedia.tool import WikipediaQueryRun

from langchain_experimental.tools import PythonREPLTool

from langchain_community.utilities import GoogleSerperAPIWrapper

from langchain_community.utilities.wikipedia import WikipediaAPIWrapper

load_dotenv(override=True)

pushover_user = os.getenv('PUSHOVER_USER_KEY')

pushover_token = os.getenv('PUSHOVER_USER_TOKEN')

pushover_url = f'https://api.pushover.net/1/messages.json'

serper_search_tool = GoogleSerperAPIWrapper()

async def playwright_tools():

    launch_playwright = await async_playwright().start()

    launch_playwright_browser = await launch_playwright.chromium.launch(headless=False)

    playwright_toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=launch_playwright_browser)

    return launch_playwright, launch_playwright_browser, playwright_toolkit.get_tools()

def send_push_notifications(notification_message: str):

    return requests.post(pushover_url, data = {'token': pushover_token, 'user': pushover_user, 'message' : notification_message})


def file_tools():

    file_toolkit = FileManagementToolkit(root_dir='sandbox')

    return file_toolkit.get_tools()


async def tool_team():

    push_notification_tool = Tool(
        
                                  name = 'Push Notification Tool', 
                                  
                                  func = send_push_notifications, 
                                  
                                  description= 'A tool for sending push notifications'
                                  
                                  )
    
    web_search_tool = Tool(

        name ='Web Search Tool',

        func = serper_search_tool.run(),

        description = 'A tool for performing web searches.'
    )
    
    file_management_tool = file_tools()

    wikipedia_tool = WikipediaAPIWrapper()

    wikipedia_search_tool = WikipediaQueryRun(api_wrapper= wikipedia_tool)

    python_coding_tool = PythonREPLTool()

    return file_management_tool + [push_notification_tool, wikipedia_tool, wikipedia_search_tool, python_coding_tool, web_search_tool]
