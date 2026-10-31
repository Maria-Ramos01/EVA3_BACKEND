document.addEventListener('DOMContentLoaded', () => {
  const formTutorMascota = document.getElementById('form-tutor-mascota');

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  if (formTutorMascota) {
    formTutorMascota.addEventListener('submit', async (e) => {
  e.preventDefault();

  const payload = {
    nombre: document.getElementById('tutor_nombre').value,
    rut: document.getElementById('tutor_rut').value,
    email: document.getElementById('tutor_email').value,
    telefono: document.getElementById('tutor_telefono').value,
    mascotas: []
  };

  // Extraer todas las mascotas del formulario
  document.querySelectorAll('.mascota-item').forEach(item => {
    payload.mascotas.push({
      nombre: item.querySelector('.mascota_nombre').value,
      especie: item.querySelector('.mascota_especie').value,
      raza: item.querySelector('.mascota_raza').value
    });
  });

  try {
    const response = await fetch('/api/registrar-tutor-mascotas/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify(payload)
    });

    const result = await response.json();

    if (response.ok) {
      alert('Tutor y mascotas guardados en PostgreSQL correctamente.');
      // Recarga la página para refrescar el listado cargado desde el backend
      window.location.reload();
    } else {
      alert('Error en el servidor: ' + JSON.stringify(result));
    }
  } catch (error) {
    console.error('Error al enviar la petición:', error);
    alert('Ocurrió un error al procesar el formulario.');
  }
});
  
// Abrir modal con datos actuales
function editarTutor(id, nombre, rut, email, telefono) {
  document.getElementById('edit_tutor_id').value = id;
  document.getElementById('edit_tutor_nombre').value = nombre;
  document.getElementById('edit_tutor_rut').value = rut;
  document.getElementById('edit_tutor_email').value = email;
  document.getElementById('edit_tutor_telefono').value = telefono;
  document.getElementById('modal-editar').style.display = 'flex';
}

function cerrarModal() {
  document.getElementById('modal-editar').style.display = 'none';
}

// Enviar actualización mediante API
document.getElementById('form-editar-tutor').addEventListener('submit', async (e) => {
  e.preventDefault();
  const id = document.getElementById('edit_tutor_id').value;
  
  const payload = {
    nombre: document.getElementById('edit_tutor_nombre').value,
    rut: document.getElementById('edit_tutor_rut').value,
    email: document.getElementById('edit_tutor_email').value,
    telefono: document.getElementById('edit_tutor_telefono').value
  };

  try {
    const response = await fetch(`/api/tutores/${id}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify(payload)
    });

    if (response.ok) {
      alert('Tutor actualizado correctamente');
      window.location.reload();
    } else {
      alert('Error al actualizar');
    }
  } catch (err) {
    console.error('Error:', err);
  }
});