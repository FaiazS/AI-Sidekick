# AI Sidekick Project

An intelligent AI assistant that can autonomously complete complex tasks using multiple tools while ensuring it meets your specified success criteria through continuous self-evaluation.

## 🚀 Features

- **Multi-Tool Capability**: Browser automation, file management, web search, Wikipedia access, Python execution, and push notifications
- **Self-Evaluating**: Built-in evaluator that checks if tasks meet your success criteria
- **Iterative Improvement**: Learns from feedback and retries when criteria aren't met
- **Persistent Memory**: Maintains conversation context across sessions
- **User-Friendly Interface**: Clean Gradio web interface for easy interaction
- **Autonomous Operation**: Can work independently while asking for clarification when needed

## 📋 Prerequisites

- Python 3.8+
- Required API keys (see Configuration section)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-Sidekick-Project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers**
   ```bash
   playwright install
   ```

## ⚙️ Configuration

Create a `.env` file in the project root with the following API keys:

```env
# OpenAI API (for evaluator)
OPENAI_API_KEY=your_openai_api_key_here

# Google Serper API (for web search)
SERPER_API_KEY=your_serper_api_key_here

# Pushover (for notifications) - Optional
PUSHOVER_USER_KEY=your_pushover_user_key_here
PUSHOVER_USER_TOKEN=your_pushover_token_here
```

### API Keys Required:

- **OpenAI API Key**: Used by the evaluator to assess task completion
- **Google Serper API Key**: Enables web search functionality
- **Pushover Keys** (Optional): For sending push notifications to your phone

## 🚀 Usage

### Starting the Application

```bash
python app.py
```

The application will start a local web server (typically at `http://localhost:7860`).

### Using the AI Sidekick

1. **Input your request**: Describe the task you want the AI to complete
2. **Specify success criteria**: Define what constitutes successful completion
3. **Click "Begin task"**: The AI will start working autonomously
4. **Monitor progress**: Watch as the AI uses tools and evaluates its work
5. **Review results**: The AI will provide the final output when criteria are met

### Example Tasks

- **Web Automation**: "Book a flight ticket for next week from New York to London"
- **Data Analysis**: "Analyze this CSV file and create a summary report"
- **Research**: "Find information about quantum computing and summarize key points"
- **File Operations**: "Organize my photos by date and create a backup"
- **Code Tasks**: "Write a Python script to scrape this website"

## 🏗️ Architecture

### Core Components

#### 1. **AI Sidekick** (`ai_sidekick.py`)
The main orchestrator that manages the AI workflow:

- **State Management**: Tracks conversation, success criteria, and evaluation feedback
- **Graph Workflow**: Uses LangGraph to create a three-node workflow:
  - **Assistant Node**: Processes requests and uses tools
  - **Tools Node**: Executes various tools (browser, files, search, etc.)
  - **Evaluator Node**: Assesses if success criteria are met
- **Memory System**: Maintains conversation context across sessions

#### 2. **User Interface** (`user_interface.py`)
Gradio-based web interface providing:
- Chat interface for conversation
- Input fields for requests and success criteria
- Session management (start new session, clear resources)
- Real-time interaction with the AI

#### 3. **Tool Arsenal** (`tool_base.py`)
Comprehensive set of tools the AI can use:

- **Browser Automation** (Playwright): Navigate websites, interact with elements
- **File Management**: Create, read, write, organize files
- **Web Search** (Google Serper): Search the internet for information
- **Wikipedia Access**: Get information from Wikipedia
- **Python Execution**: Run Python code dynamically
- **Push Notifications**: Send notifications to your phone

### Workflow Process

1. **User Input**: User provides task description and success criteria
2. **Assistant Processing**: AI analyzes the request and determines needed tools
3. **Tool Execution**: AI uses appropriate tools to complete the task
4. **Evaluation**: Built-in evaluator checks if success criteria are met
5. **Feedback Loop**: If criteria not met, AI tries again with feedback
6. **Completion**: When criteria are met, task is complete

## 🔧 Technical Details

### Dependencies

- **LangGraph/LangChain**: AI workflow orchestration
- **Groq (llama-3.3-70b)**: Main AI model for task processing
- **OpenAI GPT-4**: Evaluation model for success criteria assessment
- **Playwright**: Browser automation
- **Gradio**: Web interface
- **Pydantic**: Data validation and structure

### State Management

The system uses a `State` TypedDict to track:
- **messages**: Conversation history
- **success_criteria**: User-defined completion criteria
- **given_feedback**: Previous evaluation feedback
- **met_success_criteria**: Whether criteria are currently met
- **required_user_input**: Whether user input is needed

### Memory System

Uses LangGraph's `MemorySaver` for:
- Persistent conversation context
- Session management
- State checkpointing

## 🛠️ Development

### Project Structure

```
AI Sidekick Project/
├── app.py                 # Main application entry point
├── ai_sidekick.py        # Core AI logic and workflow
├── user_interface.py     # Gradio web interface
├── tool_base.py          # Tool definitions and setup
├── requirements.txt      # Python dependencies
└── README.md            # This documentation
```

### Adding New Tools

To add a new tool, modify `tool_base.py`:

1. Import the required library
2. Create the tool function
3. Add it to the `tool_team()` function
4. Update the tool description for the AI

### Customizing the AI

To modify AI behavior, edit `ai_sidekick.py`:
- **System prompts**: Modify the assistant's behavior and instructions
- **Evaluation criteria**: Adjust how the evaluator assesses success
- **Workflow logic**: Change the graph structure and routing

## 🐛 Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure all required API keys are in your `.env` file
2. **Playwright Issues**: Run `playwright install` to install browser binaries
3. **Memory Issues**: The system automatically manages memory, but you can start new sessions
4. **Tool Failures**: Check internet connection and API rate limits

### Debug Mode

The application runs in debug mode by default. Check the console for detailed logs and error messages.

## 📝 License

[Add your license information here]

## 🤝 Contributing

[Add contribution guidelines here]

## 📞 Support

[Add support contact information here] 