# AI Sidekick Development Guide

## Overview

This guide provides comprehensive information for developers who want to extend, modify, or contribute to the AI Sidekick project. It covers the codebase structure, development setup, and best practices for adding new features.

## Development Environment Setup

### Prerequisites

- Python 3.8+
- Git
- Virtual environment (recommended)
- API keys for testing

### Initial Setup

1. **Clone and Setup Environment**
   ```bash
   git clone <repository-url>
   cd AI-Sidekick-Project
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   playwright install
   ```

2. **Configure Development Environment**
   ```bash
   # Create .env file for development
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Install Development Dependencies**
   ```bash
   pip install pytest black flake8 mypy
   ```

## Project Structure

```
AI Sidekick Project/
├── app.py                 # Main application entry point
├── ai_sidekick.py        # Core AI logic and workflow
├── user_interface.py     # Gradio web interface
├── tool_base.py          # Tool definitions and setup
├── requirements.txt      # Python dependencies
├── docs/                # Documentation
│   ├── ARCHITECTURE.md
│   ├── API_REFERENCE.md
│   ├── USER_GUIDE.md
│   └── DEVELOPMENT_GUIDE.md
├── tests/               # Test files
├── examples/            # Example usage
└── README.md           # Main documentation
```

## Core Components Deep Dive

### 1. AI Sidekick Core (`ai_sidekick.py`)

#### Class Structure
```python
class AI_Sidekick:
    def __init__(self):
        # Initialize components
        self.assistant = None
        self.evaluator = None
        self.tools = None
        self.graph = None
        self.sidekick_id = str(uuid.uuid4())
        self.memory = MemorySaver()
        self.browser = None
        self.playwright = None
```

#### Key Methods to Understand

**`async ai_sidekick_setup()`**
- Initializes all components
- Sets up AI models
- Builds the workflow graph
- Prepares tools

**`ai_assistant(state: State) -> Dict[str, Any]`**
- Main processing function
- Handles user requests
- Manages tool selection
- Generates responses

**`ai_evaluator(state: State) -> Dict[str, Any]`**
- Evaluates task completion
- Provides structured feedback
- Determines next steps

**`async build_graph()`**
- Constructs LangGraph workflow
- Defines nodes and edges
- Sets up routing logic

### 2. Tool System (`tool_base.py`)

#### Adding New Tools

**Step 1: Create Tool Function**
```python
def my_custom_tool(input_data: str) -> str:
    """
    Custom tool description.
    
    Args:
        input_data: Description of input
        
    Returns:
        Description of output
    """
    # Tool implementation
    result = process_input(input_data)
    return result
```

**Step 2: Add to Tool Team**
```python
async def tool_team():
    # Existing tools...
    
    # Add your new tool
    custom_tool = Tool(
        name='Custom Tool Name',
        func=my_custom_tool,
        description='Detailed description of what this tool does and when to use it'
    )
    
    return existing_tools + [custom_tool]
```

**Step 3: Update Dependencies**
Add any new dependencies to `requirements.txt`:
```
# New tool dependencies
new_library==1.0.0
```

#### Tool Categories

**Browser Tools** (Playwright)
```python
async def playwright_tools():
    launch_playwright = await async_playwright().start()
    launch_playwright_browser = await launch_playwright.chromium.launch(headless=False)
    playwright_toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=launch_playwright_browser)
    return launch_playwright, launch_playwright_browser, playwright_toolkit.get_tools()
```

**File Management Tools**
```python
def file_tools():
    file_toolkit = FileManagementToolkit(root_dir='sandbox')
    return file_toolkit.get_tools()
```

**Information Retrieval Tools**
```python
# Wikipedia tools
wikipedia_tool = WikipediaAPIWrapper()
wikipedia_search_tool = WikipediaQueryRun(api_wrapper=wikipedia_tool)

# Web search tools
web_search_tool = GoogleSerperAPIWrapper()
```

### 3. User Interface (`user_interface.py`)

#### Gradio Interface Structure

**Main Interface**
```python
with gr.Blocks(theme=gr.themes.Default(primary_hue='emerald')) as ai_sidekick_user_interface:
    gr.Markdown("AI Sidekick")
    sidekick = gr.State(delete_callback=clear_resources)
    
    with gr.Row():
        ai_sidekick_bot = gr.Chatbot(label='AI Sidekick', height=300, type='messages')
        with gr.Group():
            # Input components
```

**Event Handlers**
```python
# Load event
ai_sidekick_user_interface.load(sidekick_agent_setup, [], [sidekick])

# Submit events
input.submit(process_user_and_agent_interactions, 
            [sidekick, input, success_criteria, ai_sidekick_bot], 
            [ai_sidekick_bot, sidekick])

# Button clicks
begin_task_button.click(process_user_and_agent_interactions, 
                      [sidekick, input, success_criteria, ai_sidekick_bot], 
                      [ai_sidekick_bot, sidekick])
