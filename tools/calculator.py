import ast
import json
import math
import operator

_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

def calculator(expression: str) -> str:
    """Calculate a basic arithmetic expression and return JSON text."""
    try:
        if not isinstance(expression, str):
            raise ValueError("Expression must be a string.")
        if len(expression) > 200:
            raise ValueError("Expression is too long.")

        tree = ast.parse(expression, mode="eval")
        result = _evaluate_ast(tree)
        return json.dumps({"expression": expression, "result": result})
    except Exception as error:
        return json.dumps({"error": str(error)})

def _evaluate_ast(node):
    """Evaluate only explicitly allowed arithmetic AST nodes."""
    if isinstance(node, ast.Expression):
        return _evaluate_ast(node.body)

    if isinstance(node, ast.Constant):
        value = node.value
        if type(value) not in (int, float):
            raise ValueError("Only numeric values are allowed.")
        if not math.isfinite(value):
            raise ValueError("Numbers must be finite.")
        return value

    if isinstance(node, ast.BinOp):
        operation_type = type(node.op)
        if operation_type not in _BINARY_OPERATORS:
            raise ValueError("Unsupported arithmetic operator.")

        left = _evaluate_ast(node.left)
        right = _evaluate_ast(node.right)

        if operation_type is ast.Pow:
            if abs(right) > 100 or abs(left) > 1_000_000:
                raise ValueError("Exponent calculation is too large.")

        result = _BINARY_OPERATORS[operation_type](left, right)

        if isinstance(result, int) and result.bit_length() > 4096:
            raise ValueError("Integer result is too large.")
        if isinstance(result, float) and not math.isfinite(result):
            raise ValueError("Result is not finite.")
        return result

    if isinstance(node, ast.UnaryOp):
        operation_type = type(node.op)
        if operation_type not in _UNARY_OPERATORS:
            raise ValueError("Unsupported unary operator.")
        return _UNARY_OPERATORS[operation_type](_evaluate_ast(node.operand))

    raise ValueError("Unsupported expression.")
