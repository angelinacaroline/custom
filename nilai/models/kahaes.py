from odoo import models, fields, api, _
#from odoo yg digunakan adalah u working directory
#_ untuk translate

class kahaes(models.Model):  #inherit dari Model -> ini nama class sesuai python
    _name = 'nilai.kahaes'  #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    _description = 'class untuk menyimpan KHS mahasiswa'
    # _rec_name = 'name' #default-nya name, ini untuk memberi tahu field mana yang jadi rec_name.
    # _order = 'date desc'

    #membuat attribute field

    name = fields.Char('ID', compute="_compute_name", store=True, recursive=True)
    tahun = fields.Char('Tahun', size=64, required=True, index=True, readonly=True, default="2021/2022",
                      states={'draft': [('readonly', False)]})

    semester = fields.Selection(
        [('genap', 'Genap'),
         ('gasal', 'Gasal')], required=True,
        readonly=True,
        states={'draft': [('readonly', False)]})

    ips = fields.Float('IPS', compute="_compute_ips", default=0, store=True)

    mhs_id = fields.Many2one('nilai.mahasiswa', string="Mahasiswa", readonly=True, ondelete="cascade", states={'draft': [('readonly', False)]})
    detailkhs_id = fields.One2many('nilai.detailkhs', 'khs_id', domain="[('state', '=', 'done')]")

    date = fields.Date('Date Masuk', default=fields.Date.context_today, readonly=True,states={'draft': [('readonly', False)]})

    state = fields.Selection(
        [('done', 'Done'),
         ('draft', 'Draft'), ('canceled', 'Canceled')], 'State', readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')

    _sql_constraints = [('name_unik', 'unique(mhs_id, semester, tahun)', _('KHS already exist!'))]

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.depends('mhs_id', 'detailkhs_id')
    def _compute_ips(self):
        pass

    @api.depends('mhs_id.name', 'semester', 'tahun')
    def _compute_name(self):
        for s in self:
            s.name = "%s - %s - %s" % (s.mhs_id.name, s.semester, s.tahun)

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = list(args or [])
        if not (name == '' and operator == 'ilike'):
            args += [(self._rec_name, operator, name)]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)