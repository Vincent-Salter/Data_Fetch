function openPopup() {
    document.getElementById('popup').style.display = 'flex';
}

function closePopup() {
    document.getElementById('popup').style.display = 'none';
}

    document.addEventListener('DOMContentLoaded', function() {
                const buttons = document.querySelectorAll('.chart-buttons button');
                buttons.forEach(button => {
                    button.addEventListener('click', () => {
                        buttons.forEach(btn => btn.classList.remove('selected'));
                        button.classList.add('selected');
                    });
                });
            });


// Function to handle form submission
function submitForm(event) {
    event.preventDefault(); // Prevent default form submission behavior

    // Get form values
    const stock = document.getElementById('Stock').value;
    const drawdown = document.getElementById('drawdown').value;
    const days = document.getElementById('days').value;
    const action = document.getElementById('action').value;

    // Redirect user to analysis.html with form values as URL parameters
    window.location.href = `analysis.html?stock=${stock}&drawdown=${drawdown}&days=${days}&action=${action}`;
}

        // Function to redirect back to index.html
        function redirectToIndex() {
            window.location.href = 'index.html';
        }
        
        // Function to get URL parameters
        function getUrlParams() {
            const searchParams = new URLSearchParams(window.location.search);
            return Object.fromEntries(searchParams.entries());
        }
        
        // Function to set stock name as button text
        function setStockName() {
            const params = getUrlParams();
            const stockName = params['stock']; // Retrieve stock name from URL parameters
            const backButton = document.getElementById('backButton');
            if (backButton) {
                backButton.textContent = `${stockName}`;
            }
        }
        
        // Call setStockName() function when DOM content is fully loaded
        document.addEventListener('DOMContentLoaded', () => {
            console.log('DOMContentLoaded event fired');
            setStockName();
        });
        
        // Add event listener to the back button
        const backButton = document.getElementById('backButton');
        if (backButton) {
            backButton.addEventListener('click', redirectToIndex);
        }