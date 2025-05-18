import mongoose from 'mongoose';
import { createServer } from 'http';
import { Server as SocketIO } from 'socket.io';
import app from './app.js';

const httpServer = createServer(app);
export const io = new SocketIO(httpServer, {
  cors: { origin: '*' },
});

io.on('connection', (socket) => {
  const { userId } = socket.handshake.query;
  if (userId) socket.join(userId);
});

const PORT = process.env.PORT || 3001;

if (process.env.NODE_ENV !== 'test') {
  mongoose.connect(process.env.MONGODB_URI)
    .then(() => {
      httpServer.listen(PORT, () => {
        console.log(`Server running on port ${PORT}`);
      });
    })
    .catch((err) => console.error('MongoDB connection error', err));
}

export default app;
