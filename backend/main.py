from fastapi import FastAPI
from .routes import data_routes, summary_routes
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development, consider restricting this for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

app.include_router(data_routes.router)
app.include_router(summary_routes.router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI"}



app.mount("/static",StaticFiles(directory="frontend"),name="static")

@app.get("/datatable",response_class= HTMLResponse)
async def read_root():
    with open("frontend/index.html") as f:
        html_content = f.read()
    return HTMLResponse(content= html_content)