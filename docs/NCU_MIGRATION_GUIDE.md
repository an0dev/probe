# `0.2.0` Migration Guide

Probe is evolving. This guide will help you migrate your application to `0.2.0`, also called the _New Computer Update_ (NCU).

## A New Start

To start using Probe in Python, import and instantiate the `Probe` class:

```python
from probe import Probe

agent = Probe()
agent.chat()
```

A convenient shared instance is also available:

```python
from probe import probe

probe.chat()
```

Both the class and the instance behave the same; the instance makes
one‑line usage easier.

## New Parameters

Stateless LLM attributes have moved to the `llm` sub‑object:

- `probe.model` → `probe.llm.model`
- `probe.api_key` → `probe.llm.api_key`
- `probe.llm_supports_vision` → `probe.llm.supports_vision`
- `probe.supports_function_calling` → `probe.llm.supports_functions`
- `probe.max_tokens` → `probe.llm.max_tokens`
- `probe.context_window` → `probe.llm.context_window`
- `probe.temperature` → `probe.llm.temperature`
- `probe.api_version` → `probe.llm.api_version`
- `probe.api_base` → `probe.llm.api_base`

Update any code or profile settings (the CLI `probe --profiles` command)
accordingly.

## New Static Messages Structure

- Messages are now flat and modular, allowing richer media support.
- Each message contains a `role`, `type`, `content`, and optionally
  `format` and `recipient`.
- Pass the full message list into Probe via `probe.messages = message_list`.

Example message list:

```python
[
  {"role": "user", "type": "message", "content": "Please create a plot from this data and display it as an image and then as HTML."},
  {"role": "user", "type": "image", "format": "path", "content": "path/to/image.png"},
  {"role": "assistant", "type": "message", "content": "Processing your request to generate a plot."},
  {"role": "assistant", "type": "code", "format": "python", "content": "plot = create_plot_from_data('data')\ndisplay_as_image(plot)\ndisplay_as_html(plot)"},
  {"role": "computer", "type": "image", "format": "base64.png", "content": "base64"},
  {"role": "computer", "type": "code", "format": "html", "content": "<html>Plot in HTML format</html>"},
  {"role": "computer", "type": "console", "format": "output", "content": "{HTML errors}"},
  {"role": "assistant", "type": "message", "content": "Plot generated successfully."}
]
```

## New Streaming Structure

- Streaming chunks mirror the static structure with `start`/`end` flags.
- The `confirmation` chunk is sent before executing code; cancel the
  stream if you want to run the code yourself.
- Collect chunks and reconstruct messages before passing them to Probe.

```python
{"role": "assistant", "type": "message", "start": True}
{"role": "assistant", "type": "message", "content": "Pro"}
...
{"role": "assistant", "type": "message", "end": True}

{"role": "assistant", "type": "code", "format": "python", "start": True}
{"role": "assistant", "type": "code", "format": "python", "content": "plot = create_plot_from_data"}
...
{"role": "assistant", "type": "code", "format": "python", "end": True}

{"role": "computer", "type": "confirmation", "format": "execution", "content": {
    "type": "code",
    "format": "python",
    "content": "plot = create_plot_from_data('data')\ndisplay_as_image(plot)\ndisplay_as_html(plot)",
}}

{"role": "computer", "type": "console", "start": True}
{"role": "computer", "type": "console", "format": "output", "content": "a printed statement"}
...
{"role": "computer", "type": "console", "end": True}
```

## Tips and Best Practices

- Adding `id` and `created_at` to messages helps with post‑processing.
- If your app runs the code instead of Probe, treat the app as the
  `computer` and break the stream on confirmation chunks.
- Use the streaming disconnect behavior to implement a “Stop” button.
- Forward errors from your Python server to the client for better
  debugging.

## Example Code

### Types

Python:

```python
class Message:
    role: Union["user", "assistant", "computer"]
    type: Union["message", "code", "image", "console", "file", "confirmation"]
    format: Union["output", "path", "base64.png", "base64.jpeg", "python", "javascript", "shell", "html", "active_line", "execution"]
    recipient: Union["user", "assistant"]
    content: Union[str, dict]

class StreamingChunk(Message):
    start: bool
    end: bool
```

TypeScript:

```typescript
interface Message {
  role: "user" | "assistant" | "computer";
  type: "message" | "code" | "image" | "console" | "file" | "confirmation";
  format: "output" | "path" | "base64.png" | "base64.jpeg" | "python" | "javascript" | "shell" | "html" | "active_line" | "execution";
  recipient: "user" | "assistant";
  content: string | { code: string; language: string };
}

interface StreamingChunk extends Message {
  start: boolean;
  end: boolean;
}
```

### Handling streaming chunks

```javascript
let messages = [];
let currentMessageIndex = 0;
let isGenerating = false;

async function sendRequest() {
    const params = { messages };
    const controller = new AbortController();
    const { signal } = controller;

    const probeCall = await fetch("https://YOUR_ENDPOINT/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(params),
      signal,
    });

    if (!probeCall.ok) {
      console.error("Probe didn't respond with 200 OK");
      return;
    }

    const reader = probeCall.body.getReader();
    ...
}
```

