from odoo import api, fields, models
from odoo.exceptions import ValidationError

class Session(models.Model):
    _name = 'academy.session'
    _description = 'Session Info'

    name = fields.Char(string='Title')    
    
    # Step 1 - This code will be buggy.
    # session_number = fields.Char(default=lambda self: self.env['ir.sequence'].next_by_code('session.number'))
        
    # Step 2 - Rewrite the session number with attributes.
    session_number = fields.Char(
        'Session Number', copy=False, required=True, readonly=True,
        default='S0000')
    
    # Step 5 - Define the Datetime fields
    date_start = fields.Datetime(string="Start Date", required=True)
    date_end = fields.Datetime(string="End Date", required=True)
    
    # Step 3 - Redefine Create - This does not handle multiple record creation
    # @api.model
    # def create(self, vals):
    #     if vals.get('session_number', ('S0000')) == ('S0000'):
    #         vals['session_number'] = self.env['ir.sequence'].next_by_code('session.number')
    #     return super().create(vals)

    # Step 4 - Handle Multiple Records Create
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('session_number', ('S0000')) == ('S0000'):
                vals['session_number'] = self.env['ir.sequence'].next_by_code('session.number')
        return super().create(vals_list)
    
    #Step 6 - Add Constrains
    @api.constrains('date_start','date_end')
    def _check_end_date(self):
        for session in self:
            if(session.date_start > session.date_end):
                # Step 7 - Add validation error to imports.
                raise ValidationError('The end date can not be earlier than the start date')
                