```

## Extending the System

### Adding New AI Models

**1. Create Model Wrapper**
```python
class CustomModelWrapper:
    def __init__(self, model_name: str):
        self.model = self._initialize_model(model_name)
    
    def _initialize_model(self, model_name: str):
        # Initialize your custom model
        pass
    
    def invoke(self, messages):
        # Process messages with your model
        pass
```

**2. Integrate with AI Sidekick**
```python
# In ai_sidekick.py
def __init__(self):
    # ... existing code ...
    self.custom_model = CustomModelWrapper("your-model-name")

def ai_assistant(self, state: State) -> Dict[str, Any]:
    # Use custom model instead of Groq
    assistant_response = self.custom_model.invoke(messages)
    return {'messages': [assistant_response]}
```

### Adding New Evaluation Methods

**1. Create Custom Evaluator**
```python
class CustomEvaluator(BaseModel):
    custom_metric: float = Field(description="Custom evaluation metric")
    confidence_score: float = Field(description="Confidence in evaluation")
    recommendations: List[str] = Field(description="List of recommendations")

def custom_evaluator(state: State) -> Dict[str, Any]:
    # Custom evaluation logic
    evaluation = CustomEvaluator(
        custom_metric=calculate_metric(state),
        confidence_score=calculate_confidence(state),
        recommendations=generate_recommendations(state)
    )
    return {
        'custom_evaluation': evaluation,
        'met_success_criteria': evaluation.custom_metric > threshold
    }
```

**2. Integrate with Graph**
```python
# In build_graph method
graph_builder.add_node('CustomEvaluator', custom_evaluator)
graph_builder.add_conditional_edges('CustomEvaluator', custom_routing_logic)
```

### Adding New Workflow Nodes

**1. Define Node Function**
```python
def custom_node(state: State) -> Dict[str, Any]:
    """
    Custom workflow node.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state
    """
    # Node logic here
    processed_data = process_state_data(state)
    
    return {
        'messages': state['messages'] + [processed_data],
        'custom_data': processed_data
    }
```

**2. Add to Graph**
```python
# In build_graph method
graph_builder.add_node('CustomNode', custom_node)
graph_builder.add_edge('Assistant', 'CustomNode')
graph_builder.add_edge('CustomNode', 'Evaluator')
```

### Adding New State Fields

**1. Update State Definition**
```python
class State(TypedDict):
    messages: Annotated[List[Any], add_messages]
    success_criteria: str
    given_feedback: Optional[str]
    met_success_criteria: bool
    required_user_input: bool
    # Add new fields
    custom_field: Optional[str]
    custom_metadata: Dict[str, Any]
```

**2. Update State Initialization**
```python
# In execute_graph_superstep
initial_state = {
    'messages': user_input,
    'success_criteria': success_criteria,
    'given_feedback': None,
    'met_success_criteria': False,
    'required_user_input': False,
    # Initialize new fields
    'custom_field': None,
    'custom_metadata': {}
}
```

## Testing

### Test Structure

```
tests/
├── __init__.py
├── test_ai_sidekick.py
├── test_tools.py
├── test_interface.py
└── conftest.py
```

### Writing Tests

**Unit Tests**
```python
import pytest
from ai_sidekick import AI_Sidekick

class TestAISidekick:
    @pytest.fixture
    async def sidekick(self):
        sidekick = AI_Sidekick()
        await sidekick.ai_sidekick_setup()
        yield sidekick
        sidekick.cleanup()
    
    def test_initialization(self, sidekick):
        assert sidekick.assistant is not None
        assert sidekick.evaluator is not None
        assert sidekick.tools is not None
    
    def test_state_management(self, sidekick):
        state = {
            'messages': [],
            'success_criteria': 'Test criteria',
            'given_feedback': None,
            'met_success_criteria': False,
            'required_user_input': False
        }
        # Test state processing
```

**Integration Tests**
```python
class TestWorkflow:
    async def test_complete_workflow(self):
        sidekick = AI_Sidekick()
        await sidekick.ai_sidekick_setup()
        
        result = await sidekick.execute_graph_superstep(
            "Test task",
            "Test criteria",
            []
        )
        
        assert len(result) > 0
        sidekick.cleanup()
```

**Tool Tests**
```python
class TestTools:
    def test_file_tools(self):
        tools = file_tools()
        assert len(tools) > 0
        
    def test_browser_tools(self):
        # Test browser tool initialization
        pass
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_ai_sidekick.py

# Run with coverage
pytest --cov=ai_sidekick

# Run async tests
pytest tests/ -v
```

## Code Quality

### Style Guidelines

**Python Style**
- Follow PEP 8
- Use type hints
- Write docstrings for all functions
- Keep functions focused and small

**Example**
```python
def process_user_input(user_input: str, context: Dict[str, Any]) -> ProcessedInput:
    """
    Process and validate user input.
    
    Args:
        user_input: Raw user input string
        context: Additional context information
        
    Returns:
        ProcessedInput: Validated and processed input
        
    Raises:
        ValueError: If input is invalid
    """
    if not user_input.strip():
        raise ValueError("User input cannot be empty")
    
    processed = ProcessedInput(
        original=user_input,
        cleaned=user_input.strip(),
        context=context
    )
    
    return processed
