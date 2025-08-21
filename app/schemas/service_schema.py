from marshmallow import Schema, fields

class ServiceSchema(Schema):
    service_id = fields.Int(dump_only=True)
    booking_id = fields.Int(required=True)
    service_name = fields.Str(required=True)
    price = fields.Float(required=True)
    status = fields.Str()
