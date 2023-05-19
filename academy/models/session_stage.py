from odoo import fields, models

# Kanban View Demo - Model created for Kanban Example
class SessionStage(models.Model):
    _name = "academy.session.stage"
    _description = "Session Stage"
    _order = "sequence"

    name = fields.Char()
    sequence = fields.Integer(default=10)
    fold = fields.Boolean()
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "Not Started"),
            ("open", "In Progress"),
            ("done", "Finalized"),
            ("cancel", "Canceled"),
        ],
        default="new",
    )