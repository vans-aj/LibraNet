# LangChain + LangSmith Setup for LibraNet

## ✅ What I Fixed

### 1. **Model Compatibility Issue**
**Problem**: LangChain's `langchain_google_genai` uses Google's `v1beta` API, which doesn't support newer model names like:
- ❌ `gemini-1.5-flash` 
- ❌ `gemini-1.5-pro`
- ❌ `gemini-2.0-flash-exp`

**Solution**: Use `gemini-pro` - the ONLY model that works with v1beta API
```python
ChatGoogleGenerativeAI(
    model="gemini-pro",  # ✅ This works!
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True
)
```

### 2. **Converted Both Features to LangChain**
✅ **Chatbot** (`app/services/chatbot.py`)
- Using LangChain's `ChatGoogleGenerativeAI`
- Proper chain with `ChatPromptTemplate | LLM | StrOutputParser`
- Context-aware prompts with user information

✅ **Word Meaning** (`app/routes/ebook_routes.py`)
- Using same LangChain setup
- Handles both single words and sentences/phrases
- Formatted prompts for clear responses

### 3. **Enabled LangSmith Tracing**
Added to `.env`:
```bash
# LangSmith Tracing Configuration
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY="your_langchain_api_key_here"
LANGCHAIN_PROJECT="LibraNet-AI"
```

## 📊 View Your Traces

1. Go to [LangSmith](https://smith.langchain.com/)
2. Sign in with your account
3. Select project: **"LibraNet-AI"**
4. You'll see all AI interactions:
   - User questions
   - Prompts sent to Gemini
   - Model responses
   - Latency and token usage
   - Error logs

## 🔧 How It Works Now

### Chatbot Flow
```
User Message 
  → Get context (user info, library stats)
  → Build prompt with ChatPromptTemplate
  → ChatGoogleGenerativeAI (gemini-pro)
  → StrOutputParser
  → Response to user
  → Automatically traced in LangSmith ✅
```

### Word Meaning Flow
```
User selects word/sentence
  → Detect if word or sentence
  → Choose appropriate prompt
  → ChatGoogleGenerativeAI (gemini-pro)
  → StrOutputParser
  → Display meaning in modal
  → Automatically traced in LangSmith ✅
```

## 🎯 Key Files Modified

1. **`app/services/chatbot.py`**
   - Imports: `ChatGoogleGenerativeAI`, `ChatPromptTemplate`, `StrOutputParser`
   - Model: `gemini-pro` (not gemini-1.5-flash)
   - Chain-based architecture for both chat and recommendations

2. **`app/routes/ebook_routes.py`**
   - Imports: Same LangChain imports
   - Model: `gemini-pro`
   - Separate prompts for words vs sentences

3. **`.env`**
   - Added `LANGCHAIN_TRACING_V2=true`
   - Added `LANGCHAIN_ENDPOINT`
   - Renamed project to `LibraNet-AI`

## ⚠️ Important Notes

1. **Don't change the model name** from `gemini-pro` - it's the only one that works with LangChain's v1beta API

2. **LangSmith tracing is automatic** - no code changes needed once env vars are set

3. **Check traces at**: https://smith.langchain.com/

4. **Model limitations**: `gemini-pro` is slightly older than `gemini-1.5-flash` but still very capable

## 🚀 Testing

1. **Test Chatbot**: Ask any library question
2. **Test Word Meaning**: Select any word in ebook reader
3. **Check LangSmith**: See traces in dashboard

## 📈 Benefits of LangSmith Tracing

✅ **Debug issues** - See exact prompts and responses
✅ **Monitor performance** - Track latency and costs
✅ **Improve prompts** - Compare different versions
✅ **User insights** - Understand common questions
✅ **Error tracking** - Catch and fix issues quickly

## 🔗 Resources

- [LangSmith Docs](https://docs.smith.langchain.com/)
- [LangChain Google GenAI](https://python.langchain.com/docs/integrations/chat/google_generative_ai)
- [Gemini Models](https://ai.google.dev/models/gemini)
