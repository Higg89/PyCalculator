from fastapi import FastAPI, HTTPException
import ast
import operator

app = FastAPI()

# Переменная для хранения текущего выражения
current_expression = ""

# Определение поддерживаемых операций
operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}

def safe_eval(expression: str):
    """
    Безопасная оценка математического выражения.
    """
    try:
        # Парсим строку в абстрактное синтаксическое дерево (AST)
        node = ast.parse(expression, mode='eval').body

        def evaluate(node):
            if isinstance(node, ast.Num):  # <number>
                return node.n
            elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
                return operators[type(node.op)](evaluate(node.left), evaluate(node.right))
            elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
                return operators[type(node.op)](evaluate(node.operand))
            else:
                raise TypeError(f"Неподдерживаемая операция: {ast.dump(node)}")

        return evaluate(node)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при вычислении выражения: {str(e)}")

@app.post("/add/")
async def add(a: float, b: float):
    """Метод для сложения двух чисел."""
    global current_expression
    result = a + b
    current_expression = f"{a} + {b}"
    return {"result": result, "expression": current_expression}

@app.post("/subtract/")
async def subtract(a: float, b: float):
    """Метод для вычитания двух чисел."""
    global current_expression
    result = a - b
    current_expression = f"{a} - {b}"
    return {"result": result, "expression": current_expression}

@app.post("/multiply/")
async def multiply(a: float, b: float):
    """Метод для умножения двух чисел."""
    global current_expression
    result = a * b
    current_expression = f"{a} * {b}"
    return {"result": result, "expression": current_expression}

@app.post("/divide/")
async def divide(a: float, b: float):
    """Метод для деления двух чисел."""
    global current_expression
    if b == 0:
        raise HTTPException(status_code=400, detail="Деление на ноль невозможно.")
    result = a / b
    current_expression = f"{a} / {b}"
    return {"result": result, "expression": current_expression}

@app.post("/evaluate_expression/")
async def evaluate_expression(expression: str):
    """Метод для вычисления сложного математического выражения."""
    global current_expression
    current_expression = expression
    result = safe_eval(expression)
    return {"result": result, "expression": current_expression}

# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)