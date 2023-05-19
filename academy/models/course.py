from odoo import api, fields, models
from odoo.exceptions import ValidationError

class Course(models.Model):
    _name = "academy.course"
    _description = "Course Info"
    
    # Reserved Fields
    name = fields.Char(string='Title', required=True)
    active = fields.Boolean(string='Active', default=True)
   
    # Simple Fields
    description = fields.Text(string='Description')
    level = fields.Selection(string='Level',
                            selection=[('beginner', 'Beginner'),
                                       ('intermediate', 'Intermediate'),
                                       ('advanced', 'Advanced')],
                            copy=False)
    session_ids = fields.One2many(comodel_name="academy.session",
                                 string="Sessions",
                                 inverse_name="course_id")
    currency_id = fields.Many2one(comodel_name="res.currency",
                                  default=lambda self:self.env.company.currency_id.id)
    base_price = fields.Monetary(string="Base Price", currency_field="currency_id")
    additional_fee = fields.Monetary(string="Additional Fee", currency_field="currency_id")
    total_price = fields.Monetary(string="Total Price", currency_field="currency_id", compute="_compute_total_price", store=True)
    
    # Advanced Fields Demo - Add Smartbutton to Form View
    active_session_count = fields.Integer('# Sessions', compute='_compute_session_count')
    
    @api.depends("base_price","total_price")
    def _compute_total_price(self):
        for record in self:
            if(record.base_price < 0):
                raise ValidationError(('Base Price can not be negative'))
            record.total_price = record.base_price + record.additional_fee
    # This example may cause performance issues. Do not do record search operations inside loops.
    @api.depends('session_ids.course_id')
    def _compute_session_count(self):
        read_group_sessions = self.env['academy.session'].sudo()._read_group([
            ('course_id', 'in', self.ids), 
            ('stage_id.state','not in',["done","cancel"])
        ], ['course_id'], 'course_id')      
        data = dict((res['course_id'][0], res['course_id_count']) for res in read_group_sessions)
        for course in self:
            course.active_session_count = data.get(course.id, 0)            
                
    # --------------------------------------- Smart Button Action ---------------------------------  
    # Advanced Fields Demo, Add Action through Python.
    def action_redirect_sessions(self):
        action = self.env["ir.actions.act_window"]._for_xml_id('academy.session_list_action')
        action['context'] = {
            'default_course_id': self.id
        }
        action['domain'] = [('course_id', "=", self.id)]
        return action