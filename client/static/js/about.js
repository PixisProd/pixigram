document.addEventListener('DOMContentLoaded', async () => {
    const userDetails = document.getElementById('user-details');
    const errorMessage = document.getElementById('error-message');
  
    try {
      const response = await fetch('http://localhost:8000/auth/about', {
        method: 'GET',
        credentials: 'include',
      });
  
      if (response.ok) {
        const user = await response.json();
        document.getElementById('user-id').textContent = user.id;
        document.getElementById('user-email').textContent = user.email;
        document.getElementById('user-role').textContent = user.role;
      } else {
        const resData = await response.json();
        errorMessage.textContent = resData.detail || 'Error fetching user data';
      }
    } catch (error) {
      errorMessage.textContent = `Something went wrong while fetching user data ${error.message}`;
    }
  });
  