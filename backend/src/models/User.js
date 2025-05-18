import mongoose from 'mongoose';
import bcrypt from 'bcrypt';

const userSchema = new mongoose.Schema({
  email: { type: String, unique: true, required: true },
  password: { type: String, required: true },
  role: { type: String, enum: ['user', 'shopOwner', 'admin'], default: 'user' },
  shop: { type: mongoose.Schema.Types.ObjectId, ref: 'Shop' },
});

userSchema.pre('save', async function hashPassword(next) {
  if (!this.isModified('password')) return next();
  this.password = await bcrypt.hash(this.password, 10);
  return next();
});

userSchema.methods.comparePassword = function compare(pw) {
  return bcrypt.compare(pw, this.password);
};

export default mongoose.model('User', userSchema);
