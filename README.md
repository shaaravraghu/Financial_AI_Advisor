# Financial AI Advisor

An intelligent financial advisor application powered by AI that helps users manage their finances through voice and text input. The system uses Google's Gemini AI for probabilistic reasoning and ElevenLabs for voice capabilities.

## 🎯 Features

- **Voice & Text Input**: Accept financial queries via voice (audio files) or text
- **Intelligent Data Filtering**: Automatically separates necessary financial data from conversational fluff
- **Transaction Tracking**: Maintains detailed CSV records of all financial transactions
- **Risk Analysis**: Calculates spending volatility and provides risk assessments
- **Probabilistic Reasoning**: Uses AI to generate Monte Carlo-style financial scenarios
- **Decision Logging**: Maintains an audit trail of all financial advice and recommendations
- **Bio-Data Management**: Tracks user profile, risk tolerance, and financial goals
- **Voice Output**: Provides spoken financial advice using text-to-speech

## 📁 Project Structure

```
/Financial_AI_Advisor
│
├── /data                    # Persistence Layer
│   ├── user_bio.json        # Profile, Risk Capacity, and evolving Interests
│   ├── transactions.csv     # Historical financial ledger
│   ├── market_context.txt   # Macro-economic state (2026 data)
│   ├── decision_log.txt     # Audit trail for every AI recommendation
│   ├── interaction_history.txt  # All user conversations
│   └── latest_advice.mp3    # Most recent voice advice
│
├── /engines                 # Logic Layer
│   ├── risk_engine.py       # Probabilistic analysis (Profile vs. Market)
│   ├── planning_engine.py   # Deterministic math & 5-year projections
│   └── filter_agent.py      # Sifts "Necessary" signal from fluff
│
├── main.py                  # Orchestrator: Coordinates engine workflows
├── memory_manager.py        # Data persistence and file management
├── utils.py                 # API Bridge: ElevenLabs TTS & Scribe handlers
├── .env                     # API keys (not committed to git)
└── README.md                # This file
```

## 🚀 Setup

### Prerequisites

- Python 3.8 or higher
- Google AI Studio API Key ([Get it here](https://aistudio.google.com/app/apikey))
- ElevenLabs API Key ([Get it here](https://elevenlabs.io))

### Installation

1. **Clone or download the project**
   ```bash
   cd Financial_AI_Advisor
   ```

2. **Install dependencies**
   ```bash
   pip install python-dotenv requests numpy elevenlabs
   ```

3. **Configure API keys**
   
   Create or update the `.env` file in the project root:
   ```bash
   ELEVENLABS_API_KEY="your_elevenlabs_api_key"
   GOOGLE_API_KEY="your_google_api_key"
   GOOGLE_MODEL="gemini-1.5-flash"
   ```

## 💻 Usage

### Running the Application

```bash
python3 main.py
```

### Example Interaction

```
AI Financier Active. Enter text or path to audio file.
You: I spent 500 rupees on dinner yesterday
User Input: I spent 500 rupees on dinner yesterday
Transaction recorded.

FINANCIER ADVICE: Based on your spending pattern...
```

### Input Options

- **Text Input**: Type your financial queries directly
- **Voice Input**: Provide path to an audio file for transcription
- **Exit**: Type `exit` or `quit` to close the application

## 🏗️ Architecture

### Core Components

1. **MemoryManager** (`memory_manager.py`)
   - Manages all data persistence
   - Handles CSV transactions, JSON bio-data, and text logs
   - Provides unified interface for data storage

2. **FilterAgent** (`engines/filter_agent.py`)
   - Uses Google Gemini AI to analyze user input
   - Extracts structured financial data (amount, type, category)
   - Identifies and filters conversational fluff
   - Detects bio-data updates (risk profile, interests)

3. **RiskEngine** (`engines/risk_engine.py`)
   - Calculates risk scores based on spending volatility
   - Performs probabilistic reasoning using AI
   - Generates Monte Carlo-style outcome scenarios
   - Provides 12-month financial projections

4. **APIBridge** (`utils.py`)
   - Handles ElevenLabs Scribe transcription
   - Manages text-to-speech conversion
   - Logs decisions to audit trail

5. **FinancierApp** (`main.py`)
   - Orchestrates the entire workflow
   - Coordinates between all components
   - Manages the conversation loop

### Data Flow

```
User Input (Text/Voice)
    ↓
[FilterAgent] → Extract structured data
    ↓
[MemoryManager] → Save transaction & update bio
    ↓
[RiskEngine] → Analyze risk & generate advice
    ↓
[APIBridge] → Log decision & speak advice
    ↓
Output (Text + Voice)
```

## 🔧 Configuration

### Available Models

You can change the Google AI model in `.env`:
- `gemini-1.5-flash` (default, fast and efficient)
- `gemini-1.5-pro` (more capable, slower)
- `gemini-pro` (legacy)

### Customization

- **Voice Settings**: Edit `voice_id` in `utils.py` (default: Rachel)
- **Temperature**: Adjust in `risk_engine.py` (default: 0.3 for financial accuracy)
- **Data Paths**: Modify in `memory_manager.py`

## 📊 Data Management

### Files Created

- `data/user_bio.json`: User profile and preferences
- `data/transactions.csv`: All financial transactions
- `data/decision_log.txt`: AI recommendations history
- `data/interaction_history.txt`: Complete conversation log
- `data/latest_advice.mp3`: Most recent audio advice

### CSV Format

Transactions are stored with:
- Timestamp
- Type (Income/Expense)
- Category
- Amount
- Description
- Is_Necessary (filtered by AI)

## 🛡️ Privacy & Security

- **API Keys**: Never commit `.env` to version control
- **Local Storage**: All data stored locally on your machine
- **No Cloud Sync**: Financial data never leaves your device (except API calls)

## 🐛 Troubleshooting

### Common Issues

1. **"python-dotenv not installed"**
   ```bash
   pip install python-dotenv
   ```

2. **"404 Model Not Found"**
   - Check that your `GOOGLE_MODEL` in `.env` is valid
   - Try using `gemini-1.5-flash`

3. **"Invalid API key"**
   - Verify your Google API key is correct
   - Ensure it has Gemini API access enabled

4. **Pydantic warnings**
   - These are harmless compatibility warnings with Python 3.14
   - They don't affect functionality

## 📝 Project Expectations

This project implements:
- ✅ Verbal and text input handling
- ✅ Historical data tracking (CSV + TXT)
- ✅ Transaction and planning CSV maintenance
- ✅ Decision logging system
- ✅ Bio-data management
- ✅ Risk profile and market trend analysis
- ✅ Data filtration (Necessary vs Unnecessary)
- ✅ Probabilistic reasoning engine
- ✅ Risk management calculations
- ✅ Future financial planning
- ✅ Decision explanations
- ✅ Voice transcription and synthesis

## 🤝 Contributing

This is a personal financial advisor tool. Customize it to your needs by:
- Adding new engines in `/engines`
- Extending the data model in `memory_manager.py`
- Customizing prompts in `filter_agent.py` and `risk_engine.py`

## 📄 License

Personal use project. Modify and adapt as needed.

## 🙏 Acknowledgments

- **Google Gemini**: AI reasoning engine
- **ElevenLabs**: Voice transcription and synthesis
- **Python Community**: Essential libraries

---

**Version**: 1.0  
**Last Updated**: January 2026










