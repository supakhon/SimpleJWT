const sqlite3 = require('sqlite3');
const { open } = require('sqlite');
const path = require('path');

async function createDB() {
    return open({
        filename: path.join(__dirname, 'users.db'),
        driver: sqlite3.Database,
    });
}

module.exports = createDB;