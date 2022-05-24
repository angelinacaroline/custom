from odoo import models, fields, api, _


class detailpinjam(models.Model):  # inherit dari Model -> ini nama class sesuai python
    _name = 'perpustakaan.detailpinjam'  # attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    _description = 'class untuk menyimpan daftar detail transaksi peminjaman'

    # membuat attribute field
    name = fields.Char('ID Detail Peminjaman', compute="_compute_name", store=True, recursive=True)
    buku_id = fields.Many2one('perpustakaan.buku', string="Kode Buku", readonly=True,
                              domain="[('state', '=', 'done'),('active', '=', 'true'),('jumlah', '>', '0')]",
                              states={'draft': [('readonly', False)]})
    jumlah = fields.Integer('Jumlah yang Dipinjam', readonly=True, required=True, default=1,
                            states={'draft': [('readonly', False)]})

    pinjam_id = fields.Many2one('perpustakaan.pinjam', string="Kode Transaksi", readonly=True,
                                domain="[('state', '=', 'done')]",
                                states={'draft': [('readonly', False)]})

    state = fields.Selection([('done', 'Done'),
                              ('draft', 'Draft'),
                              ('canceled', 'Canceled')], 'State', readonly=True, default='draft')

    date = fields.Date(default=fields.Date.context_today, readonly=True,
                       states={'draft': [('readonly', False)]})

    _sql_constraints = [('name_unik', 'unique(name)', _('Detail Transaksi sudah terekam di database!'))]

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.depends('buku_id.name', 'pinjam_id.name')
    def _compute_name(self):
        for s in self:
            s.name = "%s - %s- %s" % (s.pinjam_id.anggota_id.name, s.pinjam_id.name, s.buku_id.judul)
