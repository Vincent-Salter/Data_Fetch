

const apiKey = '5SpZIvR_wkivQQxrlkML7yeTyB6jsxvf';  // Replace with your actual API key

// Function to fetch popular DEFI data
async function fetchPopularDEFI() {
    const url = `https://api.polygon.io/v2/aggs/grouped/locale/global/market/crypto/2023-05-15?apiKey=${apiKey}`;

    console.log('Fetching popular DEFI data from:', url);

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();

        console.log('Data received:', data);

        // Filter and return the necessary data
        const filteredData = data.results.filter(item => ['BTC', 'ETH', 'USDT', 'BNB', 'ADA'].includes(item.T));
        console.log('Filtered data:', filteredData);
        return filteredData;
    } catch (error) {
        console.error('Error fetching popular DEFI:', error);
    }
}

// Function to fetch data for a specific DEFI and time range
async function fetchDEFIData(ticker, range) {
    const url = `https://api.polygon.io/v2/aggs/ticker/${ticker}/range/1/${range}/2023-01-09/2023-05-15?apiKey=${apiKey}`;

    console.log('Fetching DEFI data for ticker:', ticker, 'with range:', range);

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();

        console.log('Data received for ticker', ticker, ':', data);
        return data;
    } catch (error) {
        console.error('Error fetching DEFI data:', error);
    }
}

// Function to render chart using everviz
function renderChart(data, label) {
    const chartData = data.results.map(item => [new Date(item.t).getTime(), item.c]);

    everviz.chart(document.getElementById('chart'), {
        type: 'line',
        title: { text: label },
        series: [{
            name: label,
            data: chartData
        }]
    });
}

// Function to update chart when a DEFI item is clicked
async function updateChart(ticker, range = 'day') {
    const data = await fetchDEFIData(ticker, range);
    if (data && data.results) {
        renderChart(data, `${ticker} Price`);
    }
}

// Function to initialize the popular DEFI list
async function initializePopularDEFI() {
    const defiData = await fetchPopularDEFI();
    const tableBody = document.querySelector('.stock-section table tbody');

    // Clear existing table data
    tableBody.innerHTML = '';

    defiData.forEach(defi => {
        const row = document.createElement('tr');
        row.classList.add('stock-item');
        row.dataset.ticker = defi.T;

        row.innerHTML = `
            <td>${defi.T}</td>
            <td>${defi.c}</td>
            <td class="${defi.c > 0 ? 'positive' : 'negative'}">${defi.c}</td>
        `;

        row.addEventListener('click', () => updateChart(defi.T));
        tableBody.appendChild(row);
    });
}

// Function to open the popup
function openPopup() {
    document.getElementById('popup').style.display = 'block';
}

// Function to close the popup
function closePopup() {
    document.getElementById('popup').style.display = 'none';
}

// Event listeners for time range buttons
document.querySelectorAll('.chart-buttons button').forEach(button => {
    button.addEventListener('click', () => {
        const ticker = document.querySelector('.chart-section h2').innerText;
        const range = button.innerText.toLowerCase();
        updateChart(ticker, range);
    });
});

// Initialize popular DEFI on page load
document.addEventListener('DOMContentLoaded', initializePopularDEFI);

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