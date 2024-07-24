from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    is_admin = fields.Bool()

class ActivitySchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime()
    activity = fields.Str(required=True)
