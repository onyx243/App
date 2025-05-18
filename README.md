# PrintShop QR Uploader

Proof of concept for uploading print jobs to a photo/cyber café via a unique QR code.

## Features
- Unique QR per shop linking to `/upload/:shopSlug`.
- JWT-based auth with `user`, `shopOwner`, `admin` roles.
- Upload images/docs (150 MB limit) to local `/uploads` or S3.
- Real-time dashboard notifications with Socket.io and e-mail alerts.
- Simple React + Tailwind interface.

## Setup
### Backend
```bash
cd backend
npm install
cp .env.example .env # edit values
npm run dev
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
curl -X POST http://localhost:3001/api/auth/signup \
  -H 'Content-Type: application/json' \
  -d '{"email":"a@b.com","password":"pass"}'

# login
curl -X POST http://localhost:3001/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"a@b.com","password":"pass"}'
```

### Postman
Import `postman_collection.json` into Postman.
