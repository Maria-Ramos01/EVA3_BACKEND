document.addEventListener('DOMContentLoaded', () => {
  const formCita = document.getElementById('form-cita');
  const selectVeterinario = document.getElementById('veterinario');
  const inputFecha = document.getElementById('fecha');
  const tablaCitas = document.getElementById('tabla-citas');

  // Datos de disponibilidad predefinidos por profesional (simulación frontend / API)
  const disponibilidadProfesionales = {
    'Dr. Roberto Gómez - General': {
      diasPermitidos: [1, 2, 3, 4, 5], // Lunes a Viernes
      horaInicio: '09:00',
      horaFin: '17:00'
    },
    'Dra. Maria Silva - Cirugía': {
      diasPermitidos: [2, 4, 6], // Martes, Jueves y Sábado
      horaInicio: '08:00',
      horaFin: '14:00'
    }
  };

  // Validar disponibilidad dinámicamente al cambiar la fecha u hora
  if (inputFecha && selectVeterinario) {
    inputFecha.addEventListener('change', () => {
      const fechaSeleccionada = new Date(inputFecha.value);
      const vetSeleccionado = selectVeterinario.value;
      const reglasVet = disponibilidadProfesionales[vetSeleccionado];

      if (!reglasVet) return;

      const diaSemana = fechaSeleccionada.getDay();
      const horaSeleccionada = fechaSeleccionada.toTimeString().substring(0, 5);

      // Validar día de trabajo del veterinario
      if (!reglasVet.diasPermitidos.includes(diaSemana)) {
        alert(`El profesional ${vetSeleccionado} no atiende en el día seleccionado.`);
        inputFecha.value = '';
        return;
      }

      // Validar rango horario de atención
      if (horaSeleccionada < reglasVet.horaInicio || horaSeleccionada > reglasVet.horaFin) {
        alert(`Horario fuera del rango de atención del profesional (${reglasVet.horaInicio} - ${reglasVet.horaFin}).`);
        inputFecha.value = '';
      }
    });
  }

  // Manejar el envío del formulario de reserva e insertar en la tabla dinámica
  if (formCita) {
    formCita.addEventListener('submit', (e) => {
      e.preventDefault();

      const vet = selectVeterinario.value;
      const fechaHora = inputFecha.value;

      if (!fechaHora) {
        alert('Por favor selecciona una fecha y hora válidas.');
        return;
      }

      // Formatear fecha para visualización limpia
      const fechaFormateada = fechaHora.replace('T', ' ');

      // Crear nueva fila en la agenda del calendario
      const nuevaFila = document.createElement('tr');
      nuevaFila.innerHTML = `
        <td>${fechaFormateada}</td>
        <td>${vet}</td>
        <td>Mascota Registrada</td>
        <td><span style="color: green; font-weight: bold;">Confirmada</span></td>
      `;

      tablaCitas.appendChild(nuevaFila);

      // Limpiar formulario y notificar
      formCita.reset();
      alert('Cita reservada con éxito.');
    });
  }
});