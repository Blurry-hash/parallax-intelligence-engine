# Model strategy: latest available, not imaginary latest

This repository is **provider-neutral**. Model catalogs and reasoning controls change continuously. Do not pin a name merely because another assistant called it the best.

## Provider classes
OpenAI (GPT family and open-weight gpt-oss), Anthropic (Claude), Google (Gemini), xAI (Grok), DeepSeek, Alibaba Qwen, Moonshot Kimi and other publicly documented providers. The collection is not a ranking or a claim these providers are connected.

## Selection / evaluation

- List actual connected models from the API or product UI with version/date, tool modalities and supported effort settings.
- For high-impact tasks, choose highest *supported* reasoning effort when expected benefit exceeds added latency/cost.
- Evaluate with task-specific accuracy, independent tests, hallucination rate, latency p50/p95, token cost and actual tool access.
- For genuinely separate models, use independent outputs, then adjudication based on decisive evidence. Don't equate four prompts to the same model with four independent models.
- Track version drift and revalidate after provider changes; never copy an unverifiable internal system prompt and treat it as authoritative.
- Secure credentials; no API keys in git, copied URL parameters or public demos.

## Examples of official technical sources

- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)
- [PydanticAI and evaluations](https://github.com/pydantic/pydantic-ai)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Hugging Face Open R1](https://github.com/huggingface/open-r1)
- [Qwen3](https://github.com/QwenLM/Qwen3)

**Outcome contract:** skill-transfer means better instructions/workflows and observed results. It does not change the current model's trained weights or grant uninstalled APIs.
