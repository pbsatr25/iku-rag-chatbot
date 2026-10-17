# AI Agent Guidelines - Environment Variables

## DO NOT MODIFY .env FILE

The `.env` file contains sensitive credentials and configuration that has been carefully set up. **Do not modify, overwrite, or change the `.env` file** unless explicitly instructed by a developer.

### What is in .env:
- `LLM_API_KEY` - API key for LLM provider (Groq/Gemini)
- `LLM_BASE_URL` - Base URL for LLM API
- `LLM_MODEL` - Model name to use
- `LLM_TIMEOUT` - Request timeout
- `LLM_MAX_RETRIES` - Number of retry attempts
- `RAG_SERVICE_TOKEN` - Internal authentication token
- Other service credentials

### Correct approach:
1. If a key is missing/empty, ask the user for the correct value
2. If you need to change configuration, ask user first
3. Document what needs to change, don't make changes directly

### Error to avoid:
```
RuntimeError: Isi LLM_API_KEY di file .env
```
This error occurs when `.env` is not properly configured. Do not try to "fix" it by writing a new `.env` - ask the user for the correct credentials instead.
