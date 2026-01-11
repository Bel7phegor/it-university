const mongoose = require('mongoose');
const Character = require('./models/Character');

// Kết nối MongoDB
const url = 'mongodb://127.0.0.1:27017/street-fighters';
mongoose.connect(url, { useNewUrlParser: true, useUnifiedTopology: true });

// Xử lý sự kiện kết nối
const db = mongoose.connection;
db.on('error', console.error.bind(console, 'Connection error:'));
db.once('open', async () => {
  console.log('Connected to MongoDB');

  try {
    // Xóa toàn bộ dữ liệu cũ để đảm bảo tính unique
    await Character.deleteMany({});
    console.log('Cleared existing characters');

    // Tạo và lưu nhân vật Ryu
    const ryu = new Character({
      name: 'Ryu',
      ultimate: 'Shinku Hadoken'
    });
    const savedRyu = await ryu.save();
    console.log('Saved character:', savedRyu);

    // Thử tạo nhân vật trùng tên (sẽ gây lỗi)
    try {
      const duplicateRyu = new Character({
        name: 'Ryu', // Trùng tên!
        ultimate: 'Hadoken'
      });
      await duplicateRyu.save();
    } catch (err) {
      console.error('Error (expected):', err.message); // Lỗi unique
    }

    // Tạo nhân vật mới không trùng tên
    const ken = new Character({
      name: 'Ken',
      ultimate: 'Shoryuken'
    });
    const savedKen = await ken.save();
    console.log('Saved character:', savedKen);

  } catch (err) {
    console.error('Unexpected error:', err);
  } finally {
    mongoose.disconnect(); // Ngắt kết nối sau khi hoàn thành
  }
});
