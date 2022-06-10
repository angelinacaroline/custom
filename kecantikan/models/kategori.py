from odoo import models, fields, api, _
from odoo.exceptions import UserError

#MATERI YANG DIPAKAI : SEQUENCE (ID auto increment kalau d-delete nomor id tetap lanjut),

class kategori(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'kecantikan.kategori' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk membuat daftar kategori'

    #membuat attribute field

    name = fields.Char('ID Kategori', size=64, required=True, index=True, readonly=True,
                       default='new', states={})

    nama_kategori = fields.Char('Kategori Treatment', size=64, required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})

    date = fields.Date('Tanggal Create Data', required=True, default=fields.Date.context_today, readonly=True,
                              states={})

    state = fields.Selection(
        [('done', 'Done'),
         ('draft', 'Draft'),
         ('canceled', 'Canceled')], 'State', readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')

    treatment_id = fields.One2many('kecantikan.treatment', 'kategori_id', domain="[('state', '=', 'done')]",
                               states={'draft': [('readonly', False)]})

    _sql_constraints = [('name_unik', 'unique(name)', _('ID Kategori Harus Unik!'))]

    def action_done(self):  #approve
        self.state = 'done'
        if self.name == 'new' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "kecantikan.kategori")])
            if not seq:
                raise UserError(_("kecantikan.kategori sequence not found, please create kecantikan.kategori sequence"))
            self.name = seq.next_by_id()

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'