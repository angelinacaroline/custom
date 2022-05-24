{
    'name': 'Nilai',  #nama modul yg dibaca user di UI
    'version': '1.0',
    'author': 'Angelina',
    'summary': 'Modul Nilai SIB UK Petra', #deskripsi singkat dari modul
    'description': 'Nilai management module', #bisa nampilkan gambar/ deskripsi dalam bentuk html. html diletakkan
    #di idea/static/description, bisa kasi icon modul juga.
    'category': 'Latihan',
    'website': 'http://sib.petra.ac.id',
    'depends': ['base', 'sales_team'],  # list of dependencies, conditioning startup order
    'data': [
        'security/ir.model.access.csv',
        'views/mahasiswa_views.xml',
        'views/matkul_views.xml',
        'views/kahaes_views.xml',
        'views/detailkhs_views.xml',
        'views/kelas_views.xml',
        'wizard/wiz_nilai_kelas_views.xml',
        'data/ir_sequence_data.xml',
    ],
    'qweb':[],  #untuk memberi tahu static file, misal CSS
    'demo': [], #demo data (for unit tests)
    'installable': True,
    'auto_install': False,  # indikasi install, saat buat database baru
}