from odoo import models, fields, api, _
from odoo.exceptions import UserError

class buku(models.Model):  # inherit dari Model -> ini nama class sesuai python
    _name = 'perpustakaan.buku'  # attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    _description = 'class untuk menyimpan daftar buku'

    # membuat attribute field
    name = fields.Char('Kode Buku', size=64, required=True, index=True, readonly=True,
                       default='new', states={})
    judul = fields.Char('Judul Buku', size=64, required=True, index=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    genre = fields.Char('Genre', size=64, required=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    pengarang_id = fields.Many2one('perpustakaan.pengarang', string="Pengarang", readonly=True,
                                   domain="[('state', '=', 'done')]", states={'draft': [('readonly', False)]})
    penerbit_id = fields.Many2one('perpustakaan.penerbit', string="Penerbit", readonly=True,
                                  domain="[('state', '=', 'done')]", states={'draft': [('readonly', False)]})
    tahun = fields.Char('Tahun Terbit', size=64, required=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    jumlah = fields.Integer('Jumlah', store=True, readonly=True, default=1, compute="_compute_active",
                            states={'draft': [('readonly', False)]})

    active = fields.Boolean('Active', default=True, readonly=True, states={'draft': [('readonly', False)]})
    date = fields.Date('Tanggal Input Data', default=fields.Date.context_today, readonly=True,
                       states={'draft': [('readonly', False)]})

    detailpinjam_id = fields.One2many('perpustakaan.detailpinjam', 'buku_id', domain="[('state', '=', 'done')]",
                                      states={'draft': [('readonly', False)]})

    kembali_id = fields.Many2one('perpustakaan.kembali', domain="[('state', '=', 'done')]",
                                 states={'draft': [('readonly', False)]})

    #active = fields.Boolean('Active', default=True, readonly=True, states={'draft': [('readonly', False)]})

    state = fields.Selection([('done', 'Done'),
                              ('draft', 'Draft'),
                              ('canceled', 'Canceled')], 'State', readonly=True, default='draft')

    _sql_constraints = [('name_unik', 'unique(name)', _('ID Buku sudah ada di database!')),
                        ('judul_unik', 'unique(judul)', _('Buku sudah ada di database!'))]

    def action_done(self):
        self.state = 'done'
        if self.name == 'new' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "perpustakaan.buku")])
            if not seq:
                raise UserError(_("perpustakaan.buku sequence not found, please create perpustakaan.buku sequence"))
            self.name = seq.next_by_id()

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.depends("detailpinjam_id.state", "kembali_id.state")
    def _compute_active(self):
        for s in self:
            if s.detailpinjam_id.state == 'done':
                s.jumlah=0
            elif s.kembali_id.state == 'done':
                s.jumlah=1


