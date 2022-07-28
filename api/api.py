from LinearFunction import LinearFunction
from flask import Blueprint, request


api_bp = Blueprint('api_bp', __name__) # "API Blueprint"


@api_bp.route("/greeting")  # Blueprints don't use the Flask "app" context. They use their own blueprint's
def greeting():
    return {'greeting': 'Hello from me, Mario!'}


@api_bp.route("/linear/points", methods=["POST"])
def equation():
    data = request.get_json()
    try:
        linear_function = LinearFunction(
            data['function-name'],
            (data['X1'], data['Y1']),
            (data['X2'], data['Y2']),
        )
    except ZeroDivisionError:
        return "Zero Division", 400
    return {
        'equation': linear_function.equation(),
        'slope': linear_function.slope,
        'y_intersection': linear_function.y_intersection
    }
