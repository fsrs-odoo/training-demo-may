from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import date_utils

class Session(models.Model):
    _name = 'academy.session'
    _description = 'Session Info'
    # Step 2 - Add Inherit
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Title', related="course_id.name", readonly=False)    
    
    session_number = fields.Char(
        'Session Number', copy=False, required=True, readonly=True,
        default='S0000')
    date_start = fields.Datetime(string="Start Date", required=True)
    date_end = fields.Datetime(string="End Date", required=True)
    duration = fields.Integer(string="Session Duration", compute="_compute_session_duration", inverse="_inverse_session_duration")
    # Step 3 - Add tracking attribute
    course_id = fields.Many2one(comodel_name="academy.course",
                               string="Course",
                               ondelete="cascade",
                               required=True,
                               tracking=True)
    instructor_id = fields.Many2one(comodel_name="res.users",
                                   string="Instructor",
                                   ondelete="restrict",
                                   tracking=True,)
    student_ids = fields.Many2many(comodel_name="res.partner",
                                   string="Students")
    description = fields.Text(related="course_id.description")
    
    # Kanban View Demo - Create Session Stage Model
    stage_id = fields.Many2one('academy.session.stage')
    state = fields.Selection(string='State', related="stage_id.state", readonly=False)
    
    #Status Example
    kanban_state = fields.Selection(
        [("normal", "In Progress"),
         ("blocked", "Blocked"),
         ("done", "Ready for next stage")],
        "Kanban State",
        default="normal")
    color = fields.Integer()
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('session_number', ('S0000')) == ('S0000'):
                vals['session_number'] = self.env['ir.sequence'].next_by_code('session.number')
        return super().create(vals_list)
    
    @api.constrains('date_start','date_end')
    def _check_end_date(self):
        for session in self:
            if(session.date_start > session.date_end):
                raise ValidationError('The end date can not be earlier than the start date')
    
    @api.depends('date_start','date_end')
    def _compute_session_duration(self):
        for record in self:
            if record.date_start and record.date_end:
                record.duration = (record.date_end - record.date_start).days + 1
            
    def _inverse_session_duration(self):
        for record in self:
            if record.date_start and record.duration:
                record.date_end = date_utils.add(record.date_start,days=record.duration-1)
