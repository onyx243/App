import QRCode from 'qrcode';

export const generateShopQr = async (shopSlug) => {
  const url = `${process.env.BASE_URL}/upload/${shopSlug}`;
  return QRCode.toDataURL(url);
};
