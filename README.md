# ARI Voice Assistant

ARI is a voice-only, console-based AI assistant capable of natural, open-ended conversation using various LLMs (Ollama/phi3) and fallback mechanisms.

## Features

- Voice-driven interaction via Microsoft's Edge TTS
- Learning from voice input - ARI can be taught new facts by voice
- Uses local LLMs (Ollama/phi3) for primary responses
- Multiple fallbacks (ChatterBot, basic chatbot) to ensure ARI always has a response
- Knowledge expansion using LLMs for unknown topics
- Fully integrated system with memory, reasoning, and Wikipedia integration

## Prerequisites

- Python 3.9+ with required packages (see below)
- Ollama with phi3 model (for LLM capabilities)
- A working microphone for voice input

## Installation

1. Ensure you have all required packages:
   ```
   pip install speech_recognition edge-tts wikipedia pygame chatterbot vaderSentiment rapidfuzz requests
   ```

2. Install Ollama following instructions at [ollama.ai](https://ollama.ai/)

3. Pull the phi3 model:
   ```
   ollama pull phi3
   ```

## Running ARI

### Option 1: Run from VS Code

1. Open this project in VS Code
2. Press `Ctrl+Shift+P` and select "Tasks: Run Task"
3. Select "Run ARI Assistant" 

OR

1. Press `Ctrl+Shift+B` to run the default build task which is set to run ARI

### Option 2: Run from Command Line

Open a terminal/command prompt in the project directory and run:

```
python ari_master_brain_final.py
```

## Using ARI

1. Wait for ARI's greeting
2. You'll hear a subtle sound when ARI is ready for input
3. Speak clearly into your microphone
4. ARI will play a quick sound to indicate it heard you and is processing
5. ARI will respond to your questions and statements
6. If ARI doesn't know something, it will:
   - Try to find information using the local LLM (Ollama/phi3)
   - Save what it learns for future reference
   - Share the information it found with you

### Expected User Experience

When using ARI, the experience should flow like this:

1. **Ready Signal**: A subtle audio cue indicates ARI is ready
2. **User Speaks**: You ask a question or give a command
3. **Processing Signal**: A brief sound confirms ARI heard you
4. **Response**: ARI responds verbally with the answer

The whole process should take only a few seconds in most cases. If you don't hear the processing signal after speaking, ARI might not have heard you clearly - try again when you hear the ready signal.

## Voice-Driven Learning

One of ARI's key features is the ability to learn through natural conversation:

- When you ask something ARI doesn't know, it first tries to generate an answer using the LLM
- ARI saves all learned information for future interactions
- For best results, validate any information ARI generates - if it's incorrect, say "that's not right" and ARI will try again

## Commands

- "Goodbye", "bye", "exit", "quit" - End the conversation
- "Stop", "stop talking", "be quiet" - Interrupt ARI when it's speaking

## Troubleshooting

### Audio and Greeting Issues

If ARI starts but doesn't speak or the greeting stops midway:

#### Run the Audio Diagnostic Tool

1. In VS Code, open the Command Palette (`Ctrl+Shift+P`)
2. Type "Tasks: Run Task"
3. Select "Run ARI Audio Diagnostic Tool"
4. Follow the on-screen instructions

#### Generate a Pre-recorded Greeting

1. In VS Code, open the Command Palette (`Ctrl+Shift+P`)
2. Type "Tasks: Run Task"
3. Select "Generate ARI Greeting Audio"
4. This will create a `_sonia_greeting.mp3` file that ARI can use as a fallback

#### Quick Audio Test

1. In VS Code, open the Command Palette (`Ctrl+Shift+P`)
2. Type "Tasks: Run Task"
3. Select "Test ARI Audio System"

#### Common Solutions for Audio Problems

1. **Check your audio connections and volume settings**
   - Make sure your speakers/headphones are connected and not muted
   - Adjust the volume to an audible level

2. **Restart your computer**
   - This can free up audio resources that might be locked by other applications

3. **Update packages**
   ```
   pip install --upgrade pygame edge-tts numpy
   ```

4. **Check for audio conflicts**
   - Close other applications that might be using audio resources
   - Check for background processes using the audio device

5. **Run as administrator**
   - Try running ARI with administrator privileges

### Speech Recognition Issues
- Speak clearly and at a moderate pace
- Reduce background noise in your environment
- Position your microphone properly (5-8 inches from your mouth)
- If ARI consistently misunderstands you, try using shorter phrases
- Ensure your microphone is set as the default recording device

### Ollama/LLM Issues
- Verify Ollama is running with `ollama list` in a terminal
- Make sure the phi3 model is installed with `ollama pull phi3`
- Check that port 11434 is open and accessible
- For slow responses, try restarting Ollama service
- If Ollama is unavailable, ARI will automatically fall back to other methods

### General Problems
- Check the `ari_error.log` file for detailed error information
- If ARI fails to start, ensure all required packages are installed
- For "Module not found" errors, run the pip install command again
- Try restarting your computer if multiple issues persist

## Files

### Core Components
- `ari_master_brain_final.py` - Main program file containing the central logic
- `learning_module.py` - Knowledge retrieval and learning capabilities
- `ari_speak.py` - Text-to-speech functionality
- `ari_listen.py` - Speech recognition functionality

### Knowledge Storage
- `learned_facts.json` - Simple key-value storage for learned facts
- `learned_facts_expanded.json` - Enhanced storage with paraphrases and structured data
- `knowledge.json` / `knowledge_expanded.json` - Base knowledge files

### Fallback Systems
- `chatbot_basic.py` - Simple pattern-matching chatbot as final fallback
- `memory_manager.py` - Short-term memory for conversation context
- `rules_engine.py` / `simple_reasoning.py` - Reasoning capabilities

### Utility Files
- `utils.py` - General utility functions
- `paraphrase_helper.py` - Generates variations of questions for better matching
- `edge_tts_sonia.py` - Edge TTS integration

## Environment Setup

For best results, ensure your environment meets these specifications:
- Python 3.9+ (3.10 or 3.11 recommended for best performance)
- At least 8GB RAM for smooth LLM operation
- A quality microphone (headset microphones often work best)
- A quiet environment for optimal speech recognition

## Development

If you want to extend ARI's capabilities:

1. The main response logic is in `get_response()` method in `ari_master_brain_final.py`
2. To add new knowledge sources, modify the fallback chain in that method
3. To change voices, modify the `voice` variable (default is "en-GB-SoniaNeural")
4. Custom commands can be added to the expression_commands dictionary

## Updates and Improvements

### Latest Updates (July 2025)
- Optimized for fast response times with audio feedback during processing
- Added subtle audio cues to indicate when ARI is ready for input
- Enhanced speech recognition with better confidence thresholds and noise filtering
- Improved error handling throughout the conversation loop
- Added automatic Ollama availability detection
- Optimized response generation with more contextual prompts
- Implemented nested fallback system with multiple LLM attempts
- Added better feedback during startup and operation
- Reduced TTS processing time with smart text truncation for long responses

### Performance Optimizations
- Immediate audio feedback when processing speech (users know ARI heard them)
- Faster LLM responses with optimized parameter settings
- Shorter ambient noise calibration (0.5s vs 1.5s)
- Simplified speech recognition flow for quicker turnaround
- Smart text preprocessing for faster TTS generation
- First-word matching for common questions
- Early returns in matching algorithms for faster responses
- Shorter timeouts for external services

### Planned Improvements
- Integration with additional LLMs beyond phi3
- Sentiment analysis for more natural responses
- Long-term memory for extended conversations
- Customizable voice and speech parameters
- Per-user learned facts and preferences

## Credits

ARI Voice Assistant was developed at Vertex Fusion Robotics using open-source technologies and libraries. Special thanks to the following projects:

- Microsoft Edge TTS for high-quality speech synthesis
- Ollama for local LLM capabilities
- ChatterBot for conversation fallback
- SpeechRecognition library for voice input
- Python ecosystem and community
