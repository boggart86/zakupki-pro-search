from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
import uvicorn
from models import SearchParams
from services.processor import get_lots, form_params_to_query
from constants import translation, default_params


app = FastAPI(title="To-Do App")

app.mount("/static", StaticFiles(directory="src/static"), name="static")


templates = Jinja2Templates(directory="src/templates")


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

@app.post('/submit', response_class=RedirectResponse)
async def submit(request: Request, params: Annotated[SearchParams, Form()]):
    params_dict = params.model_dump()
    is_none = is_all_false_dict(params_dict)
    if not is_none:
        query_params = form_params_to_query(params_dict)
        query_url = "&".join([f"{k}={v}" for k, v in query_params.items()])
        return RedirectResponse(url=f"/result?{query_url}", status_code=303)
    return RedirectResponse(url="/", status_code=303)

@app.get('/result', response_class=HTMLResponse)
async def search_results(request: Request):
    params_dict = dict(request.query_params)
    is_none = is_all_false_dict(params_dict)
    lots = []
    if not is_none:
        lots, lots_per_phrase = get_lots(
            base_url=base_url,
            params_dict=params_dict,
            translation=translation,
            default_params=default_params
        )
    return templates.TemplateResponse(
        request=request, name="index.html", context={
            "params_dict": params_dict,
            "is_none": is_none,
            "lots": lots,
            "lots_per_phrase": lots_per_phrase
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )