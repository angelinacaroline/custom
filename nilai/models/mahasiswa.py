from odoo import models, fields, api, _
#from odoo yg digunakan adalah u working directory
#_ untuk translate

class mahasiswa(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'nilai.mahasiswa' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk membuat daftar mahasiswa'
    # _rec_name = 'name' #default-nya name, ini untuk memberi tahu field mana yang jadi rec_name.
    # _order = 'date desc'

    #membuat attribute field

    name = fields.Char('NRP', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    nama_mhs = fields.Char('Nama', size=64, required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})

    status = fields.Selection(
        [('aktif', 'Aktif'),  # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
         ('cuti', 'Cuti'),
         ('do', 'DO'),
         ('lulus', 'Lulus')], required=True,
        readonly=True,
        states={'draft': [('readonly', False)]})

    ipk = fields.Char('IPK', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})

    date = fields.Date('Date Masuk', default=fields.Date.context_today, readonly=True,states={'draft': [('readonly', False)]})

    state = fields.Selection(
        [('done', 'Done'),
         ('draft', 'Draft'), ('canceled', 'Canceled')], 'State', readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')

    #khs_ids = fields.One2many('nilai.khss', 'khs_id', string="KHS")

    _sql_constraints = [('name_unik', 'unique(name)', _('NRP must be unique!'))]

    def action_done(self):  #approve
        self.state = 'done'
        t = self.env.context
        print(t.get('keterangan'))

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    def action_tes(self):
        #contoh ambil active user
        print(self.env.user.name)

        #contoh ambil active company
        print(self.env.company.name)

        #contoh common orm method search
        a = self.env["res.partner"].search([('name', 'ilike', 'Gemini')])
        for rec in a:
            print(rec.name)

        a = self.env["res.partner"].search([], limit=2)

        #contoh context
        print(self.env.context.get('lang'))

        t = self.env.context.copy()
        t["keterangan"] = 'Ideku'
        self.with_context(t).action_done()

        b = self.env["idea.idea"]
        b.with_context(t).tes_bookrent()

        #contoh query select
        query = "select name from res_partner order by name desc limit 3"
        self.env.cr.execute(query)
        res = self .env.cr.fetchall()
        for data in res:
            print(data[0])

        #contoh query update

        #contoh untuk delete

        #contoh browse
        #query = "select * from res_partner limit 3"
        #res = self.env['res_partner'].browse([row[0] for row in self.env.cr.fetchall()])
        #for rec in res:
        #    print(rec.name)

        #contoh serach

