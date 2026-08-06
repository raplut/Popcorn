from fastapi import FastAPI

app = FastAPI(
    title="Movie Recommendation API",
    description="An API that recommends movies based on your watch history, likes and, dislikes",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "API is running"
    }