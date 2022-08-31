# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time


class HelpdeskTicketInherit(models.Model):
    _inherit = 'helpdesk.ticket'

    # tag_ids = fields.Many2one('helpdesk.tag', string='Helpdesk Team', default=_default_team_id, index=True)

    canal_type = fields.Many2one('res.canales', string='Canal', index=True)
    clasificacion_ticket = fields.Many2one('clasificacion.ticket', string='Clasificación', index=True)
    # team_id = fields.Many2one('helpdesk.team', string='Helpdesk Team', default=_default_team_id, index=True)
    user_id = fields.Many2one(
        'res.users', string='Assigned to', default=lambda self: self._get_user())
    contar = fields.Float("MeasureCuenta", compute='_calculate_percentage', compute_sudo=True, store=True)

    # CAMPOS DE TIMER
    status_ticket = fields.Selection(
        [('new', 'Nuevo'), ('progress', 'En Progreso'), ('completed', 'Completada'), ('anulated', 'Anulada')], 'Type')
    start_timer = fields.Float(string='Timer')

    start = fields.Float(string='Start')
    progress = fields.Float(string='Progress')
    completed = fields.Float(string='Completed')
    cancelled = fields.Float(string='Cancelled')

    stop = fields.Float(string='Stop')

    # GUARDAR HORAS DE TICKETS
    tiempo_new = fields.Float(string='TimerNew')
    tiempo_progress = fields.Float(string='T. Nuevo a Progreso')
    tiempo_completado = fields.Float(string='T. en Completarse')
    tiempo_anulado = fields.Float(string='T. en ser Anulado')

    @api.onchange('team_id')
    def _get_user(self):
        for record in self:
            return {'domain': {'user_id': [('helpdesk_team_id', '=', record.team_id.id)]}}

    @api.model
    def _calculate_percentage(self):
        for record in self:
            contar = self.env['helpdesk.ticket'].search_count([])
            record.contar = contar

    # FUNCIONES DE TIMER

    @api.onchange("status_ticket")
    def stopping(self):
        if self.status_ticket == 'completed' or self.status_ticket == 'anulated':
            elapsed_time = time.time() - self.start
            self.start_timer = elapsed_time

#    @api.onchange("stage_id")
#    def progressStage(self, vals):
#        for record in self:
#            if record.stage_id.id == 2:
#                vals['progress'] = time.time()
#                #result = super(HelpdeskTicketInherit, self).create(vals)
#                return result


    @api.onchange("stage_id")
    def stoppingStage(self):
        for record in self:

            if record.stage_id.id == 2:
                record.progress = time.time()
                elapsed_time_progress = time.time() - record.start
                record.tiempo_progress = elapsed_time_progress

            if record.stage_id.id == 3:
                elapsed_time_completado = time.time() - record.progress
                record.tiempo_completado = elapsed_time_completado

            if record.stage_id.id == 4:
                elapsed_time_anulado = time.time() - record.progress
                record.tiempo_anulado = elapsed_time_anulado

    @api.model
    def create(self, vals):
        vals['start'] = time.time()
        vals['progress'] = time.time()
        result = super(HelpdeskTicketInherit, self).create(vals)
        return result