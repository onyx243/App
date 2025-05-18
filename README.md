# PrintShop QR Uploader

Proof of concept for uploading print jobs via a unique QR code.

## Features
- Unique QR per shop linking to `/upload/:shopSlug`.
- JWT-based auth with `user`, `shopOwner`, `admin` roles.
- Upload images/docs (150 MB limit) to local `/uploads` or S3.
- E-mail notification and basic Socket.IO hooks.
- Simple React + Tailwind interface.

## Setup
### Backend (FastAPI)
```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # edit values
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

### Sample cURL
```bash
# signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H 'Content-Type: application/json' \
  -d '{"email":"a@b.com","password":"pass"}'

# login
curl -X POST http://localhost:8000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"a@b.com","password":"pass"}'
```

### Postman
Import `postman_collection.json` into Postman.
