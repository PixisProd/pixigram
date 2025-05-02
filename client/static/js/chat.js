document.addEventListener('DOMContentLoaded', async () => {
  const response = await fetch("http://localhost:8000/auth/is-authorized", {
    method: "GET",
    credentials: "include",
  });

  if (response.status === 200) {
    const urlParams = new URLSearchParams(window.location.search);
    const roomId = urlParams.get('room') || 'default';

    const ws = new WebSocket(`ws://localhost:8000/ws/${roomId}`);

    const chat = document.getElementById('chat');
    const input = document.getElementById('input');
    const sendBtn = document.getElementById('send');

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      const message = document.createElement('div');
      message.textContent = data.text;
      if (data.is_system) {
        message.classList.add("message", "system");
      } else if (data.is_self) {
        message.classList.add("message", "self");
      } else {
        message.classList.add("message", "other");
      }
      chat.appendChild(message);
      chat.scrollTop = chat.scrollHeight;
    };

    sendBtn.onclick = () => {
      if (input.value) {
        ws.send(input.value);
        input.value = '';
      }
    };

    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') sendBtn.click();
    });
  } else {
    window.location.href = "/login";
  }
});


