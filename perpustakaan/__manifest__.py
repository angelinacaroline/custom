{
    'name': 'Perpustakaan',  # nama modul yg dibaca user di UI
    'version': '1.0',
    'author': 'Angelina',
    'summary': 'Modul Perpustakaan (Peminjaman & Pengembalian Buku)',  # deskripsi singkat dari modul
    'description': 'library management module',  # bisa nampilkan gambar/ deskripsi dalam bentuk html. html diletakkan
    # di idea/static/description, bisa kasi icon modul juga.
    'category': 'Latihan',
    'website': 'http://sib.petra.ac.id',
    'depends': ['base', 'sales_team'],  # list of dependencies, conditioning startup order
    'data': [
        'security/ir.model.access.csv',
        'views/buku_views.xml',
        'views/penerbit_views.xml',
        'views/pengarang_views.xml',
        'views/staff_views.xml',
        'views/anggota_views.xml',
        'views/pinjam_views.xml',
        'views/detailpinjam_views.xml',
        'views/kembali_views.xml',
        'data/ir_sequence_data.xml',
    ],
    'qweb': [],  # untuk memberi tahu static file, misal CSS
    'demo': [],  # demo data (for unit tests)
    'installable': True,
    'auto_install': False,  # indikasi install, saat buat database baru
}
