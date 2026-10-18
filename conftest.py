"""
conftest.py — Konfigurasi pytest untuk seluruh project.
Memastikan root project ada di sys.path sehingga 'from app import ...' bekerja
baik saat dijalankan lokal maupun di GitHub Actions (CI environment).
"""
import sys
import os

# Tambahkan direktori root project ke Python path
sys.path.insert(0, os.path.dirname(__file__))
