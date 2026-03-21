// Church MRM - Website portal customizations
document.addEventListener('DOMContentLoaded', function () {
    // Replace the default "Apps" link in user dropdown with "Expense Scanner"
    var navLinks = document.querySelectorAll('.navbar .dropdown-item, .navbar .nav-link');
    navLinks.forEach(function (link) {
        if (link.getAttribute('href') === '/apps') {
            link.setAttribute('href', '/expense-scanner');
            link.textContent = 'Expense Scanner';
        }
    });
});
