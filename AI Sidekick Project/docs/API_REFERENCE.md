# AI Sidekick API Reference

## Overview

This document provides detailed API reference for all components of the AI Sidekick system, including tools, functions, and interfaces.

## Core Classes

### AI_Sidekick Class

The main orchestrator class that manages the AI workflow.

#### Constructor
```python
def __init__(self):
    self.assistant = None
    self.evaluator = None
    self.tools = None
    self.graph = None
    self.sidekick_id = str(uuid.uuid4())
    self.memory = MemorySaver()
    self.browser = None
    self.playwright = None
```

#### Methods

##### `async ai_sidekick_setup()`
Initializes the AI Sidekick with all tools and models.

**Returns**: None

**Side Effects**: 
- Initializes browser automation
- Sets up AI models (Groq and OpenAI)
- Builds the workflow graph

##### `ai_assistant(state: State) -> Dict[str, Any]`
Main assistant function that processes user requests.

**Parameters**:
- `state`: Current state containing messages and success criteria

**Returns**: Dictionary with updated messages

**Behavior**:
- Analyzes user input
- Determines required tools
- Generates responses using Groq model

##### `ai_evaluator(state: State) -> Dict[str, Any]`
Evaluates whether the assistant's work meets success criteria.

**Parameters**:
- `state`: Current state with messages and criteria

**Returns**: Dictionary with evaluation feedback

**Behavior**:
- Analyzes assistant's response
- Compares against success criteria
- Provides structured feedback

##### `route_ai_assistant(state: State) -> str`
Routes the workflow after assistant processing.

**Parameters**:
- `state`: Current state

**Returns**: String indicating next node ('tools' or 'Evaluator')

##### `route_ai_evaluator(state: State) -> str`
Routes the workflow after evaluation.

**Parameters**:
- `state`: Current state

**Returns**: String indicating next node ('Assistant' or 'END')

##### `async build_graph()`
Constructs the LangGraph workflow.

**Returns**: None

**Side Effects**: Creates the workflow graph with nodes and edges

##### `async execute_graph_superstep(user_input, success_criteria, conversation_history)`
Executes one complete workflow cycle.

**Parameters**:
- `user_input`: User's request
- `success_criteria`: Success criteria string
- `conversation_history`: Previous conversation

**Returns**: Updated conversation history

##### `cleanup()`
Cleans up resources (browser, playwright).

**Returns**: None

## Tool Reference

### Browser Automation Tools

#### Playwright Browser Toolkit
**Purpose**: Web automation and interaction

**Available Actions**:
- Navigate to URLs
- Click elements
- Fill forms
- Extract text
- Take screenshots
- Handle popups and dialogs

**Setup**:
```python
async def playwright_tools():
    launch_playwright = await async_playwright().start()
    launch_playwright_browser = await launch_playwright.chromium.launch(headless=False)
    playwright_toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=launch_playwright_browser)
    return launch_playwright, launch_playwright_browser, playwright_toolkit.get_tools()
```

### File Management Tools

#### FileManagementToolkit
**Purpose**: File system operations

**Available Operations**:
- Create directories
- List files
- Read file contents
- Write files
- Delete files
- Copy/move files

**Setup**:
```python
def file_tools():
    file_toolkit = FileManagementToolkit(root_dir='sandbox')
    return file_toolkit.get_tools()
```

### Web Search Tools

#### Google Serper API
**Purpose**: Internet search capabilities

**Features**:
- Web search
- News search
- Image search
- Shopping search

**Setup**:
```python
web_search_tool = GoogleSerperAPIWrapper()
```

### Information Retrieval Tools

#### Wikipedia Tools
**Purpose**: Access Wikipedia information

**Available Tools**:
- `WikipediaAPIWrapper`: Direct Wikipedia API access
- `WikipediaQueryRun`: Structured Wikipedia queries

**Setup**:
```python
wikipedia_tool = WikipediaAPIWrapper()
wikipedia_search_tool = WikipediaQueryRun(api_wrapper=wikipedia_tool)
```

### Code Execution Tools

#### PythonREPLTool
**Purpose**: Dynamic Python code execution

**Features**:
- Execute Python code
- Variable manipulation
- Data processing
- Mathematical calculations

**Setup**:
```python
python_coding_tool = PythonREPLTool()
```

### Notification Tools

#### Push Notification Tool
**Purpose**: Send push notifications to mobile devices

**Setup**:
```python
def send_push_notifications(notification_message: str):
    return requests.post(pushover_url, data={
        'token': pushover_token, 
        'user': pushover_user, 
        'message': notification_message
    })

push_notification_tool = Tool(
    name='Push Notification Tool',
    func=send_push_notifications,
    description='A tool for sending push notifications'
)
```

