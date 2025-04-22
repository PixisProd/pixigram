const form = document.getElementById('registrationForm');
const errorDiv = document.getElementById('error');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  errorDiv.textContent = '';


  const formData = new FormData(form);
  const password = formData.get('password')
  const confirm_password = formData.get('password_confirm')
  if (password != confirm_password) {
    errorDiv.textContent = 'Passwords do not match';
    return;
  }

  const data = {
    login: formData.get('login'),
    password: formData.get('password'),
    username: formData.get('username'),
    email: formData.get('email'),
  };

  try {
    const response = await fetch('http://localhost:8000/auth/registration', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data),
    });
    if (response.ok) {
      window.location.href = '/login';
    } else {
      const resData = response.json();
      errorDiv.textContent = resData.detail;
    }
  } catch (error) {
    errorDiv.textContent = 'Something went wrong';
  }
});