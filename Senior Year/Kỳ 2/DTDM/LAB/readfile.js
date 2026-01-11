const fs = require('fs');
const path = './Data.md';
fs.access(path, fs.F_OK, (err) => {
    if (err) {
        console.error(err);
        return;
    }
    console.log("File ok")
});