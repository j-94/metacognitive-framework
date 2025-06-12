# Donkey Usage Guide

## Running Without OpenAI API (Simulation Mode)

By default, the system runs in simulation mode with realistic but fake responses:

```bash
make run-real
```

You'll see:
- "⚠️ No OPENAI_API_KEY found - using simulation mode"
- Simulated responses like "This is a simulated response..."

## Running With Real OpenAI API

To use actual AI responses:

1. **Set your OpenAI API key**:
   ```bash
   export OPENAI_API_KEY=sk-your-api-key-here
   ```

2. **Install OpenAI library** (if needed):
   ```bash
   pip install openai
   ```

3. **Run the system**:
   ```bash
   make run-real
   ```

You'll see:
- "✅ OpenAI API key found (using gpt-3.5-turbo)"
- Real AI-generated responses to your tasks

## Viewing Results

After running, open the trace viewer:
```bash
open trace_latest.html
```

This shows:
- Token usage per task
- Which tasks were mutated (🧬)
- Actual responses
- Budget tracking

## Removing Simulation Messages

The simulation messages only appear when:
1. No OPENAI_API_KEY is set, OR
2. The OpenAI library isn't installed, OR  
3. The API call fails

To get real responses, ensure you have:
- Valid API key exported
- OpenAI library installed
- Active internet connection