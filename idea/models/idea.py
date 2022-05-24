from odoo import models, fields, api, _
#untuk translate

class idea(models.Model): #inherit dari Model
    _name = 'idea.idea'
    _description = 'class untuk berlatih ttg idea'
    #_rec_name = 'name' #yang keluar nanti kumpulan Nama
    #_order = 'date desc' #defaultnya adalah id, pengaruhnya saat List View

    #membuat attribute field
    name = fields.Char('Number', size=64, required=True, index=True, readonly=True, states={'draft' : [('readonly', False)]})
    date = fields.Date('Date Release', default=fields.Date.context_today, readonly=True, help='Please fill the date here')
    state = fields.Selection([('draft', 'Draft'), #draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
                              ('confirmed', 'Confirmed'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft') #tuple di dalam list, nama field harus state spy bisa diakses oleh states
    #Description is read-only whrn not draft!
    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})
    active = fields.Boolean('Active', default=True, readonly=True, states={'draft': [('readonly', False)]})
    confirm_date = fields.Date('Confirm date')
    #by convention, many2one fields en with '_id'
    confirm_partner_id = fields.Many2one('res.partner', 'Confirm By', readonly=True)

    #sponsor_ids = fields.Many2many('res.partner', 'ide_idea_res_partner_rel', 'idea_idea_id', 'res_partner_id', 'Sponsors')
    sponsor_ids = fields.Many2many('res.partner', string='Sponsors')

    score = fields.Integer('Score', default=0, readonly=True)
    owner = fields.Many2one('res.partner', 'Owner', index=True, readonly=True, states={'draft': [('readonly', False)]})

    voting_ids = fields.One2many('idea.voting', 'idea_id', string='Votes')
    total_yes = fields.Integer("Yes", compute="_compute_vote", store=True, default=0)
    total_no = fields.Integer("No", compute="_compute_vote", store=True, default=0)
    total_abstain = fields.Integer("Abstain", compute="_compute_vote", store=True, default=0)
    _sql_constraints = [('name_unik', 'unique(name)', _('Ideas must be unique!'))]

    @api.depends("voting_ids", "voting_ids.vote", "voting_ids.state")
    #function ini dijalankan jika record voting (voting_ids), berubah (new / delete),
    #atau saat vote (voting_ids.vote) berubah,
    #atau saat stave (voting_ids.state)
    #@api.depends("voting_ids", "voting_ids.vote", "voting_ids.state")
    #mirip dengan depends tapi ini perubahannya jk hanya melalui UI
    #klo ondepends bisa lwt phyton code ataupun UI, misal kita uat function automatic dari progeam
    #ini tidak bisa dihandle oleh onchange
    def _compute_vote (self):
        for idea in self.filtered(lambda i:i.state=='done'):
            val = {
                "total_yes": 0,
                "total_no": 0,
                "total_abstain": 0
            }
            for rec in idea.voting_ids.filtered(lambda s:s.state=='voted'):
                #lambda = on the fly function dari phyton
                #s ini = self dari voting_ids, fungsi filtered ini akan memfilter khusus yg voting_ids
                #bisa juga pakai looping tp lbh lama, jd sblm masuk loop dilakukan filter dlu
                if rec.vote == 'yes':
                    val["total_yes"] += 1
                elif rec.vote == 'no':
                    val["total_no"] += 1
                else:
                    val["total_abstain"] += 1
            idea.update(val) #utk update 1 record melalui phyton code hrs dlm bentuk dictionary

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'

    def tes_bookrent(self):
        print("ini di idea")
        t = self.env.context.get("keterangan")
        print(t)