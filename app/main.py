from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class CalculationRequest(BaseModel):
    a: float
    b: float
    operation: str


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


@app.post("/calculations", status_code=201)
def create_calculation(calculation: CalculationRequest):
    if calculation.operation == "add":
        result = calculation.a + calculation.b

    elif calculation.operation == "divide":
        if calculation.b == 0:
            raise HTTPException(
                status_code=400,
                detail="Division by zero is not allowed"
            )
        result = calculation.a / calculation.b

    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported operation"
        )

    return {
        "a": calculation.a,
        "b": calculation.b,
        "operation": calculation.operation,
        "result": result
    }