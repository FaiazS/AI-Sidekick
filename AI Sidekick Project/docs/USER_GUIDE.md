# AI Sidekick User Guide

## Getting Started

### First Time Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

2. **Configure API Keys**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   SERPER_API_KEY=your_serper_api_key_here
   ```

3. **Start the Application**
   ```bash
   python app.py
   ```

4. **Access the Interface**
   Open your browser and go to `http://localhost:7860`

## Using the AI Sidekick

### Interface Overview

The AI Sidekick interface consists of:

- **Chat Area**: Shows conversation history and AI responses
- **Input Field**: Enter your task description
- **Success Criteria Field**: Define what constitutes successful completion
- **Begin Task Button**: Start the AI workflow
- **Start New Session Button**: Clear current session and start fresh

### Step-by-Step Usage

#### 1. Define Your Task
**Input Field**: Describe what you want the AI to accomplish

**Examples**:
- "Find the latest news about artificial intelligence and summarize the key points"
- "Create a Python script to analyze this CSV file and generate a report"
- "Book a flight from New York to London for next week"
- "Organize my photos by date and create a backup"

#### 2. Set Success Criteria
**Success Criteria Field**: Define what constitutes successful completion

**Good Examples**:
- "Provide a 3-5 sentence summary of the main AI news stories"
- "Generate a Python script that reads the CSV and outputs statistical analysis"
- "Successfully book a flight and provide booking confirmation details"
- "Create organized folders by date and save a backup to external drive"

**Poor Examples**:
- "Do it well" (too vague)
- "Complete the task" (not specific)
- "Make it good" (no clear criteria)

#### 3. Begin the Task
Click **"Begin Task"** to start the AI workflow.

The AI will:
1. Analyze your request
2. Determine required tools
3. Execute the task step by step
4. Evaluate its work against your criteria
5. Provide the final result or ask for clarification

### Understanding the Workflow

#### What Happens Behind the Scenes

1. **Assistant Processing**: The AI analyzes your request and determines what tools to use
2. **Tool Execution**: The AI uses various tools (browser, search, files, etc.) to complete the task
3. **Evaluation**: A separate AI evaluator checks if the work meets your success criteria
4. **Feedback Loop**: If criteria aren't met, the AI tries again with feedback
5. **Completion**: When criteria are met, the task is complete

#### Reading the Conversation

The chat area shows:
- **User Messages**: Your input and success criteria
- **Assistant Responses**: AI's work and explanations
- **Tool Usage**: When the AI uses tools (browser, search, etc.)
- **Evaluator Feedback**: Assessment of whether criteria are met

### Best Practices

#### Writing Effective Tasks

**Be Specific**:
- ✅ "Find the top 5 AI companies by market cap and list their key products"
- ❌ "Research AI companies"

**Include Context**:
- ✅ "Analyze this sales data CSV file and identify trends in Q4 2023"
- ❌ "Analyze the data"

**Set Clear Boundaries**:
- ✅ "Search for Python tutorials and create a list of the 10 best ones for beginners"
- ❌ "Find Python tutorials"

#### Setting Good Success Criteria

**Make it Measurable**:
- ✅ "Provide a list of exactly 5 items with brief descriptions"
- ❌ "Give me some information"

**Include Quality Standards**:
- ✅ "Summarize in 3-5 sentences with key statistics and recent developments"
- ❌ "Summarize the information"

**Consider Completeness**:
- ✅ "Ensure all data is processed, errors are handled, and results are saved to a file"
- ❌ "Process the data"

### Example Use Cases

#### Web Research and Analysis
**Task**: "Research the latest developments in quantum computing and summarize the key breakthroughs"

**Success Criteria**: "Provide a comprehensive summary covering at least 3 recent breakthroughs, including technical details, company involvement, and potential applications. Include specific dates and sources."

#### File Management
**Task**: "Organize my photos by date and create a backup"

**Success Criteria**: "Create folders organized by year/month, move all photos to appropriate folders, and create a complete backup copy in a separate location. Verify all files are properly organized and backed up."

#### Data Analysis
**Task**: "Analyze this sales data and identify trends"

