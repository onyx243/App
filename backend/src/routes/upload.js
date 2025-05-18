import express from 'express';
import multer from 'multer';
import AWS from 'aws-sdk';
import Upload from '../models/Upload.js';
import Shop from '../models/Shop.js';
import { sendUploadEmail } from '../utils/email.js';
import { io } from '../server.js';

const router = express.Router();

const storage = multer.diskStorage({
  destination: 'uploads',
  filename: (req, file, cb) => cb(null, `${Date.now()}-${file.originalname}`),
});
const upload = multer({ storage, limits: { fileSize: 150 * 1024 * 1024 } });

router.post('/:slug', upload.array('files'), async (req, res) => {
  const shop = await Shop.findOne({ slug: req.params.slug }).populate('owner');
  if (!shop) return res.status(404).json({ message: 'Shop not found' });

  let filePaths = req.files.map((f) => f.path);
  if (process.env.USE_S3 === 'true') {
    const s3 = new AWS.S3();
    const uploads = await Promise.all(req.files.map((file) => {
      const params = {
        Bucket: process.env.S3_BUCKET,
        Key: `${Date.now()}-${file.originalname}`,
        Body: file.buffer,
      };
      return s3.upload(params).promise();
    }));
    filePaths = uploads.map((u) => u.Location);
  }

  const uploadDoc = await Upload.create({
    shop: shop.id,
    user: req.user.id,
    files: filePaths,
  });

  sendUploadEmail(shop.owner.email, filePaths).catch(console.error);
  io.to(shop.owner.id).emit('new-upload', uploadDoc);

  res.json({ upload: uploadDoc });
});

export default router;
