from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class Point(BaseModel):
    x: float
    y: float

app = FastAPI()

current_position = Point(x=0, y=0)

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/mouse-position")
async def handle(point: Point):
    global current_position
    current_position.x = point.x
    current_position.y = point.y
    return {"x": point.x, "y": point.y}

@app.get("/mouse-position")
async def handle_mouse_get():
    global current_position
    return current_position

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

