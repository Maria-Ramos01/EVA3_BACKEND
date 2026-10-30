document.addEventListener('DOMContentLoaded', () => {
  console.log('PetCare System Ready');
  
  // Ejemplo de interacción dinámica básica para formularios
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', (e) => {
      // Las peticiones reales se conectarán a las API endpoints de DRF
      console.log(`Formulario ${form.id} enviado.`);
    });
  });
});