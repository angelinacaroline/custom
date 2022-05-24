from odoo import models, fields, api, _
#from odoo yg digunakan adalah u working directory
#_ untuk translate

class detailkhs(models.Model):  #inherit dari Model -> ini nama class sesuai python
    _name = 'nilai.detailkhs'  #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    _description = 'class untuk menyimpan detail KHS mahasiswa'
    # _rec_name = 'name' #default-nya name, ini untuk memberi tahu field mana yang jadi rec_name.
    # _order = 'date desc'

    #membuat attribute field
    name = fields.Char('ID DetailKHS', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})

    khs_id = fields.Many2one('nilai.kahaes', string="KHS", readonly=True, ondelete="cascade",
                             domain="[('state', '=', 'done')]",
                             states={'draft': [('readonly', False)]})

    mk_id = fields.Many2one('nilai.matkul', string="MK", readonly=True, ondelete="cascade",
                            domain="[('state', '=', 'done'),('active', '=', 'true')]",
                            states={'draft': [('readonly', False)]})

    sksnya = fields.Integer('SKS MK', compute="_compute_sks", default=0, store=True, recursive=True)

    grade = fields.Selection(
        [('a', 'A'),
         ('bp', 'B+'),
         ('b', 'B'),
         ('cp', 'C+'),
         ('c', 'C'),
         ('d', 'D'),
         ('e', 'E')], required=True, readonly=True, states={'draft': [('readonly', False)]})


    total = fields.Float('Total', compute="_compute_total", default=0, store=True)

    date = fields.Date('Date Masuk', default=fields.Date.context_today, readonly=True,states={'draft': [('readonly', False)]})

    state = fields.Selection(
        [('done', 'Done'),
         ('draft', 'Draft'), ('canceled', 'Canceled')], 'State', readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')

    _sql_constraints = [('name_unik', 'unique(name)', _('Detail KHS already exist!'))]

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.depends('mk_id.sks', 'grade')
    def _compute_total(self):
        val = {
            "total": 0
        }
        for a in self:
            if a.grade == 'a':
                val["total"] = a.mk_id.sks * 4.0
            elif a.grade == 'bp':
                val["total"] = a.mk_id.sks * 3.5
            elif a.grade == 'b':
                val["total"] = a.mk_id.sks * 3.0
            elif a.grade == 'cp':
                val["total"] = a.mk_id.sks * 2.5
            elif a.grade == 'c':
                val["total"] = a.mk_id.sks * 2.0
            elif a.grade == 'd':
                val["total"] = a.mk_id.sks * 1.0
            elif a.grade == 'e':
                val["total"] = a.mk_id.sks * 0.0
        a.update(val)

    @api.depends('mk_id.sks')
    def _compute_sks(self):
        for s in self:
            s.sksnya = s.mk_id.sks