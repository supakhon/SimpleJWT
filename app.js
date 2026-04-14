const express = require('express');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const createDB = require('./db');
const app = express();

app.use(express.json());
app.use(express.static('public'));

const SECRET = 'mysecretkey'; // env ??

let db;

(async () => {
    db = await createDB();

    await db.exec(`
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            password TEXT
        )
    `);
})();

// Register
app.post('/register', async (req, res) => {
    const { name, password } = req.body;

    if (!name || !password) {
        return res.status(400).json({
            error: 'Missing Data'
        });
    }

    // Hash Password
    const hashedPassword = await bcrypt.hash(password, 10);

    const result = await db.run(
        'INSERT INTO users (name, password) VALUES (?, ?)',
        [name, hashedPassword]
    );

    res.status(201).json({
        id: result.lastID,
        name,
    });
});

// Login
app.post('/login', async (req, res) => {
    const { name, password } = req.body;

    const user = await db.get(
        'SELECT * FROM users WHERE name = ?',
        [name]
    );

    if (!user) {
        return res.status(401).json({error: 'User not found'});
    }

    // Compare password
    const isMatch = await bcrypt.compare(password, user.password);

    if (!isMatch) {
        return res.status(401).json({ error: 'Wrong password' });
    }

    // Create Token
    const token = jwt.sign(
        { id: user.id, name: user.name },
        SECRET,
        { expiresIn: '1h' },
    );

    res.json({ token });
});


// Middleware for Checking Token
const authMiddleware = (req, res, next) => {
    const authHeader = req.headers['authorization'];

    if (!authHeader) {
        return res.status(401).json({ error: 'No token' });
    }

    const token = authHeader.split(' ')[1];

    try {
        const decoded = jwt.verify(token, SECRET);
        req.user = decoded;
        next();
    } catch (err) {
        return res.status(403).json({ error: 'Invalid token' });
    }
}

// Protected Route
app.get('/profile', authMiddleware, (req, res) => {
    res.json({
        message: 'This is protected data',
        user: req.user,
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
