from odoo import models, fields, api, _
#untuk translate

class voting(models.Model): #inherit dari Model
    _name = 'idea.voting'
    _description = 'class untuk berlatih ttg voting sebuah idea'
    #_rec_name = 'name' #yang keluar nanti kumpulan Nama
    #_order = 'date desc' #defaultnya adalah id, pengaruhnya saat List View

    #membuat attribute field
    name = fields.Char('Number', size=64, required=True, index=True, readonly=True, states={'draft' : [('readonly', False)]})
    date = fields.Date('Date Release', default=fields.Date.context_today, readonly=True, help='Please fill the date here')

    state = fields.Selection([('draft', 'Draft'),  # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
                             ('voted', 'Voted'),
                             ('canceled', 'Canceled')], 'State', readonly=True, default='draft')

    vote = fields.Selection([('yes', 'Yes'), #draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
                              ('no', 'No'),
                              ('abstain', 'Abstain')], required=True,
                            readonly=True,
                            states={'draft':[('readonly', False)]}) #tuple di dalam list, nama field harus state spy bisa diakses oleh states

    voter_id = fields.Many2one('res.users', 'Voted By', readonly=True, ondelete="cascade", default=lambda self: self.env.user)
    idea_id = fields.Many2one('idea.idea', string='Idea', readonly=True, ondelete="cascade",
                              states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done'),('active', '=', 'true')]")

    #field ini adalah related field, merefer ke date yg ada di model idea_idea, sifatnya readonly
    #field ini tdk meng-cretae field baru di tabel, jk mau disimpan, berikan atribute store=True
    #related field yg store = false tdk bisa di sort, group by
    idea_date = fields.Date("Idea date", related='idea_id.date')

    #ondelete="restrict" jika master tidak boleh dihapus
    #ondelete="default" jika master dihapus maka menjadi null di database / false di phyton
    def action_voted(self):
        self.state = 'voted'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'