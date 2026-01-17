# 🎤 Tech Talk Idea Generator

An AI-powered web application that generates tech talk topic ideas for technical summits and conferences.

## 🎯 What It Does

Enter a topic (like "AI in DevOps") and get 5-7 engaging tech talk ideas with:
- Catchy titles
- Brief descriptions
- Key takeaways for the audience

## 🏗️ Architecture

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Browser   │  ────►  │   Backend   │  ────►  │  DeepSeek   │
│  (Frontend) │  ◄────  │   (Python)  │  ◄────  │     AI      │
└─────────────┘         └─────────────┘         └─────────────┘
     User                  Your Code              AI Service
   sees this             processes this         generates ideas
```

## 📁 Project Structure

| File | Purpose |
|------|---------|
| `pages/index.tsx` | Frontend - the webpage users see and interact with |
| `api/index.py` | Backend - Python API that talks to DeepSeek AI |
| `styles/globals.css` | Styling for markdown content |
| `requirements.txt` | Python dependencies (fastapi, openai) |
| `package.json` | JavaScript dependencies (react, next) |

## 🛠️ Tech Stack

**Frontend:**
- Next.js (React framework)
- TypeScript
- Tailwind CSS
- React Markdown

**Backend:**
- Python
- FastAPI
- OpenAI SDK (configured for DeepSeek)

**Deployment:**
- Vercel (hosts both frontend and backend)

## 🔑 Key Concepts Learned

### Frontend (TypeScript/React)
| Concept | What it means |
|---------|---------------|
| `useState` | Remembers values (like the topic text, loading state) |
| `EventSource` | Receives streaming responses from backend |
| `className="..."` | Tailwind CSS - styling with preset classes |
| `<ReactMarkdown>` | Converts AI's markdown text into nice HTML |

### Backend (Python)
| Concept | What it means |
|---------|---------------|
| `FastAPI` | Framework that makes creating APIs easy |
| `@app.get("/api")` | "When someone visits /api, run this function" |
| `Query(...)` | Gets the `?topic=xxx` from the URL |
| `OpenAI(...)` | Library to talk to AI (works with DeepSeek too) |
| `StreamingResponse` | Sends response in chunks |

## 🚀 Deployment

1. **Link to Vercel:**
   ```bash
   vercel link
   ```

2. **Add API Key:**
   ```bash
   vercel env add DEEPSEEK_API_KEY
   ```

3. **Deploy:**
   ```bash
   vercel --prod
   ```

## 💡 The Simplest Mental Model

```
Frontend = Waiter (takes order, serves food)
Backend  = Kitchen (prepares the food)
AI API   = Chef (does the actual cooking)
```

## 📝 Note on Streaming

Vercel's Python Serverless Functions buffer streaming responses, so content loads all at once rather than streaming in real-time. This is a Vercel infrastructure limitation, not a code issue.

---

**Built with ❤️ while learning AI application development**
