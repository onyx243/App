import express from 'express';
import Upload from '../models/Upload.js';
import { roleMiddleware } from '../middleware/auth.js';

const router = express.Router();

router.get('/', roleMiddleware(['shopOwner']), async (req, res) => {
  const uploads = await Upload.find({ shop: req.user.shop, printed: false })
    .populate('user', 'email')
    .sort({ createdAt: -1 });
  res.json({ uploads });
});

router.patch('/:id/printed', roleMiddleware(['shopOwner']), async (req, res) => {
  const upload = await Upload.findByIdAndUpdate(req.params.id, { printed: true }, { new: true });
  res.json({ upload });
});

router.delete('/:id', roleMiddleware(['shopOwner']), async (req, res) => {
  await Upload.findByIdAndDelete(req.params.id);
  res.status(204).end();
});

export default router;
