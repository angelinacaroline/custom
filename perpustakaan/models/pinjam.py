from odoo import models, fields, api, _


class pinjam(models.Model):  # inherit dari Model -> ini nama class sesuai python
    _name = 'perpustakaan.pinjam'  # attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    _description = 'class untuk menyimpan daftar transaksi peminjaman buku'

    # membuat attribute field
    name = fields.Char('Kode Transaksi', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    anggota_id = fields.Many2one('perpustakaan.anggota', string="ID Anggota", readonly=True, required=True,
                                 domain="[('state', '=', 'done'),('active', '=', 'true')]",
                                 states={'draft': [('readonly', False)]})
    staff_id = fields.Many2one('perpustakaan.staff', string="ID Staff", readonly=True, required=True,
                               domain="[('state', '=', 'done'),('active', '=', 'true')]",
                               states={'draft': [('readonly', False)]})
    detail_id = fields.One2many('perpustakaan.detailpinjam', 'pinjam_id', domain="[('state', '=', 'done')]",
                                states={'draft': [('readonly', False)]})
    date = fields.Date('Tanggal Peminjaman', default=fields.Date.context_today, readonly=True, required=True,
                       states={'draft': [('readonly', False)]})
    tgl_kembali = fields.Date('Tanggal Pengembalian', readonly=True, required=True,
                              states={'draft': [('readonly', False)]})

    state = fields.Selection([('done', 'Done'),
                              ('draft', 'Draft'),
                              ('canceled', 'Canceled')], 'State', readonly=True, default='draft')

    kembali_id = fields.One2many('perpustakaan.kembali', 'pinjam_id', domain="[('state', '=', 'done')]",
                                states={'draft': [('readonly', False)]})

    _sql_constraints = [('name_unik', 'unique(name)', _('Transaksi sudah terekam di database!'))]

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'
