from odoo import models, fields, api, _


class kembali(models.Model):  # inherit dari Model -> ini nama class sesuai python
    _name = 'perpustakaan.kembali'  # attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    _description = 'class untuk menyimpan daftar transaksi pengembalian buku'

    # membuat attribute field
    name = fields.Char('Kode Pengambalian', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})

    pinjam_id = fields.Many2one('perpustakaan.pinjam', string="ID Peminjaman", domain="[('state', '=', 'done')]",
                                states={'draft': [('readonly', False)]})

    staff_id = fields.Many2one('perpustakaan.staff', string="ID Staff", readonly=True, required=True,
                               domain="[('state', '=', 'done'),('active', '=', 'true')]",
                               states={'draft': [('readonly', False)]})

    tgl_sekarang = fields.Date('Tanggal Harus Kembali', compute="_compute_date", readonly=True, required=True,
                               states={'draft': [('readonly', False)]})

    tgl_kembali = fields.Date('Tanggal Pengembalian', default=fields.Date.context_today, required=True,
                              readonly=True, states={'draft': [('readonly', False)]})

    denda = fields.Selection(
        [('none', 'Tidak Ada'),
         ('terlambat', 'Terlambat'),
         # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
         ('rusak', 'Rusak'),
         ('hilang', 'Hilang')], required=True, readonly=True,
        states={'draft': [('readonly', False)]})

    tarif = fields.Integer('Tarif Denda', readonly=True, required=True, default=0,
                           states={'draft': [('readonly', False)]})

    buku_id = fields.One2many('perpustakaan.buku', 'kembali_id', domain="[('state', '=', 'done')]",
                                      states={'draft': [('readonly', False)]})

    state = fields.Selection([('done', 'Done'),
                              ('draft', 'Draft'),
                              ('canceled', 'Canceled')], 'State', readonly=True, default='draft')

    _sql_constraints = [('name_unik', 'unique(name)', _('Transaksi sudah terekam di database!')),
                        ('pinjam_id_unik', 'unique(pinjam_id)', _('Transaksi Pengembalian sudah ada di database!'))]

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.depends('name', 'pinjam_id', 'pinjam_id.name')
    def _compute_date(self):
        for s in self:
            s.tgl_sekarang = s.pinjam_id.tgl_kembali
