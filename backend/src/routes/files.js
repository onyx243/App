import express from 'express';
import path from 'path';
import { authMiddleware, roleMiddleware } from '../middleware/auth.js';

const router = express.Router();

const uploadsDir = path.resolve('uploads');

router.get('/:filename', authMiddleware, roleMiddleware(['shopOwner']), (req, res) => {
  const filePath = path.join(uploadsDir, path.basename(req.params.filename));
  res.sendFile(filePath, (err) => {
    if (err) res.status(404).end();
  });
});

export default router;
