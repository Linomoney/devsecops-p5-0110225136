# TaskManager — DevSecOps Pipeline Demo

> **Nama:** Tengku Erlangga Athallah | **NIM:** 0110225136  
> **Mata Kuliah:** DevSecOps | **Pertemuan:** 5

---

## 1. Nama Aplikasi & Fungsinya

**TaskManager** adalah aplikasi REST API berbasis Python/Flask yang menyediakan layanan manajemen tugas (_task management_). Pengguna dapat membuat, membaca, memperbarui, dan menghapus tugas (operasi CRUD penuh) melalui antarmuka HTTP JSON. Aplikasi ini menggunakan SQLite sebagai database dan dirancang dengan pola **Application Factory** serta **Service Layer** untuk memisahkan tanggung jawab (_separation of concerns_).

Fitur utama:
- ✅ CRUD lengkap untuk entitas **Task** (tugas)
- ✅ Manajemen **User** (pengguna)  
- ✅ Filter task berdasarkan status (`pending`, `in_progress`, `completed`) dan prioritas (`low`, `medium`, `high`)
- ✅ Endpoint _health check_ untuk monitoring
- ✅ Coverage unit test ≥70%

---

## 2. Bahasa & Framework

| Komponen        | Teknologi                          |
|-----------------|------------------------------------|
| Bahasa          | Python 3.12                        |
| Framework       | Flask 3.0.3                        |
| ORM Database    | Flask-SQLAlchemy 3.1.1 + SQLite    |
| Testing         | pytest + pytest-cov                |
| SAST Tool       | Bandit 1.8.0                       |
| CI/CD Platform  | GitHub Actions                     |

---

## 3. Cara Menjalankan Aplikasi

### Prasyarat
- Python 3.10+  
- pip

### Langkah Instalasi

```bash
# 1. Clone repository
git clone https://github.com/tengkuerlangga/devsecops-p5-0110225136.git
cd devsecops-p5-0110225136

# 2. Buat virtual environment (opsional namun dianjurkan)
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Jalankan aplikasi
python run.py
```

Aplikasi akan berjalan di `http://localhost:5000`.

### Contoh Penggunaan API

```bash
# Health check
curl http://localhost:5000/health

# Buat task baru
curl -X POST http://localhost:5000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Belajar DevSecOps", "priority": "high"}'

# Ambil semua task
curl http://localhost:5000/api/tasks/

# Filter task selesai
curl http://localhost:5000/api/tasks/?status=completed
```

### Menjalankan Unit Test

```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

---

## 4. Overview Pipeline CI/CD (DevSecOps)

Pipeline diimplementasikan menggunakan **GitHub Actions** dan terdapat dalam file `.github/workflows/devsecops.yml`. Pipeline terpicu secara otomatis pada setiap **push** dan **pull request** ke branch `main`.

```
PUSH / PR ke main
       │
       ▼
┌──────────────────────────────┐
│  JOB 1: build                │
│  • Checkout code             │
│  • Setup Python 3.12         │
│  • pip install -r req.txt    │
│  • pytest + coverage ≥70%   │
│  • Upload coverage artifact  │
└──────────────┬───────────────┘
               │  needs: build
               ▼
┌──────────────────────────────┐
│  JOB 2: sast-scan            │
│  • Checkout code             │
│  • Install Bandit            │
│  • bandit -r app/ → JSON     │
│  • Upload Bandit report      │
│  • Quality Gate:             │
│    ✗ HIGH severity → FAIL    │
│    ✓ No HIGH → PASS          │
└──────────────────────────────┘
```

### Komponen Pipeline

| Tahap          | Tool/Action            | Tujuan                                          |
|----------------|------------------------|-------------------------------------------------|
| Checkout       | `actions/checkout@v4`  | Mengambil source code dari repository           |
| Build          | `actions/setup-python` | Menyiapkan runtime Python 3.12                  |
| Unit Test      | pytest + pytest-cov    | Menjalankan test & memastikan coverage ≥70%     |
| SAST Scan      | Bandit                 | Analisis statis keamanan source code Python     |
| Quality Gate   | Custom Python Script   | Menggagalkan pipeline jika ada isu HIGH severity|
| Artifact Store | `actions/upload-artifact` | Menyimpan laporan coverage & Bandit          |

---

## 5. Struktur File

```
devsecops-p5-0110225136/
├── .github/
│   └── workflows/
│       └── devsecops.yml    # GitHub Actions workflow
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Konfigurasi (dev/test/prod)
│   ├── database.py          # Model SQLAlchemy (Task, User)
│   ├── routes.py            # Blueprint & REST endpoints
│   └── services.py          # Business logic / service layer
├── tests/
│   └── test_app.py          # Unit tests (15+ test cases)
├── run.py                   # Entry point aplikasi
├── requirements.txt         # Daftar dependensi Python
└── README.md                # Dokumentasi ini
```

---

*Dibuat untuk keperluan tugas Pertemuan 5 mata kuliah DevSecOps.*
