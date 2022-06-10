from odoo import models, fields, api, _
from odoo.exceptions import UserError

#MATERI YANG DIPAKAI : SEQUENCE (ID auto increment kalau d-delete nomor id tetap lanjut),
#                    : @API.DEPENDS (Buat create ID otomatis, Cek Tanggal),

class transaksi(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'kecantikan.transaksi' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk membuat daftar transaksi'

    #membuat attribute field

    name = fields.Char('ID Transaksi', size=64, required=True, index=True, readonly=True,
                       default='new', states={})

    appointment_id = fields.Many2one('kecantikan.janji', string="Kode Appointment", readonly=True, required=True,
                                    domain="[('state', '=', 'done')]",
                                    states={'draft': [('readonly', False)]})

    date_transaksi = fields.Date('Tanggal Transaksi', required=True, default=fields.Date.context_today, readonly=True,
                                 states={'draft': [('readonly', False)]})

    total_harga = fields.Integer('Total Harga', compute="_compute_harga", required=True, index=True, readonly=True,
                           states={})

    disc = fields.Integer('Diskon (%)', index=True, required=True, readonly=True, default='0',
                           states={'draft': [('readonly', False)]})

    total_harga2 = fields.Integer('Total Harus Dibayar', compute="_compute_harga2", store=True, required=True, index=True,
                                  readonly=True, states={'draft': [('readonly', False)]})

    state = fields.Selection(
        [('paid', 'Paid'),
         ('draft', 'Draft'),
         ('canceled', 'Canceled')], 'State', readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')

    date_janji = fields.Date('Tanggal Treatment', compute="_compute_tanggal", readonly=True, required=True, states={})

    staff_id = fields.Many2one('kecantikan.staff', string="Staff", readonly=True,
                               domain="[('state', '=', 'done'), ('active', '=', 'true')]",
                               states={'draft': [('readonly', False)]})

    _sql_constraints = [('name_unik', 'unique(name)', _('ID Transaksi Harus Unik!'))]

    def action_paid(self):  #treatment selesai & terbayar
        self.state = 'paid'
        if self.name == 'new' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "kecantikan.transaksi")])
            if not seq:
                raise UserError(_("kecantikan.transaksi sequence not found, please create kecantikan.transaksi sequence"))
            self.name = seq.next_by_id()

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.depends('appointment_id.name')
    def _compute_harga(self):
        for s in self:
            s.total_harga = s.appointment_id.total_harga

    @api.depends('appointment_id.name')
    def _compute_tanggal(self):
        for s in self:
            s.date_janji = s.appointment_id.date_janji

    @api.constrains('date_transaksi')
    def _check_date_transaksi(self):
        if self.date_transaksi != self.date_janji:
            raise UserError(_("Tanggal Transaksi Beda Dengan Tanggal Treatment."))

    @api.depends('appointment_id.name', 'disc')
    def _compute_harga2(self):
        for rec in self:
            val = {
                "total_harga2" : 0
            }
            val["total_harga2"] = rec.total_harga - ((rec.disc / 100) * rec.total_harga)
        rec.update(val)