from celery.result import AsyncResult
from fastapi import FastAPI
import uvicorn
import tasks



app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/generate-article")
async def generate_article_endpoint(video_url: str):
    task = tasks.process_article_generation.delay(video_url)
    return {"task_id": task.id}

@app.get("/task/{id}")
async def get_status(id: str):
    task_result = AsyncResult(id)
    if task_result.ready():
        return {"status": task_result.state, "result": task_result.result}
    elif task_result.failed():
        return {"status": task_result.state, "result": task_result.result}
    else:
        return {"status": task_result.state}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)