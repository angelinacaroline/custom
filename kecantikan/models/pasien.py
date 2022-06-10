from odoo import models, fields, api, _
from odoo.exceptions import UserError

#MATERI YANG DIPAKAI : SEQUENCE (ID auto increment kalau d-delete nomor id tetap lanjut),

class pasien(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'kecantikan.pasien' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk membuat daftar pasien'

    #membuat attribute field

    name = fields.Char('ID Pelanggan', size=64, required=True, index=True, readonly=True,
                       default='new', states={})

    nama_pasien = fields.Char('Nama Pelanggan', size=64, required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})

    date_lahir = fields.Date('Tanggal Lahir', required=True, readonly=True,
                             states={'draft': [('readonly', False)]})

    gender = fields.Selection(
        [('pria', 'Pria'),  # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
         ('wanita', 'Wanita')],
        required=True, readonly=True, states={'draft': [('readonly', False)]})

    alamat = fields.Char('Alamat Pelanggan', size=64, required=True, index=True, readonly=True,
                              states={'draft': [('readonly', False)]})

    no_telp = fields.Char('No. Telepon', size=64, required=True, index=True, readonly=True,
                              states={'draft': [('readonly', False)]})

    date_gabung = fields.Date('Tanggal Gabung', required=True, default=fields.Date.context_today, readonly=True,
                              states={})

    state = fields.Selection(
        [('done', 'Done'),
         ('draft', 'Draft'),
         ('canceled', 'Canceled')], 'State', readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')

    janji_id = fields.One2many('kecantikan.janji', 'pasien_id', domain="[('state', '=', 'done')]",
                                   states={'draft': [('readonly', False)]})

    _sql_constraints = [('name_unik', 'unique(name)', _('ID Pelanggan Harus Unik!'))]

    def action_done(self):  #approve
        self.state = 'done'
        if self.name == 'new' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "kecantikan.pasien")])
            if not seq:
                raise UserError(_("kecantikan.pasien sequence not found, please create kecantikan.pasien sequence"))
            self.name = seq.next_by_id()

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'