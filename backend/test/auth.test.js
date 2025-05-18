import request from 'supertest';
import mongoose from 'mongoose';
import dotenv from 'dotenv';
import app from '../src/app.js';

dotenv.config({ path: '.env.test', override: true });

beforeAll(async () => {
  await mongoose.connect(process.env.MONGODB_URI);
});

afterAll(async () => {
  await mongoose.disconnect();
});

describe('Auth', () => {
  test('signup and login', async () => {
    const email = `test${Date.now()}@example.com`;
    const password = 'pass123';
    const signup = await request(app).post('/api/auth/signup').send({ email, password });
    expect(signup.status).toBe(200);
    const login = await request(app).post('/api/auth/login').send({ email, password });
    expect(login.body.token).toBeTruthy();
  });
});