```

### Linting and Formatting

**Setup Tools**
```bash
# Install development tools
pip install black flake8 mypy

# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

**Configuration Files**

`.flake8`:
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .git,__pycache__,venv
```

`pyproject.toml`:
```toml
[tool.black]
line-length = 88
target-version = ['py38']

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

## Performance Optimization

### Async Best Practices

**Use Async Properly**
```python
# Good
async def process_data():
    result = await expensive_operation()
    return result

# Avoid
async def process_data():
    result = expensive_operation()  # Blocking!
    return result
```

**Parallel Execution**
```python
async def parallel_processing():
    tasks = [
        process_item(item1),
        process_item(item2),
        process_item(item3)
    ]
    results = await asyncio.gather(*tasks)
    return results
```

### Memory Management

**Resource Cleanup**
```python
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
```

**State Management**
```python
# Clear old state periodically
def clear_old_state(self):
    if len(self.memory.checkpoints) > MAX_CHECKPOINTS:
        # Clear oldest checkpoints
        pass
```

## Deployment

### Production Setup

**Environment Configuration**
```bash
# Production environment variables
export OPENAI_API_KEY="your-production-key"
export SERPER_API_KEY="your-production-key"
export ENVIRONMENT="production"
export DEBUG="false"
```

**Docker Setup**
```dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN playwright install

EXPOSE 7860

CMD ["python", "app.py"]
```

**Docker Compose**
```yaml
version: '3.8'
services:
  ai-sidekick:
    build: .
    ports:
      - "7860:7860"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - SERPER_API_KEY=${SERPER_API_KEY}
    volumes:
      - ./data:/app/data
```

### Monitoring

**Logging Setup**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Use in code
logger.info("Processing user request")
logger.error("Tool execution failed", exc_info=True)
```

**Health Checks**
```python
def health_check():
    """Check system health."""
    checks = {
        'api_keys': check_api_keys(),
        'tools': check_tools_availability(),
        'memory': check_memory_usage(),
        'browser': check_browser_status()
    }
    return all(checks.values()), checks
```

## Contributing

### Development Workflow

1. **Fork the Repository**
2. **Create Feature Branch**
   ```bash
   git checkout -b feature/new-tool
   ```
3. **Make Changes**
4. **Write Tests**
5. **Run Tests**
   ```bash
   pytest
   black .
   flake8 .
   ```
6. **Submit Pull Request**

### Pull Request Guidelines

**Before Submitting**
- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes (or documented)

**PR Template**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
```

### Code Review Process

**Review Checklist**
- [ ] Code is readable and well-documented
- [ ] Tests are comprehensive
- [ ] Performance considerations addressed
- [ ] Security implications considered
- [ ] Error handling is appropriate

## Troubleshooting Development Issues

### Common Problems

**Import Errors**
```bash
# Solution: Install in development mode
pip install -e .
```

**Async Issues**
```python
# Problem: RuntimeError: no running event loop
# Solution: Use asyncio.run() or ensure event loop exists
```

**Tool Integration Issues**
```python
# Problem: Tool not found
# Solution: Check tool registration in tool_team()
```

**Memory Issues**
```python
# Problem: Memory leaks
# Solution: Implement proper cleanup in __del__ or context managers
```

### Debug Tools

**Debug Mode**
```python
# Enable debug logging
logging.getLogger().setLevel(logging.DEBUG)
```

**State Inspection**
```python
def debug_state(state: State):
    """Print current state for debugging."""
    print(f"Messages: {len(state['messages'])}")
    print(f"Success Criteria: {state['success_criteria']}")
    print(f"Met Criteria: {state['met_success_criteria']}")
```

**Tool Testing**
```python
async def test_tool_directly():
    """Test a tool directly without the full workflow."""
    tool = your_tool_function
    result = await tool("test input")
    print(f"Tool result: {result}")
```

## Future Development

### Planned Features

- **Plugin System**: Allow third-party tool plugins
- **Advanced Analytics**: Detailed performance metrics
- **Multi-Model Support**: Support for multiple AI models
- **Enhanced UI**: More interactive interface options
- **API Endpoints**: REST API for programmatic access

### Architecture Evolution

- **Microservices**: Split into separate services
- **Database Integration**: Persistent storage options
- **Distributed Processing**: Handle multiple concurrent users
- **Cloud Deployment**: Easy cloud deployment options

### Contributing to Future Features

1. **Discuss on Issues**: Open issues for feature requests
2. **Design Reviews**: Participate in design discussions
3. **Prototype Development**: Create proof-of-concepts
4. **Documentation**: Help maintain and improve docs 