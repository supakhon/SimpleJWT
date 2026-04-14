const Datastore = require('nedb-promises');
const path = require('path');

const db = Datastore.create({ 
    filename: path.join(__dirname, 'users.db'), 
    autoload: true 
});

async function createDB() {
    return {
        exec: async () => {},
        run: async (query, params) => {
            const newUser = { name: params[0], password: params[1] };
            const doc = await db.insert(newUser);
            return { lastID: doc._id };
        },
        get: async (query, params) => {
            return await db.findOne({ name: params[0] });
        }
    };
}

module.exports = createDB;