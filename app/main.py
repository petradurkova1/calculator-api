from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "OK"}


@app.get("/calculate/add")
def add(a: float, b: float):
    return {"result": a + b}


@app.get("/calculate/divide")
def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(
            status_code=400,
            detail="Division by zero is not allowed"
        )

    return {"result": a / b}