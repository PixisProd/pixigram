const form = document.getElementById('loginForm');
const errorDiv = document.getElementById('error');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  errorDiv.textContent = '';

  const formData = new FormData(form);

  try {

    const response = await fetch('api/auth/login', {
      method: 'POST',
      body: formData,
      credentials: "include",
    });
    if (response.ok) {
      window.location.href = '/about';
    } else {
      const resData = await response.json();
      errorDiv.textContent = resData.detail || 'Login failed';
    }
  } catch (error) {
    console.log(response.status)
    errorDiv.textContent = 'Something went wrong';
  }
});

