from odoo import models, fields, api, _

class wizjanji(models.TransientModel): #inherit dari Model -> ini nama class sesuai python
    _name = 'wiz.kecantikan.janji' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk mencatat data appointment'

    janji_id = fields.Many2one('kecantikan.janji', String='ID Appointment')

    pasien_id = fields.Many2one(related='janji_id.pasien_id')
    staff_id = fields.Many2one(related='janji_id.staff_id')
    date_janji = fields.Date(related='janji_id.date_janji')
    time = fields.Selection(related='janji_id.time')
    total_harga = fields.Integer(related='janji_id.total_harga')
    date_create = fields.Date(related='janji_id.date_create')

    detail_id = fields.One2many('wiz.kecantikan.djanji', 'wiz_header_id', string='Detail')

    def action_done(self):
        for rec in self.detail_id:
            rec.djanji_id.treatment_id = rec.wiz_treatment_id
            rec.djanji_id.nama_treatment = rec.wiz_nama_treatment
            rec.djanji_id.harga = rec.wiz_harga
            rec.djanji_id.nama_beautician = rec.wiz_nama_beautician

    def default_get(self, fields_list):
        res = super(wizjanji, self).default_get(fields_list)
        res['janji_id'] = self.env.context['active_id']
        return res

    @api.onchange('janji_id')
    def onchange_janji_id(self):
        if not self.janji_id:
            return
        detail_id = self.env['wiz.kecantikan.djanji']
        for rec in self.janji_id.detail_id:
            detail_id += self.env['wiz.kecantikan.djanji'].new({
                'wiz_header_id': self.id,
                'wiz_treatment_id': rec.treatment_id.id,
                'djanji_id': rec.id
            })
            # cara embuat record baru di m2m atau o2m
        self.detail_id = detail_id

class wizdjanji(models.TransientModel):
    _name = 'wiz.kecantikan.djanji'
    _description = 'class untuk menyimpan data detail appointment'

    wiz_header_id = fields.Many2one('wiz.kecantikan.janji', string='ID Appointment')
    wiz_treatment_id = fields.Many2one('kecantikan.treatment', string="Kode Treatment", required=True,
                                       domain="[('state', '=', 'done')]")
    wiz_nama_treatment = fields.Char('Nama Treatment', compute="_compute_nama", required=True)
    wiz_harga = fields.Integer('Harga Treatment', compute="_compute_harga", required=True)
    wiz_nama_beautician = fields.Char('Nama Beautician', compute="_compute_nama2", required=True)
    wiz_date_create = fields.Date('Tanggal Create Data', required=True, default=fields.Date.context_today)

    djanji_id = fields.Many2one('kecantikan.djanji')

    @api.depends('wiz_treatment_id.name')
    def _compute_nama(self):
        for s in self:
            s.wiz_nama_treatment = "%s" % (s.wiz_treatment_id.nama_treat)

    @api.depends('wiz_treatment_id.name')
    def _compute_harga(self):
        for s in self:
            s.wiz_harga = "%s" % (s.wiz_treatment_id.harga)

    @api.depends('wiz_treatment_id.name')
    def _compute_nama2(self):
        for s in self:
            s.wiz_nama_beautician = "%s" % (s.wiz_treatment_id.nama_beautician)

