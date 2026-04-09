from Fastapi import Fastapi
app = FastAPI()

@app.get("/")
def home():
    return{"message": "PRISM API Running"}