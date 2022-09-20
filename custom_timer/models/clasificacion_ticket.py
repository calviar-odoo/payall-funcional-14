# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time

class ClasificacionTicket(models.Model):
    _name = 'clasificacion.ticket'
    _description = 'Clasificación de los tickets'

    name = fields.Char(string='Categoria')
    clasificacion_ticket_ids = fields.One2many(string='Clasificación', comodel_name='helpdesk.ticket',
                                           inverse_name='clasificacion_ticket')
    contar = fields.Float("MeasureCuentaClasifc", compute='_calculate_percentage', compute_sudo=True, store=True)
    subclasificacion_id = fields.Many2one(string="Subclasificacion", comodel_name="subclasificacion.ticket")



    @api.model
    def _calculate_percentage(self):
        for record in self:
            contar = self.env['helpdesk.ticket'].search_count(['clasificacion_ticket', '=', 1])
            record.contar = contar



