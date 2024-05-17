//Dynamic Buttons
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.chart-buttons button');
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            buttons.forEach(btn => btn.classList.remove('selected'));
            button.classList.add('selected');
        });
    });
    //Box Two Output Change
    const stockRows = document.querySelectorAll('.stock-section table tr');
    const chartTitle = document.querySelector('.chart-title');

    stockRows.forEach((row, index) => {
        if (index > 0) { // Skip the header row
            row.addEventListener('click', () => {
                const stockName = row.querySelector('td:first-child').textContent;
                chartTitle.textContent = stockName;
            });
        }
    });
});

//Analysis Popup
function openPopup() {
    document.getElementById('popup').style.display = 'flex';
}

function closePopup() {
    document.getElementById('popup').style.display = 'none';
}

//API Data
const apiKey = '18LjE9K8L83T29Dme8VBHARXUHg4X4qT';