**Success Criteria**: "Process the CSV file, calculate monthly sales trends, identify top-performing products, create visualizations, and provide actionable insights in a clear report format."

#### Web Automation
**Task**: "Book a flight from New York to London for next week"

**Success Criteria**: "Find available flights, compare prices across multiple airlines, select the best option considering price and timing, complete the booking process, and provide confirmation details including flight number, departure time, and booking reference."

### Troubleshooting

#### Common Issues

**AI Gets Stuck**
- **Solution**: Click "Start New Session" to reset
- **Prevention**: Be more specific in your task description

**Tool Errors**
- **Solution**: Check your internet connection and API keys
- **Prevention**: Ensure all required API keys are configured

**Unclear Results**
- **Solution**: Refine your success criteria to be more specific
- **Prevention**: Use measurable, specific criteria

**Browser Issues**
- **Solution**: The system will automatically retry or ask for clarification
- **Prevention**: Ensure the target website is accessible

#### Getting Better Results

**If the AI asks for clarification**:
- Provide the requested information
- Be as specific as possible
- Include any relevant context

**If the AI seems confused**:
- Rephrase your request more clearly
- Break complex tasks into smaller parts
- Provide more context or examples

**If results don't meet your expectations**:
- Review and refine your success criteria
- Try starting a new session
- Provide more specific instructions

### Advanced Features

#### Session Management
- **Start New Session**: Clears current conversation and starts fresh
- **Automatic Cleanup**: Resources are automatically cleaned up when sessions end
- **Memory Persistence**: Conversation context is maintained within a session

#### Tool Capabilities
The AI can use:
- **Web Browsing**: Navigate websites, fill forms, click buttons
- **File Operations**: Create, read, write, organize files
- **Web Search**: Search the internet for information
- **Code Execution**: Run Python code for data processing
- **Information Retrieval**: Access Wikipedia and other sources
- **Notifications**: Send push notifications to your phone

#### Customization
- **Tool Selection**: The AI automatically chooses appropriate tools
- **Workflow Control**: The system handles complex multi-step processes
- **Error Recovery**: Automatic retry and error handling

### Tips for Success

#### Planning Your Tasks
1. **Break Down Complex Tasks**: Large tasks work better when broken into smaller parts
2. **Provide Context**: Include relevant background information
3. **Set Realistic Expectations**: Consider the complexity of your request

#### Writing Clear Instructions
1. **Be Specific**: Avoid vague language
2. **Include Examples**: Provide examples when possible
3. **Set Boundaries**: Define what's in and out of scope

#### Monitoring Progress
1. **Watch the Conversation**: Monitor how the AI is working
2. **Provide Feedback**: If the AI asks questions, answer them
3. **Be Patient**: Complex tasks may take multiple steps

### Safety and Security

#### Data Privacy
- **Local Processing**: Conversations are stored locally only
- **Session Isolation**: Each session is independent
- **Automatic Cleanup**: Sensitive data is automatically removed

#### Tool Safety
- **Sandboxed Execution**: Code runs in controlled environments
- **Limited Access**: File operations are restricted to safe directories
- **Browser Security**: Web automation includes safety checks

#### Best Practices
- **Don't Share Sensitive Data**: Avoid sharing passwords or personal information
- **Review Results**: Always review AI-generated content before using
- **Use Responsibly**: The AI is a tool, not a replacement for human judgment

### Getting Help

#### When to Start a New Session
- The AI seems confused or stuck
- You want to try a completely different task
- The conversation has become too long or complex
- You want to test different approaches

#### When to Refine Your Request
- The AI keeps asking for clarification
- Results don't match your expectations
- The AI seems to misunderstand your intent
- You want to try a different approach

#### Debugging Issues
- Check the console for error messages
- Verify your API keys are correct
- Ensure your internet connection is stable
- Try simpler tasks to test the system

### Future Enhancements

The AI Sidekick system is designed to be extensible. Future versions may include:
- Additional tools and capabilities
- Improved evaluation algorithms
- Enhanced user interface features
- Integration with more external services
- Advanced customization options 