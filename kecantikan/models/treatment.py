from odoo import models, fields, api, _
from odoo.exceptions import UserError

#MATERI YANG DIPAKAI : SEQUENCE (ID auto increment kalau d-delete nomor id tetap lanjut),

class treatment(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'kecantikan.treatment' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk membuat daftar treatment'

    #membuat attribute field

    name = fields.Char('ID Treatment', size=64, required=True, index=True, readonly=True,
                       default='new', states={})

    nama_treat = fields.Char('Treatment', size=64, required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})

    harga = fields.Integer('Harga Treatment', size=64, required=True, index=True, readonly=True,
                             states={'draft': [('readonly', False)]})

    kategori_id = fields.Many2one('kecantikan.kategori', string="Kategori", readonly=True, required=True,
                                  domain="[('state', '=', 'done')]", states={'draft': [('readonly', False)]})

    date = fields.Date('Tanggal Create Data', required=True, default=fields.Date.context_today, readonly=True,
                              states={})

    state = fields.Selection(
        [('done', 'Done'),
         ('draft', 'Draft'),
         ('canceled', 'Canceled')], 'State', readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')

    beautician_id = fields.Many2one('kecantikan.beautician', string="Beautician", readonly=True, required=True,
                                    domain="[('state', '=', 'done'), ('active', '=', 'true')]",
                                    states={'draft': [('readonly', False)]})

    nama_beautician = fields.Char('Nama Beautician', compute="_compute_nama", index=True, readonly=True,
                                  required=True, states={})

    _sql_constraints = [('name_unik', 'unique(name)', _('ID Treatment Harus Unik!'))]

    def action_done(self):  #approve
        self.state = 'done'
        if self.name == 'new' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "kecantikan.treatment")])
            if not seq:
                raise UserError(_("kecantikan.treatment sequence not found, please create kecantikan.treatment sequence"))
            self.name = seq.next_by_id()

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.depends('beautician_id.name')
    def _compute_nama(self):
        for s in self:
            s.nama_beautician = "%s" % (s.beautician_id.nama_beautician)