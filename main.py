from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
import uvicorn
from models import SearchParams
from services.processor import get_lots
from constants import translation, default_params


app = FastAPI(title="To-Do App")

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


base_url = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html"

params_dict = {}

def is_all_false_dict(params_dict: dict):
    # состоитли словарь полностью из значений, которые == False
    return all((not param) for param in params_dict.values())

@app.get('/', response_class=HTMLResponse)
async def main_page(request: Request):
    is_none = is_all_false_dict(params_dict)
    return templates.TemplateResponse(
        request=request, name="index.html", context={"params_dict": params_dict, "is_none": is_none}
    )


@app.post('/')
async def search_results(request: Request, params: Annotated[SearchParams, Form()]):
    params_dict = params.model_dump()
    is_none = is_all_false_dict(params_dict)
    lots = []
    if not is_none:
        lots = get_lots(base_url=base_url, params_dict=params_dict, translation=translation, default_params=default_params)
    return templates.TemplateResponse(
        request=request, name="index.html", context={"params_dict": params_dict, "is_none": is_none, "lots": lots}
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )