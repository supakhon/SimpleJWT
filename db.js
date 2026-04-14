const sqlite3 = require('sqlite3');
const { open } = require('sqlite');

async function createDB() {
    return open({
        filename: './users.db',
        driver: sqlite3.Database,
    });
}

module.exports = createDB;