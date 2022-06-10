from odoo import models, fields, api, _
from odoo.exceptions import UserError

#MATERI YANG DIPAKAI : SEQUENCE (ID auto increment kalau d-delete nomor id tetap lanjut),
#                    : @API.DEPENDS (Buat create ID otomatis, Cek Tanggal),

class djanji(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'kecantikan.djanji' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk membuat daftar detail janji'

    #membuat attribute field

    name = fields.Char('ID Detail Appointment', size=64, required=True, index=True, readonly=True,
                       default='new', states={})

    janji_id = fields.Many2one('kecantikan.janji', string="Kode Appointment", readonly=True, required=True,
                               domain="[('state', '=', 'done')]",
                               states={'draft': [('readonly', False)]})

    treatment_id = fields.Many2one('kecantikan.treatment', string="Kode Treatment", readonly=True, required=True,
                                domain="[('state', '=', 'done')]",
                                states={'draft': [('readonly', False)]})

    nama_treatment = fields.Char('Nama Treatment', compute="_compute_nama", required=True, index=True, readonly=True,
                           states={})

    harga = fields.Integer('Harga Treatment', compute="_compute_harga", required=True, index=True, readonly=True,
                           states={'draft': [('readonly', False)]})

    nama_beautician = fields.Char('Nama Beautician', compute="_compute_nama2", required=True, index=True, readonly=True,
                           states={})

    date_create = fields.Date('Tanggal Create Data', required=True, default=fields.Date.context_today, readonly=True,
                              states={})

    state = fields.Selection(
        [('done', 'Done'),
         ('draft', 'Draft'),
         ('canceled', 'Canceled')], 'State', readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')

    _sql_constraints = [('name_unik', 'unique(name)', _('ID Detail Janji Harus Unik!'))]

    def action_done(self):  #approve
        self.state = 'done'
        if self.name == 'new' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "kecantikan.djanji")])
            if not seq:
                raise UserError(_("kecantikan.djanji sequence not found, please create kecantikan.djanji sequence"))
            self.name = seq.next_by_id()

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.depends('treatment_id.name')
    def _compute_nama(self):
        for s in self:
            s.nama_treatment = "%s" % (s.treatment_id.nama_treat)

    @api.depends('treatment_id.name')
    def _compute_harga(self):
        for s in self:
            s.harga = "%s" % (s.treatment_id.harga)

    @api.depends('treatment_id.name')
    def _compute_nama2(self):
        for s in self:
            s.nama_beautician = "%s" % (s.treatment_id.nama_beautician)