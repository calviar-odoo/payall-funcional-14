# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time


class SubClasificacionTicket(models.Model):
    _name = 'subclasificacion.ticket'
    _description = 'Clasificación de los tickets'

    name = fields.Char(string='Subcategoria')
    clasificacion_ids = fields.One2many(string="Clasificaciones", comodel_name="clasificacion.ticket",
                                        inverse_name="subclasificacion_id")
    contar = fields.Float("MeasureCuentaClasifc", compute='_calculate_percentage', compute_sudo=True, store=True)

    @api.model
    def _calculate_percentage(self):
        for record in self:
            contar = self.env['helpdesk.ticket'].search_count(['clasificacion_ticket', '=', 1])
            record.contar = contar
