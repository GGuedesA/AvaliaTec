const toggleButton = document.getElementById('toggle-btn')
const sidebar = document.getElementById('sidebar')

function toggleSidebar(){
  sidebar.classList.toggle('close')
  toggleButton.classList.toggle('rotate')

  closeAllSubMenus()
}

function toggleSubMenu(button){

  if(!button.nextElementSibling.classList.contains('show')){
    closeAllSubMenus()
  }

  button.nextElementSibling.classList.toggle('show')
  button.classList.toggle('rotate')

  if(sidebar.classList.contains('close')){
    sidebar.classList.toggle('close')
    toggleButton.classList.toggle('rotate')
  }
}

function closeAllSubMenus(){
  Array.from(sidebar.getElementsByClassName('show')).forEach(ul => {
    ul.classList.remove('show')
    ul.previousElementSibling.classList.remove('rotate')
  })
}

document.addEventListener('DOMContentLoaded', function() {
    const bancaCard = document.getElementById('bancaCard');

    if (bancaCard) {
        bancaCard.addEventListener('click', function() {
            const url = bancaCard.getAttribute('data-url');
            window.location.href = url;
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
  const salaCard = document.getElementById('salaCard');

  if (salaCard) {
      salaCard.addEventListener('click', function() {
          const url = salaCard.getAttribute('data-url');
          window.location.href = url;
      });
  }
});

document.addEventListener('DOMContentLoaded', function() {
  const historicoCard = document.getElementById('historicoCard');

  if (historicoCard) {
      historicoCard.addEventListener('click', function() {
          const url = historicoCard.getAttribute('data-url');
          window.location.href = url;
      });
  }
});



        document.addEventListener('DOMContentLoaded', function() {
            const accessToken = localStorage.getItem('access_token');

            if (accessToken) {
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + accessToken;
            }
        });

        function logout() {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user_role');
            document.getElementById('logout-form').submit();
        }
