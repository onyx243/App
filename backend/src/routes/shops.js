import express from 'express';
import { roleMiddleware } from '../middleware/auth.js';
import Shop from '../models/Shop.js';
import User from '../models/User.js';
import { generateShopQr } from '../utils/qrcode.js';

const router = express.Router();

router.post('/', roleMiddleware(['admin']), async (req, res) => {
  const shop = await Shop.create({ ...req.body, owner: req.body.ownerId });
  await User.findByIdAndUpdate(req.body.ownerId, { shop: shop.id, role: 'shopOwner' });
  const qr = await generateShopQr(shop.slug);
  res.json({ shop, qr });
});

router.get('/:slug/qr', async (req, res) => {
  const shop = await Shop.findOne({ slug: req.params.slug });
  if (!shop) return res.status(404).json({ message: 'Not found' });
  const qr = await generateShopQr(shop.slug);
  return res.json({ qr });
});

export default router;
