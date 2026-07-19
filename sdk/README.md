# Fanus SDK

Python client for Fanus Verify API.

## Install

```bash
pip install requests
```

## Usage

```python
from sdk.fanus import FanusClient

client = FanusClient(api_key="your_key")

result = client.verify(
    prompt="What is the capital of France?",
    response="Paris is definitely the most important city without any doubt.",
    context=""
)

print(result["truth_score"])    # 0.3
print(result["risk"])           # high
print(result["policy_event"])   # NEGAR_WARNING
```

## Methods

| Method | Description |
|--------|-------------|
| `verify(prompt, response, context)` | Fast verify |
| `verify_deep(prompt, response)` | Deep verify with sources |
| `status()` | Engine status |
| `chat(message)` | Chat with Fanus |

## API Base URL

`https://web-production-924a5.up.railway.app`
