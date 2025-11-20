from fastapi import FastAPI
from controller import router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(router) 
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,  # Allows cookies to be included in cross-origin requests
        allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],  # Allows all headers
    )



@app.get("/")
def root():
    return {"msg": "MyToken FastAPI backend is running "}