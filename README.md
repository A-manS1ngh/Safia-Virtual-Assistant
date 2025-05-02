# Safia - Voice-Controlled Virtual Assistant

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)

Safia is a sophisticated, voice-controlled personal assistant built using Python. It delivers a natural, conversational experience while automating various tasks through voice commands - from system control and web browsing to email management and information retrieval.

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Voice Commands](#-voice-commands)
- [Customization](#-customization)
- [Troubleshooting](#-troubleshooting)
- [Future Roadmap](#-future-roadmap)

## 🔧 Features

### 🎤 Voice Interaction
* **Speech Recognition**: Advanced voice recognition using `SpeechRecognition`
* **Natural Speech Synthesis**: Human-like responses powered by `pyttsx3`
* **Context-Aware Conversations**: Remembers context for more natural interactions
* **Name Personalization**: Adapts to user's name for a personalized experience

### 🛠️ System Automation
* **Display Control**: Adjust screen brightness via `screen_brightness_control`
* **System Monitoring**: Check battery status and system resources using `psutil`
* **Power Management**: Execute system shutdown, restart, and sleep commands
* **Screen Capture**: Take screenshots on demand with `pyautogui`

### 🌐 Web & Information
* **Search Integration**: Seamless Google and Wikipedia search capabilities
* **Quick App Access**: Open websites and web applications (YouTube, WhatsApp, Gmail, etc.)
* **Weather Updates**: Real-time weather information for any location
* **News Headlines**: Latest news from various categories and sources
* **Computational Intelligence**: Calculations and knowledge queries via WolframAlpha

### 📧 Voice-to-Email System
* **Email Composition**: Create and send emails using voice commands through `smtplib`
* **Smart Email Parsing**: Convert spoken email addresses using regex (e.g., "john dot doe at gmail dot com" → `john.doe@gmail.com`)
* **Multiple Recipients**: Support for sending to multiple addresses in one command

### 🧠 Knowledge and Memory
* **User Preferences**: Remembers preferences (name, volume, favorite websites)
* **Command History**: Stores recent commands (up to 50) for reference
* **Learning Capability**: Learns new facts through conversation for future recall
* **Persistent Memory**: Saves knowledge across sessions

### ⏰ Utilities
* **Voice Reminders**: Set, manage, and receive time-based reminders
* **Definitions**: Access Wikipedia for definitions and summaries
* **Entertainment**: Play jokes, coin toss, rock-paper-scissors, and other mini-games
* **Calendar Integration**: Date and time management features

## 📁 Project Structure

```
safia/
├── main.py             # Core assistant logic and voice command processor
├── info.py             # User profile, knowledge base, and entertainment features
├── email_config.json   # Stores email credentials (you must create this)
├── reminders.txt       # Auto-generated storage for reminders
├── user_data/          # Auto-created folder for user preferences/history
│   ├── preferences.json  # User settings and preferences
│   ├── history.json      # Command history
│   └── knowledge.json    # Learned information
├── assets/             # Icons, sounds, and other media files
├── README.md           # Project documentation
└──  requirements.txt    # Dependencies list

```

## ⚙️ Requirements

- Python 3.7 or higher
- Working microphone
- Internet connection for web-based features
- Windows OS (primary support, partial compatibility with macOS/Linux)

## 🔐 Configuration

### Email Setup

Create a file named `email_config.json` in the root directory with the following structure:

```json
{
  "email": "your_email@gmail.com",
  "password": "your_app_password"
}
```

> **⚠️ Important**: If using Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password.

### API Keys (Optional)

For enhanced functionality, you may want to set up the following API keys:

1. **WolframAlpha API Key** - For advanced knowledge queries
   - Sign up at [Wolfram Alpha Developer Portal](https://developer.wolframalpha.com/)
   - Add the key to your environment variables or config file

2. **Weather API Key** - For detailed weather information
   - Register at [OpenWeatherMap](https://openweathermap.org/api)
   - Configure the key in your settings

## ▶️ Usage

1. **Start the assistant**
   ```bash
   python main.py
   ```

2. **Initial setup**
   - Safia will guide you through the initial setup
   - Set your name and preferences when prompted

3. **Wake word**
   - By default, Safia is always listening
   - You can configure a wake word like "Hey Safia" in the settings

## 🗣️ Voice Commands

Here are some example commands to get you started:

### System Control
- "What time is it?"
- "Set brightness to 70 percent"
- "How much battery do I have left?"
- "Take a screenshot"
- "Shut down the computer"

### Web & Search
- "Open YouTube"
- "Search for Python tutorials"
- "What's the weather in New York?"
- "Tell me the latest news"
- "Show me today's top headlines"

### Email & Communication
- "Send an email to John"
- "Check my unread emails"
- "Send a message saying I'll be late"

### Information
- "What is the capital of France?"
- "How tall is Mount Everest?"
- "Define artificial intelligence"
- "Who invented the telephone?"
- "Calculate 15 percent of 85 dollars"

### Utilities
- "Remind me to call mom in 10 minutes"
- "Set a timer for 5 minutes"
- "Tell me a joke"
- "Flip a coin"
- "Let's play rock paper scissors"

### System Learning
- "Remember that my favorite color is blue"
- "My birthday is January 15th"
- "Learn that I prefer dark mode"

## 🔧 Customization

Safia can be customized in several ways:

1. **Voice Settings**
   - Change the voice (gender, accent, speed)
   - Adjust volume levels
   - Modify response verbosity

2. **Custom Commands**
   - Add your own commands by editing `info.py`
   - Create shortcuts for frequently used actions

3. **Appearance** (if adding GUI)
   - Change themes and colors
   - Resize the assistant window

## ❓ Troubleshooting

### Common Issues

1. **Microphone not detected**
   - Check your system's audio settings
   - Ensure your microphone is not being used by another application
   - Try running with administrator privileges

2. **Speech recognition errors**
   - Speak clearly and at a moderate pace
   - Reduce background noise
   - Use the retry command if Safia misunderstands you

3. **Feature limitations**
   - Some features may require internet connectivity
   - API-dependent features need proper API keys configured

### Logs

Check the generated log files in the `logs/` directory for detailed error information and debugging.

## 🚀 Future Roadmap

- **GUI Interface**: Graphical user interface using `tkinter` or `PyQt`
- **Voice Authentication**: Recognize different users by their voice patterns
- **Multi-language Support**: Input and output in multiple languages
- **Smart Home Integration**: Control compatible IoT devices
- **Advanced NLP**: Improved natural language understanding using more sophisticated models
- **Mobile App Connection**: Companion mobile application
- **Cloud Sync**: Preferences and history synchronization across devices
