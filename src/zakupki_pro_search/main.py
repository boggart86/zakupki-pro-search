from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
import uvicorn
from models import SearchParams


app = FastAPI(title="To-Do App")

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


params_dict = {}

@app.get('/', response_class=HTMLResponse)
async def main_page(request: Request):
    is_none = all(param is None for param in params_dict.values())
    return templates.TemplateResponse(
        request=request, name="index.html", context={"params_dict": params_dict, "is_none": is_none}
    )


@app.post('/')
async def search_results(request: Request, params: Annotated[SearchParams, Form()]):
    params_dict = params.model_dump()
    is_none = all(param is None for param in params_dict.values())
    return templates.TemplateResponse(
        request=request, name="index.html", context={"params_dict": params_dict, "is_none": is_none}
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )