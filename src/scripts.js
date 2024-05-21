document.addEventListener('DOMContentLoaded', function() {
    // Function to handle form submission
    function submitForm(event) {
        event.preventDefault(); // Prevent default form submission

        // Get form data
        const stock = document.getElementById('Stock').value;
        const drawdown = document.getElementById('drawdown').value;
        const days = document.getElementById('days').value;
        const action = document.getElementById('action').value;

        // Get the current date as the buy date and calculate a sell date
        const buyDate = new Date();
        const sellDate = new Date(buyDate);
        sellDate.setDate(buyDate.getDate() + parseInt(days));

        // Mock prices for demonstration purposes
        const buyPrice = 100;
        const sellPrice = 105;
    
        const longProfit = sellPrice - buyPrice;

        // Get the results table body
        const tableBody = document.getElementById('resultsTable').querySelector('tbody');

        // Create a new row and populate it with data
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td>${buyDate.toLocaleDateString()}</td>
            <td>${buyPrice}</td>
            <td>${sellDate.toLocaleDateString()}</td>
            <td>${sellPrice}</td>
            <td>${longProfit}</td>
        `;

        tableBody.appendChild(newRow);
    }

    // Add event listener to the form
    const form = document.getElementById('stockForm');
    form.addEventListener('submit', submitForm);
});

function saveCSV() {
    console.log("Save CSV button clicked!");
    // Get the table element
    const table = document.getElementById('resultsTable');

    // Get the table rows
    const rows = table.querySelectorAll('tbody tr');

    // Create a CSV content string with headers
    let csvContent = "data:text/csv;charset=utf-8,";
    csvContent += "Buy Date,Buy Price,Sell Date,Sell Price,Long Profit\n"; // Add headers

    // Iterate over each row and construct the CSV content
    rows.forEach(row => {
        const rowData = [];
        row.querySelectorAll('td').forEach(cell => {
            rowData.push(cell.innerText);
        });
        csvContent += rowData.join(',') + '\n';
    });

    // Encode the CSV content
    const encodedURI = encodeURI(csvContent);

    const link = document.createElement('a');
    link.setAttribute('href', encodedURI);
    link.setAttribute('download', 'analysis_results.csv');

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);
}