document.addEventListener('DOMContentLoaded', () => {
  const tablaCitas = document.getElementById('tabla-body-citas');

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

  if (tablaCitas) {
    tablaCitas.addEventListener('click', async (e) => {
      // Verificar si se hizo clic en un botón de acción
      if (e.target.classList.contains('btn-accion-cita')) {
        const citaId = e.target.dataset.id;
        const nuevoEstado = e.target.dataset.estado;
        const csrftoken = getCookie('csrftoken');

        try {
          const response = await fetch(`/api/citas/${citaId}/estado/`, {
            method: 'PATCH',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ estado: nuevoEstado })
          });

          if (response.ok) {
            // Recargar para refrescar el estado guardado en PostgreSQL
            window.location.reload();
          } else {
            const err = await response.json();
            alert('Error al cambiar el estado: ' + JSON.stringify(err));
          }
        } catch (error) {
          console.error('Error procesando el cambio de estado:', error);
        }
      }
    });
  }
});