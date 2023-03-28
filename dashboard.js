/* dashboard_10.13.js

2023-03-26
Designer: mytechtoday@protonmail.com
Coder: ChatGPT
*/


// Load the dashboard when the page is ready
document.addEventListener("DOMContentLoaded", function() {
  loadDashboard();
});

// Load the dashboard data and update the UI
function loadDashboard() {
  // Call the API to get the dashboard data
  fetch('/api/dashboard')
    .then(response => response.json())
    .then(data => {
      // Update the UI with the data
      updateDashboard(data);
      // Schedule a refresh of the dashboard every 30 seconds
      setInterval(loadDashboard, 30000);
    })
    .catch(error => {
      // Handle errors
      console.error('Error loading dashboard:', error);
      showError('Error loading dashboard');
    });
}

// Update the UI with the dashboard data
function updateDashboard(data) {
  // Update the account balance
  const balanceElement = document.getElementById('balance');
  balanceElement.textContent = data.balance.toFixed(2);

  // Update the list of open orders
  const openOrdersElement = document.getElementById('open-orders');
  openOrdersElement.innerHTML = '';
  data.open_orders.forEach(order => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${order.symbol}</td>
      <td>${order.side}</td>
      <td>${order.price}</td>
      <td>${order.amount}</td>
      <td>${order.time}</td>
    `;
    openOrdersElement.appendChild(row);
  });

  // Update the list of transaction history
  const transactionHistoryElement = document.getElementById('transaction-history');
  transactionHistoryElement.innerHTML = '';
  data.transaction_history.forEach(transaction => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${transaction.symbol}</td>
      <td>${transaction.side}</td>
      <td>${transaction.price}</td>
      <td>${transaction.amount}</td>
      <td>${transaction.time}</td>
    `;
    transactionHistoryElement.appendChild(row);
  });
}

// Show an error message
function showError(message) {
  const errorElement = document.getElementById('error');
  errorElement.textContent = message;
  errorElement.style.display = 'block';
}
