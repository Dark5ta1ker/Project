from marshmallow import Schema, fields

class BookingSchema(Schema):
    booking_id = fields.Int(dump_only=True)
    guest_id = fields.Int(required=True)
    room_id = fields.Int(required=True)
    check_in = fields.Date(required=True)
    check_out = fields.Date(required=True)
    status = fields.Str()
    total_price = fields.Float()
