import express from 'express';
import cors from 'cors';
import mongoose from 'mongoose';
import dotenv from 'dotenv';
import { createServer } from 'http';
import { Server as SocketIO } from 'socket.io';
import authRoutes from './routes/auth.js';
import uploadRoutes from './routes/upload.js';
import dashboardRoutes from './routes/dashboard.js';
import shopRoutes from './routes/shops.js';
import { authMiddleware } from './middleware/auth.js';

dotenv.config();

const app = express();
const httpServer = createServer(app);
export const io = new SocketIO(httpServer, {
  cors: { origin: '*' },
});

io.on('connection', (socket) => {
  const { userId } = socket.handshake.query;
  if (userId) socket.join(userId);
});

app.use(cors());
app.use(express.json());
app.use('/uploads', express.static('uploads'));

app.use('/api/auth', authRoutes);
app.use('/api/shops', shopRoutes);
app.use('/api/upload', authMiddleware, uploadRoutes);
app.use('/api/dashboard', authMiddleware, dashboardRoutes);

const PORT = process.env.PORT || 3001;
mongoose.connect(process.env.MONGODB_URI)
  .then(() => {
    httpServer.listen(PORT, () => {
      console.log(`Server running on port ${PORT}`);
    });
  })
  .catch((err) => console.error('MongoDB connection error', err));
