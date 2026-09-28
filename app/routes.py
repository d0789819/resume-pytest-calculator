"""HTTP routes for the calculation CRUD API."""

from numbers import Real

from flask import Blueprint, current_app, jsonify, request

from app.database import Calculation, db
from app.services import send_audit_event
from calculator import add, divide

api = Blueprint("api", __name__)
OPERATIONS = {"add": add, "divide": divide}


def _error(message: str, status: int):
    return jsonify({"error": message}), status


def _parse_calculation_payload():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return None, "request body must be a JSON object"

    missing = [field for field in ("operation", "a", "b") if field not in payload]
    if missing:
        return None, f"missing fields: {', '.join(missing)}"

    operation = payload["operation"]
    if operation not in OPERATIONS:
        return None, "operation must be 'add' or 'divide'"

    a, b = payload["a"], payload["b"]
    if (
        not isinstance(a, Real)
        or isinstance(a, bool)
        or not isinstance(b, Real)
        or isinstance(b, bool)
    ):
        return None, "a and b must be numbers"

    if operation == "divide" and b == 0:
        return None, "cannot divide by zero"

    return {"operation": operation, "a": float(a), "b": float(b)}, None


def _calculate(data: dict) -> float:
    return float(OPERATIONS[data["operation"]](data["a"], data["b"]))


@api.get("/")
def index():
    return jsonify(
        {
            "service": "pytest-demo",
            "endpoints": ["/health", "/calculations"],
        }
    )


@api.get("/health")
def health():
    return jsonify({"status": "ok"})


@api.get("/calculations")
def list_calculations():
    records = db.session.execute(
        db.select(Calculation).order_by(Calculation.id)
    ).scalars()
    return jsonify([record.to_dict() for record in records])


@api.get("/calculations/<int:calculation_id>")
def get_calculation(calculation_id: int):
    record = db.session.get(Calculation, calculation_id)
    if record is None:
        return _error("calculation not found", 404)
    return jsonify(record.to_dict())


@api.post("/calculations")
def create_calculation():
    data, validation_error = _parse_calculation_payload()
    if validation_error:
        return _error(validation_error, 400)

    record = Calculation(**data, result=_calculate(data))
    db.session.add(record)
    db.session.commit()

    send_audit_event(
        current_app.config["AUDIT_SERVICE_URL"],
        {"action": "calculation.created", "calculation_id": record.id},
    )
    return jsonify(record.to_dict()), 201


@api.put("/calculations/<int:calculation_id>")
def update_calculation(calculation_id: int):
    record = db.session.get(Calculation, calculation_id)
    if record is None:
        return _error("calculation not found", 404)

    data, validation_error = _parse_calculation_payload()
    if validation_error:
        return _error(validation_error, 400)

    record.operation = data["operation"]
    record.a = data["a"]
    record.b = data["b"]
    record.result = _calculate(data)
    db.session.commit()
    return jsonify(record.to_dict())


@api.delete("/calculations/<int:calculation_id>")
def delete_calculation(calculation_id: int):
    record = db.session.get(Calculation, calculation_id)
    if record is None:
        return _error("calculation not found", 404)

    db.session.delete(record)
    db.session.commit()
    return "", 204
