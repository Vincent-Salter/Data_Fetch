//Popup and Dynamic Buttons
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.chart-buttons button');
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            buttons.forEach(btn => btn.classList.remove('selected'));
            button.classList.add('selected');
        });
    });
});
function openPopup() {
    document.getElementById('popup').style.display = 'flex';
}

function closePopup() {
    document.getElementById('popup').style.display = 'none';
}

//API Data