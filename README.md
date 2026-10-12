# TaskTracker - DevSecOps Pipeline (Praktikum 5)

![DevSecOps Pipeline](https://github.com/Linomoney/devsecops-p5-0110225136/actions/workflows/devsecops.yml/badge.svg)

## 1. Nama Aplikasi & Fungsinya
**TaskTracker** adalah REST API sederhana untuk mengelola daftar tugas (to-do list).
Pengguna dapat membuat, melihat, mengubah, menghapus, dan memfilter tugas berdasarkan
status (`todo`, `in_progress`, `done`) serta melihat ringkasan jumlah tugas.

| Method | Endpoint        | Fungsi                                   |
|--------|-----------------|------------------------------------------|
| GET    | `/health`       | Cek kesehatan aplikasi                   |
| GET    | `/tasks`        | Daftar tugas (opsional `?status=done`)   |
| POST   | `/tasks`        | Buat tugas baru                          |
| GET    | `/tasks/<id>`   | Detail satu tugas                        |
| PUT    | `/tasks/<id>`   | Ubah tugas                               |
| DELETE | `/tasks/<id>`   | Hapus tugas                              |
| GET    | `/summary`      | Ringkasan jumlah tugas per status        |

## 2. Bahasa / Framework
- **Python 3.12**
- **Flask 3** (web framework)
- **unittest/pytest + pytest-cov** (pengujian & coverage)
- **Bandit** (SAST untuk Python)

Struktur source code:
```
app/__init__.py     # application factory
app/models.py       # model data Task
app/storage.py      # repository in-memory
app/validators.py   # validasi input
app/utils.py        # helper (kode tugas, ringkasan)
app/routes.py       # endpoint REST API
tests/              # unit test
run.py              # entry point
```

## 3. Cara Menjalankan Aplikasi
```bash
git clone https://github.com/Linomoney/devsecops-p5-0110225136.git
cd devsecops-p5-NIM

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

python run.py                    # aplikasi berjalan di http://127.0.0.1:5000
```
Contoh penggunaan:
```bash
curl -X POST http://127.0.0.1:5000/tasks \
     -H "Content-Type: application/json" \
     -d '{"title": "Belajar DevSecOps", "priority": "high"}'
curl http://127.0.0.1:5000/tasks
```
Menjalankan test:
```bash
pytest --cov=app --cov-report=term-missing
```

## 4. Overview Pipeline CI/CD
Pipeline didefinisikan di `.github/workflows/devsecops.yml` dan berjalan otomatis pada
**push** dan **pull request** ke branch `main`, memakai runner `ubuntu-latest`.

```
push / pull_request (main)
          |
          v
  [ Job 1: build ]  -->  [ Job 2: sast-scan ]   (needs: build)
   - checkout             - checkout
   - setup Python         - install Bandit
   - install deps         - generate report (JSON + TXT)
   - unit test            - upload artifact
   - coverage gate >= 80% - QUALITY GATE: gagal jika ada temuan Medium/High
```

**Quality Gate**
1. Coverage unit test minimal **80%** (`--cov-fail-under=80`).
2. Bandit tidak boleh menemukan kerentanan berseverity **Medium atau High**.
   Temuan *Low* dilaporkan tetapi tidak menggagalkan pipeline.

Laporan Bandit tersedia sebagai artifact `bandit-reports` pada setiap run.
