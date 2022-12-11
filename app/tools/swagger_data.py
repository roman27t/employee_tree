from decimal import Decimal

DATA_SWAGGER = {
    "StaffPatch": {"type": "object", "properties": {"last_name": {"type": "string", "default": "Petrov"}}},
    "StaffPost": {
        "type": "object",
        "properties": {
            "last_name": {"type": "string", "default": "Ivanov"},
            "first_name": {"type": "string", "default": "Roman"},
            "parent_id": {"type": "int", "default": 1},
            "wage_rate": {"type": "float", "default": Decimal(1.22)},
            "position_id": {"type": "int", "description": "id - Employee's position", "default": 1},
            "birthdate": {"type": "date", "default": "2000-12-22"},
        },
    },
    "PositionPost": {
        "type": "object",
        "properties": {
            "name": {"type": "string", "default": "economist"},
            "detail": {"type": "string", "default": "detail of economist"},
        },
    },
}
