import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import authRoutes from './routes/auth.js';
import uploadRoutes from './routes/upload.js';
import dashboardRoutes from './routes/dashboard.js';
import shopRoutes from './routes/shops.js';
import filesRoutes from './routes/files.js';
import { authMiddleware } from './middleware/auth.js';

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

app.use('/api/auth', authRoutes);
app.use('/api/shops', shopRoutes);
app.use('/api/upload', authMiddleware, uploadRoutes);
app.use('/api/dashboard', authMiddleware, dashboardRoutes);
app.use('/api/files', filesRoutes);

export default app;
