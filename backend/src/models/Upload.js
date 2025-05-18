import mongoose from 'mongoose';

const uploadSchema = new mongoose.Schema({
  shop: { type: mongoose.Schema.Types.ObjectId, ref: 'Shop', required: true },
  user: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  files: [String],
  createdAt: { type: Date, default: Date.now },
  printed: { type: Boolean, default: false },
});

export default mongoose.model('Upload', uploadSchema);
