let isLoginMode = true;

// สลับหน้าจอระหว่าง Login และ Register
function toggleForm() {
    isLoginMode = !isLoginMode;
    const title = document.getElementById('form-title');
    const link = document.getElementById('toggle-link');
    const btn = document.getElementById('main-btn');

    if (isLoginMode) {
        title.innerText = 'เข้าสู่ระบบ';
        btn.innerText = 'ตกลง';
        link.innerText = 'ยังไม่มีบัญชี? สมัครสมาชิก';
    } else {
        title.innerText = 'สมัครสมาชิก';
        btn.innerText = 'สมัครสมาชิก';
        link.innerText = 'มีบัญชีอยู่แล้ว? เข้าสู่ระบบ';
    }
}

// จัดการการส่งข้อมูล API
async function handleAuth() {
    const name = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!name || !password) return alert('กรุณากรอกข้อมูลให้ครบ');

    const endpoint = isLoginMode ? '/login' : '/register';

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, password })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'เกิดข้อผิดพลาด');
        }

        if (isLoginMode) {
            // เก็บ Token ลง localStorage
            localStorage.setItem('token', data.token);
            loadProfile();
        } else {
            alert('สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ');
            toggleForm();
        }
    } catch (err) {
        alert(err.message);
    }
}

// ดึงข้อมูล Profile โดยใช้ Token
async function loadProfile() {
    const token = localStorage.getItem('token');
    if (!token) return;

    try {
        const response = await fetch('/profile', {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('auth-section').style.display = 'none';
            document.getElementById('profile-section').style.display = 'block';
            document.getElementById('user-id').innerText = data.user.id;
            document.getElementById('user-name').innerText = data.user.name;
        } else {
            logout();
        }
    } catch (err) {
        logout();
    }
}

function logout() {
    localStorage.removeItem('token');
    location.reload();
}

// ตรวจสอบสถานะเมื่อเปิดหน้าเว็บ
window.onload = () => {
    if (localStorage.getItem('token')) {
        loadProfile();
    }
};