## Data Structures

### State TypedDict
```python
class State(TypedDict):
    messages: Annotated[List[Any], add_messages]  # Conversation history
    success_criteria: str                          # User-defined criteria
    given_feedback: Optional[str]                  # Previous evaluation feedback
    met_success_criteria: bool                     # Current success status
    required_user_input: bool                      # Whether user input is needed
```

### EvaluatorFeedback Model
```python
class EvaluatorFeedback(BaseModel):
    feedback: str = Field(description="Feedback on the assistant's performance")
    met_success_criteria: bool = Field(description="Whether the success criteria has been met or not")
    required_user_input: bool = Field(description="True if more user input is required, or clarifications, or assistant is stuck")
```

## User Interface API

### Gradio Interface Functions

#### `async sidekick_agent_setup()`
Creates and initializes a new AI Sidekick instance.

**Returns**: AI_Sidekick instance

#### `async process_user_and_agent_interactions(sidekick, user_input, success_criteria, conversation_history)`
Processes user input through the AI workflow.

**Parameters**:
- `sidekick`: AI_Sidekick instance
- `user_input`: User's request
- `success_criteria`: Success criteria
- `conversation_history`: Previous conversation

**Returns**: Tuple of (sidekick, result)

#### `async start_new_session()`
Creates a fresh AI Sidekick session.

**Returns**: Tuple of (empty_input, empty_criteria, empty_history, new_sidekick)

#### `clear_resources(sidekick)`
Cleans up resources for a sidekick instance.

**Parameters**:
- `sidekick`: AI_Sidekick instance to clean up

**Returns**: None

## Configuration

### Environment Variables

#### Required Variables
```env
# OpenAI API (for evaluator)
OPENAI_API_KEY=your_openai_api_key_here

# Google Serper API (for web search)
SERPER_API_KEY=your_serper_api_key_here
```

#### Optional Variables
```env
# Pushover (for notifications)
PUSHOVER_USER_KEY=your_pushover_user_key_here
PUSHOVER_USER_TOKEN=your_pushover_token_here
```

### Model Configuration

#### Assistant Model (Groq)
- **Model**: `llama-3.3-70b-versatile`
- **Purpose**: Main task processing and tool orchestration
- **Features**: Tool binding, conversation management

#### Evaluator Model (OpenAI)
- **Model**: `gpt-4o`
- **Purpose**: Success criteria evaluation
- **Features**: Structured output, feedback generation

## Error Handling

### Common Error Types

#### API Errors
- **Rate Limiting**: Automatic retry with exponential backoff
- **Authentication**: Clear error messages for missing/invalid keys
- **Network Issues**: Graceful degradation with user feedback

#### Tool Errors
- **Browser Errors**: Automatic cleanup and retry
- **File System Errors**: Permission handling and fallback options
- **Code Execution Errors**: Sandboxed execution with error reporting

### Error Recovery

#### Automatic Recovery
- **Session Reset**: Start fresh sessions when needed
- **Resource Cleanup**: Automatic cleanup of browser instances
- **Memory Management**: Clear memory when sessions become too large

#### Manual Recovery
- **New Session Button**: Users can start fresh sessions
- **Clear Resources**: Automatic cleanup on session end
- **Debug Mode**: Detailed error reporting for troubleshooting

## Performance Metrics

### Monitoring Points

#### Response Times
- **Assistant Processing**: Time to generate responses
- **Tool Execution**: Time for individual tool operations
- **Evaluation**: Time for success criteria assessment

#### Resource Usage
- **Memory Consumption**: Conversation history and state storage
- **Browser Resources**: Playwright instance management
- **API Usage**: Rate limiting and quota management

### Optimization Strategies

#### Caching
- **Tool Results**: Cache frequently accessed information
- **Conversation Context**: Efficient state management
- **Browser Sessions**: Reuse browser instances when possible

#### Async Operations
- **Parallel Tool Execution**: Execute independent tools simultaneously
- **Non-blocking UI**: Responsive interface during processing
- **Background Tasks**: Handle cleanup and maintenance in background

## Security Considerations

### API Key Security
- **Environment Variables**: No hardcoded credentials
- **Secure Storage**: Use .env files with proper permissions
- **Key Rotation**: Support for regular key updates

### Tool Security
- **Sandboxed Execution**: Python code runs in controlled environment
- **File System Limits**: Restricted access to specific directories
- **Browser Security**: Controlled automation with safety checks

### Data Privacy
- **Conversation Storage**: Local memory only, no external storage
- **Session Isolation**: Independent state for each session
- **Cleanup**: Automatic removal of sensitive data 