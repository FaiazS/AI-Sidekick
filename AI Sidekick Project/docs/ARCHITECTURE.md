# AI Sidekick Architecture Documentation

## Overview

The AI Sidekick is built using a **LangGraph-based workflow architecture** that orchestrates multiple AI agents and tools to complete complex tasks autonomously. The system uses a three-node graph structure with built-in evaluation and feedback loops.

## System Architecture

### Core Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │───▶│   Assistant     │───▶│     Tools       │
│   & Criteria    │    │     Node        │    │     Node        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       │
                       ┌─────────────────┐              │
                       │   Evaluator     │◀─────────────┘
                       │     Node        │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  End/Continue   │
                       └─────────────────┘
```

### 1. Assistant Node

**Purpose**: Main AI agent that processes user requests and orchestrates tool usage.

**Key Functions**:
- Analyzes user input and determines required tools
- Manages conversation flow and context
- Handles tool selection and execution
- Provides responses to users

**Implementation**: Uses Groq's llama-3.3-70b model with tool binding

**System Prompt Structure**:
```python
system_prompt = f"""
You are an exceptional assistant who leverages tools to complete tasks effectively and efficiently.

You seamlessly work on a given task until you have additional questions or clarifications for the user or when the success criteria is met.

This is the success criteria: {state['success_criteria']}.

Your task is to respond either a question regarding additional user input if and only required by clearly elaborating what is needed for current assignment being performed or with the final response post completion of the assignment at hand.
"""
```

### 2. Tools Node

**Purpose**: Executes various tools based on assistant requests.

**Available Tools**:
- **Browser Automation** (Playwright): Web navigation, form filling, clicking
- **File Management**: File operations, organization, backup
- **Web Search** (Google Serper): Internet search capabilities
- **Wikipedia Access**: Information retrieval from Wikipedia
- **Python Execution**: Dynamic code execution
- **Push Notifications**: Mobile notifications

**Tool Integration**:
```python
async def tool_team():
    push_notification_tool = Tool(
        name='Push Notification Tool',
        func=send_push_notifications,
        description='A tool for sending push notifications'
    )
    
    file_management_tool = file_tools()
    wikipedia_tool = WikipediaAPIWrapper()
    wikipedia_search_tool = WikipediaQueryRun(api_wrapper=wikipedia_tool)
    python_coding_tool = PythonREPLTool()
    
    return file_management_tool + [push_notification_tool, wikipedia_tool, wikipedia_search_tool, python_coding_tool]
```

### 3. Evaluator Node

**Purpose**: Assesses whether the assistant's work meets the user's success criteria.

**Evaluation Process**:
1. Analyzes the assistant's response
2. Compares against user-defined success criteria
3. Determines if criteria are met
4. Provides feedback for improvement if needed

**Implementation**: Uses OpenAI GPT-4 with structured output

**Evaluation Criteria**:
```python
class EvaluatorFeedback(BaseModel):
    feedback: str = Field(description="Feedback on the assistant's performance")
    met_success_criteria: bool = Field(description="Whether the success criteria has been met or not")
    required_user_input: bool = Field(description="True if more user input is required, or clarifications, or assistant is stuck")
```

## State Management

### State Structure

```python
class State(TypedDict):
    messages: Annotated[List[Any], add_messages]  # Conversation history
    success_criteria: str                          # User-defined criteria
    given_feedback: Optional[str]                  # Previous evaluation feedback
    met_success_criteria: bool                     # Current success status
    required_user_input: bool                      # Whether user input is needed
```

### State Flow

1. **Initial State**: User input + success criteria
2. **Assistant Processing**: Messages updated with AI response
3. **Tool Execution**: Tool results added to messages
4. **Evaluation**: Evaluator feedback stored in state
5. **Decision Point**: Continue or end based on evaluation

## Workflow Graph

### Graph Construction

```python
async def build_graph(self):
    graph_builder = StateGraph(State)
    
    # Add nodes
    graph_builder.add_node('Assistant', self.ai_assistant)
    graph_builder.add_node('tools', ToolNode(tools=self.tools))
    graph_builder.add_node('Evaluator', self.ai_evaluator)
    
    # Add edges
    graph_builder.add_conditional_edges('Assistant', self.route_ai_assistant, 
                                      {'tools':'tools', 'Evaluator':'Evaluator'})
    graph_builder.add_edge('tools', 'Assistant')
    graph_builder.add_conditional_edges('Evaluator', self.route_ai_evaluator, 
                                      {'Assistant':'Assistant', 'END': END})
    graph_builder.add_edge(START, 'Assistant')
    
    self.graph = graph_builder.compile(checkpointer=self.memory)
```

### Routing Logic

**Assistant → Tools/Evaluator**:
```python
def route_ai_assistant(self, state: State) -> str:
    recent_message = state['messages'][-1]
    if hasattr(recent_message, 'tool_calls') and recent_message.tool_calls:
        return 'tools'
    else:
        return 'Evaluator'
```

**Evaluator → Assistant/End**:
```python
def route_ai_evaluator(self, state: State) -> str:
    if state['met_success_criteria'] or state['required_user_input']:
        return 'END'
    else:
        return 'Assistant'
```

## Memory System

### Memory Components

- **Conversation History**: Maintains all messages and tool interactions
- **Session Management**: Unique session IDs for each conversation
- **State Checkpointing**: Automatic state persistence across graph executions

### Memory Implementation

```python
self.memory = MemorySaver()
self.sidekick_id = str(uuid.uuid4())

config = {'configurable': {'thread_id': self.sidekick_id}}
```

## Error Handling and Recovery

### Error Scenarios

1. **Tool Failures**: Individual tool errors don't crash the system
2. **API Rate Limits**: Graceful handling of API limitations
3. **Network Issues**: Retry mechanisms for network-dependent tools
4. **Memory Issues**: Automatic cleanup and session management

### Recovery Mechanisms

- **Feedback Loop**: Evaluator provides guidance for failed attempts
- **Session Reset**: Ability to start fresh sessions
- **Resource Cleanup**: Automatic cleanup of browser instances and resources

## Performance Considerations

### Optimization Strategies

1. **Async Operations**: All I/O operations are asynchronous
2. **Tool Caching**: Frequently used tools are cached
3. **Memory Management**: Automatic cleanup of unused resources
4. **Parallel Execution**: Tools can execute in parallel when possible

### Scalability

- **Modular Design**: Easy to add new tools and capabilities
- **State Isolation**: Each session maintains independent state
- **Resource Pooling**: Efficient resource management across sessions

## Security Considerations

### API Key Management

- Environment variable-based configuration
- No hardcoded credentials
- Secure key rotation support

### Tool Security

- Sandboxed Python execution
- Limited file system access
- Controlled browser automation

## Monitoring and Logging

### Debug Information

- Detailed conversation logs
- Tool execution tracking
- Performance metrics
- Error reporting

### User Interface Feedback

- Real-time progress updates
- Clear success/failure indicators
- Detailed error messages
- Session management controls 