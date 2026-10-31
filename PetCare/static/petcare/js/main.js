document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('main-login-form');
  const loginSection = document.getElementById('login-section');
  const dashboardSection = document.getElementById('dashboard-section');
  const protectedLinks = document.getElementById('nav-protected-links');

  // Simulación de persistencia de sesión local (o autenticación en Django/DRF)
  const isAuthenticated = localStorage.getItem('petcare_authenticated') === 'true';

  function activarVistaSistema() {
    if (loginSection) loginSection.style.display = 'none';
    if (dashboardSection) dashboardSection.style.display = 'block';
    if (protectedLinks) protectedLinks.style.display = 'inline';
  }

  // Si ya inició sesión anteriormente
  if (isAuthenticated) {
    activarVistaSistema();
  }

  // Manejador del submit de login en la página principal
  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      // Si usas submit convencional por Django, la vista redirigirá.
      // Si usas JS/API:
      const user = document.getElementById('username').value;
      const pass = document.getElementById('password').value;

      if (user && pass) {
        localStorage.setItem('petcare_authenticated', 'true');
        activarVistaSistema();
      }
    });
  }
});