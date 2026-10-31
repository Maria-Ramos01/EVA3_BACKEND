document.addEventListener('DOMContentLoaded', () => {
  const radioAntiguo = document.getElementById('radio-antiguo');
  const radioNuevo = document.getElementById('radio-nuevo');
  const seccionAntiguo = document.getElementById('seccion-paciente-antiguo');
  const seccionNuevo = document.getElementById('seccion-paciente-nuevo');
  const selectMascota = document.getElementById('select_mascota');
  const formCita = document.getElementById('form-cita');

  // Alternar Visibilidad entre Paciente Antiguo y Nuevo
  function conmutarTipoPaciente() {
    if (radioAntiguo.checked) {
      seccionAntiguo.style.display = 'grid';
      seccionNuevo.style.display = 'none';
      selectMascota.required = true;
    } else {
      seccionAntiguo.style.display = 'none';
      seccionNuevo.style.display = 'grid';
      selectMascota.required = false;
    }
  }

  radioAntiguo.addEventListener('change', conmutarTipoPaciente);
  radioNuevo.addEventListener('change', conmutarTipoPaciente);

  // Procesar Guardado de la Cita
  formCita.addEventListener('submit', async (e) => {
    e.preventDefault();

    const esNuevo = radioNuevo.checked;
    let payload = {
      tipo_paciente: esNuevo ? 'NUEVO' : 'ANTIGUO',
      veterinario_id: document.getElementById('select_veterinario').value,
      fecha_hora: document.getElementById('fecha_hora').value,
      motivo: document.getElementById('motivo_consulta').value
    };

    if (esNuevo) {
      payload.tutor = {
        nombre: document.getElementById('nuevo_tutor_nombre').value,
        rut: document.getElementById('nuevo_tutor_rut').value,
        telefono: document.getElementById('nuevo_tutor_telefono').value,
        email: document.getElementById('nuevo_tutor_email').value
      };
      payload.mascota = {
        nombre: document.getElementById('nueva_mascota_nombre').value,
        especie: document.getElementById('nueva_mascota_especie').value,
        raza: document.getElementById('nueva_mascota_raza').value
      };
    } else {
      payload.mascota_id = selectMascota.value;
    }

    try {
      const response = await fetch('/api/agendar-cita/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(payload)
      });

      const res = await response.json();
      if (response.ok) {
        alert('¡Cita reservada con éxito!');
        window.location.reload();
      } else {
        alert('Error: ' + JSON.stringify(res));
      }
    } catch (err) {
      console.error('Error agendando cita:', err);
    }
  });
});