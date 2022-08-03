from FunctionCollection import FunctionCollection
from LinearFunction import LinearFunction
from flask import Blueprint, request


api_bp = Blueprint('api_bp', __name__)  # "API Blueprint"


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


@api_bp.route("/linear/single/graph", methods=["POST"])
def single_function_graph():
    data = request.get_json()
    print(data)
    linear_func = LinearFunction(name=data['function-name'], slope=data['slope'], y_intersection=data['y_intersection'])
    return linear_func.graph_json()


@api_bp.route("/linear/multiple/graph", methods=["POST"])
def multiple_function_graph():
    payload = request.get_json()
    print(payload)
    lf_objects = []
    for lf in payload:
        linear_func = LinearFunction(name=lf['function-name'], slope=lf['slope'], y_intersection=lf['y_intersection'])
        lf_objects.append(linear_func)
    fc = FunctionCollection(*lf_objects)
    return fc.graph_json()


# @api_bp.route("/linear/multiple/graph", methods=["POST"])
# def multiple_function_graph():
#     oferta = LinearFunction(
#         name="Oferta",
#         point1=(2000, 250),
#         point2=(4000, 750)
#     )
#     demanda = LinearFunction(
#         name="Demanda",
#         point1=(2500, 450),
#         point2=(3000, 300)
#     )
#
#     return FunctionCollection(
#         oferta,
#         demanda,
#         LinearFunction(
#             name="Otra",
#             point1=(3500, 450),
#             point2=(6000, 300)
#         )
#     ).graph_json()
