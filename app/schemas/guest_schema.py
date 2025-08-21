from marshmallow import Schema, fields

class GuestSchema(Schema):
    guest_id = fields.Int(dump_only=True)  # только для чтения
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    passport_number = fields.Str(required=True)
    phone_number = fields.Str()
    email = fields.Email()
