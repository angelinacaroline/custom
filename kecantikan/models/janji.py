from odoo import models, fields, api, _
from odoo.exceptions import UserError

#MATERI YANG DIPAKAI : SEQUENCE (ID auto increment kalau d-delete nomor id tetap lanjut),
#                    : @API.DEPENDS (Buat create ID otomatis, Cek Tanggal),
#                    : WIZARD (Sekadar untuk melihat detail dari appointment yang dibuat, menggantikan Detail Appointment Views,

class janji(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'kecantikan.janji' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk membuat daftar janji'

    #membuat attribute field

    name = fields.Char('ID Appointment', compute="_compute_name", store=True, recursive=True)

    pasien_id = fields.Many2one('kecantikan.pasien', string="Pelanggan", readonly=True, required=True,
                                domain="[('state', '=', 'done')]",
                                states={'draft': [('readonly', False)]})

    staff_id = fields.Many2one('kecantikan.staff', string="Staff", readonly=True, required=True,
                                domain="[('state', '=', 'done'), ('active', '=', 'true')]",
                                states={'draft': [('readonly', False)]})

    date_janji = fields.Date('Tanggal', readonly=True, required=True,
                             states={'draft': [('readonly', False)]})

    time = fields.Selection(
            [('08:00', '08:00'),
            ('11:00', '11:00'),
            ('14:00', '14:00'),
            ('17:00', '17:00'),],
            string="Jam", required=True, readonly=True, states={'draft': [('readonly', False)]})

    date_create = fields.Date('Tanggal Create Data', required=True, default=fields.Date.context_today, readonly=True,
                              states={})

    state = fields.Selection(
        [('done', 'Done'),
         ('draft', 'Draft'),
         ('canceled', 'Canceled')], 'State', readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')

    detail_id = fields.One2many('kecantikan.djanji', 'janji_id', domain="[('state', '=', 'done')]",
                                states={'draft': [('readonly', False)]})

    total_harga = fields.Integer('Total Harga', compute="_compute_total", required=True, index=True, readonly=True,
                                 default='0', states={'draft': [('readonly', False)]})

    _sql_constraints = [('name_unik', 'unique(name)', _('ID Janji Harus Unik!'))]

    def action_done(self):  #approve
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    #Buat passing isi saja
    @api.depends('pasien_id.name', 'date_janji', 'time')
    def _compute_name(self):
        for s in self:
            s.name = "%s / %s / %s" % (s.pasien_id.nama_pasien, s.date_janji, s.time)

    #Constraint buat cek tanggal appointment harus lebih dari hari ini
    @api.constrains('date_janji')
    def _check_date_janji(self):
        if self.date_janji <= self.date_create:
            raise UserError(_("Tanggal Appointment Harus Setelah Hari Ini."))

    #Cek apakah appointment untuk tanggal dan jam yang dipilih masih ada slot (5 slot)
    @api.constrains('date_janji', 'time')
    def _check_appointment(self):
        cjam = 0
        for rec in self:
            cjam = self.env['kecantikan.janji'].search_count([('time', '=', rec.time),
                                                              ('date_janji', '=', rec.date_janji)])
            if cjam > 5:
                raise UserError(_("Jadwal yang dipilih sudah penuh."))

    #Wizard
    def action_wiz_djanji(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Wizard Appointment & Details'),
            'res_model': 'wiz.kecantikan.janji',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }

    #Hitung total harga berdasarkan janji treatment
    @api.depends('detail_id.name')
    def _compute_total(self):
        for total in self:
            total_harga = 0
            for line in total.detail_id:
                total_harga += line.harga
            total.update({
                'total_harga': total_harga,
            })