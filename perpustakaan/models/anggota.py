from odoo import models, fields, api, _


class anggota(models.Model):  # inherit dari Model -> ini nama class sesuai python
    _name = 'perpustakaan.anggota'  # attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    _description = 'class untuk menyimpan daftar anggota perpustakaan'

    # membuat attribute field
    name = fields.Char('ID Anggota', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    member = fields.Char('Nama Anggota', size=64, required=True, readonly=True,
                         states={'draft': [('readonly', False)]})
    tgl_lahir = fields.Date('Tanggal Lahir', readonly=True, states={'draft': [('readonly', False)]})
    tgl_gabung = fields.Date('Tanggal Bergabung', default=fields.Date.context_today, readonly=True,
                             states={'draft': [('readonly', False)]})
    email = fields.Char('Email', size=64, required=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    telp = fields.Char('Nomor Telepon', size=64, required=True, readonly=True,
                       states={'draft': [('readonly', False)]})

    active = fields.Boolean('Active', default=True, readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([('done', 'Done'),
                              ('draft', 'Draft'),
                              ('canceled', 'Canceled')], 'State', readonly=True, default='draft')

    date = fields.Date('Tanggal Input Data', default=fields.Date.context_today, readonly=True,
                       states={'draft': [('readonly', False)]})

    pinjamm_id = fields.One2many('perpustakaan.pinjam', 'anggota_id', domain="[('state', '=', 'done')]",
                                 states={'draft': [('readonly', False)]})

    _sql_constraints = [('name_unik', 'unique(name)', _('Anggota Perpus sudah ada di database!'))]

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'
