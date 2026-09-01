from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

calculations = {}
next_id = 1

class CalculationRequest(BaseModel):
    a: float
    b: float
    operation: str
    
class CalculationPatch(BaseModel):
    a: float | None = None
    b: float | None = None
    operation: str | None = None

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
    global next_id

    if calculation.operation == "add":
        result = calculation.a + calculation.b

    elif calculation.operation == "divide":
        if calculation.b == 0:
            raise HTTPException(
                status_code=400,
                detail="Division by zero is not allowed"
            )
        
    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported operation"
        )

    calculation_data = {
        "id": next_id,
        "a": calculation.a,
        "b": calculation.b,
        "operation": calculation.operation,
        "result": result
    }

    calculations[next_id] = calculation_data
    next_id += 1

    return calculation_data


@app.get("/calculations/{calculation_id}")
def get_calculation(calculation_id: int):
    if calculation_id not in calculations:
        raise HTTPException(
            status_code=404,
            detail="Calculation not found"
        )

    return calculations[calculation_id]

@app.put("/calculations/{calculation_id}")
def update_calculation(
    calculation_id: int,
    calculation: CalculationRequest
):
    if calculation_id not in calculations:
        raise HTTPException(
            status_code=404,
            detail="Calculation not found"
        )

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

    calculation_data = {
        "id": calculation_id,
        "a": calculation.a,
        "b": calculation.b,
        "operation": calculation.operation,
        "result": result
    }

    calculations[calculation_id] = calculation_data

    return calculation_data

@app.patch("/calculations/{calculation_id}")
def patch_calculation(
    calculation_id: int,
    calculation: CalculationPatch
):
    if calculation_id not in calculations:
        raise HTTPException(
            status_code=404,
            detail="Calculation not found"
        )

    current = calculations[calculation_id]

    a = calculation.a if calculation.a is not None else current["a"]
    b = calculation.b if calculation.b is not None else current["b"]
    operation = (
        calculation.operation
        if calculation.operation is not None
        else current["operation"]
    )

    if operation == "add":
        result = a + b

    elif operation == "divide":
        if b == 0:
            raise HTTPException(
                status_code=400,
                detail="Division by zero is not allowed"
            )
        result = a / b

    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported operation"
        )

    calculation_data = {
        "id": calculation_id,
        "a": a,
        "b": b,
        "operation": operation,
        "result": result
    }

    calculations[calculation_id] = calculation_data

    return calculation_data

@app.delete("/calculations/{calculation_id}", status_code=204)
def delete_calculation(calculation_id: int):
    if calculation_id not in calculations:
        raise HTTPException(
            status_code=404,
            detail="Calculation not found"
        )

    del calculations[calculation_id]