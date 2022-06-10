{
    'name': 'Studio Kecantikan',  #nama modul yg dibaca user di UI
    'version': '1.0',
    'author': 'Angelina',
    'summary': 'Modul Studio Kecantikan', #deskripsi singkat dari modul
    'description': 'beauty studio management module', #bisa nampilkan gambar/ deskripsi dalam bentuk html. html diletakkan
    #di idea/static/description, bisa kasi icon modul juga.
    'category': 'Latihan',
    'website': 'http://sib.petra.ac.id',
    'depends': ['base', 'sales_team'],  # list of dependencies, conditioning startup order
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/pasien_views.xml',
        'views/staff_views.xml',
        'views/beautician_views.xml',
        'views/kategori_views.xml',
        'views/treatment_views.xml',
        'views/janji_views.xml',
        'views/djanji_views.xml',
        'views/transaksi_views.xml',
        # #'views/inheritance_views.xml',
        'wizard/wiz_kecantikan_transaksi.xml',
    ],
    'qweb':[],  #untuk memberi tahu static file, misal CSS
    'demo': [], #demo data (for unit tests)
    'installable': True,
    'auto_install': False,  # indikasi install, saat buat database baru
}