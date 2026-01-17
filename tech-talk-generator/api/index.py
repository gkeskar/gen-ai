import os
from fastapi import FastAPI, Query  # type: ignore
from fastapi.responses import StreamingResponse  # type: ignore
from openai import OpenAI  # type: ignore

DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
app = FastAPI()

@app.get("/api")
def idea(topic: str = Query(default="AI in DevOps", description="Topic for tech talk ideas")):
    api_key = os.getenv("DEEPSEEK_API_KEY")
    client = OpenAI(base_url=DEEPSEEK_BASE_URL, api_key=api_key)
    
    prompt = [{
        "role": "user", 
        "content": f"""Generate a list of engaging tech talk topic ideas for a technical summit about: {topic}

For each topic idea, include:
- A catchy title
- A brief description (2-3 sentences)
- Key takeaways for the audience

Format with headings, sub-headings and bullet points. Provide 5-7 topic ideas."""
    }]
    
    stream = client.chat.completions.create(model="deepseek-chat", messages=prompt, stream=True)

    def event_stream():
        for chunk in stream:
            text = chunk.choices[0].delta.content
            if text:
                lines = text.split("\n")
                for line in lines:
                    yield f"data: {line}\n"
                yield "\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
