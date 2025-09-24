document.getElementById("citaForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const token = localStorage.getItem("token");
  if (!token) {
    alert("Su cita esta guardada");
    return;
  }

  const body = {
    title: document.getElementById("title").value,
    contact_id: document.getElementById("contactId").value, // obligatorio
    startTime: new Date(document.getElementById("startTime").value).toISOString(),
    endTime: new Date(document.getElementById("endTime").value).toISOString(),
    description: document.getElementById("description").value
  };

  try {
    const res = await fetch("http://localhost:8000/api/citas/crear/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify(body)
    });

    const data = await res.json();
    document.getElementById("resultado").textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    document.getElementById("resultado").textContent = "❌ Error al crear cita.";
  }
});
