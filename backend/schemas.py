from marshmallow import Schema, fields


class NestedMeasurementSchema(Schema):
    name = fields.Str(required=True)
    value = fields.Float(required=True)
    unit = fields.Str(required=True)


class IntervalSchema(Schema):
    start = fields.DateTime(required=True)
    end = fields.DateTime(required=True)


class MeasurementSchema(Schema):
    project = fields.Str(required=True)
    measurement = fields.Nested(NestedMeasurementSchema, required=True)
    interval = fields.Nested(IntervalSchema, required=True)
