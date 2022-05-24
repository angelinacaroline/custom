from odoo import models, fields, api, _
#from odoo yg digunakan adalah u working directory
#_ untuk translate

class matkul(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'nilai.matkul' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    _description = 'class untuk membuat daftar mata kuliah'
    # _rec_name = 'name' #default-nya name, ini untuk memberi tahu field mana yang jadi rec_name.
    # _order = 'date desc'

    #membuat attribute field

    name = fields.Char('Kode MK', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    nama_mk = fields.Char('Nama MK', size=64, required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})

    sks = fields.Integer('SKS', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})

    date = fields.Date('Date Masuk', default=fields.Date.context_today, readonly=True,states={'draft': [('readonly', False)]})
    active = fields.Boolean('Active', default=True, readonly=True, states={'draft': [('readonly', False)]})

    state = fields.Selection(
        [('done', 'Done'),
         ('draft', 'Draft'), ('canceled', 'Canceled')], 'State', readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')

    _sql_constraints = [('name_unik', 'unique(name)', _('Kode MK must be unique!'))]

    def action_done(self):  #approve
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'