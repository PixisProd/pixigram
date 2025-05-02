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
      document.getElementById('user-name').textContent = user.username;
      document.getElementById('user-email').textContent = user.email;
      document.getElementById('user-role').textContent = user.role;
    } else {
      const resData = await response.json();
      errorMessage.textContent = resData.detail || 'Error fetching user data';
      window.location.href = '/login';
    }
  } catch (error) {
    errorMessage.textContent = `Something went wrong while fetching user data`;
    window.location.href = '/login';
  }
});

function connectToRoom() {
  const roomId = document.getElementById("room-id-input").value;
  if (roomId.trim()) {
    window.location.href = `/chat?room=${encodeURIComponent(roomId)}`;
  } else {
    alert("Please enter a Room ID");
  }
}