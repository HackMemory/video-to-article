from celery.result import AsyncResult
import uvicorn
import tasks

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="storage/picture"), name="images")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


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
    
@app.delete("/task/{id}")
async def stop_task(id: str):
    tasks.celery_app.control.revoke(id, terminate=True)
    return {"status": "STOPPED"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)