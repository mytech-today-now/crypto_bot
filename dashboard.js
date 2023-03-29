// Define constants
const COLOR_SCHEMES = {
  "light": {
      "--background-color": "#ffffff",
      "--text-color": "#333333",
      "--primary-color": "#007bff",
      "--secondary-color": "#6c757d",
      "--accent-color": "#ffc107",
      "--success-color": "#28a745",
      "--danger-color": "#dc3545",
      "--warning-color": "#ffc107"
  },
  "dark": {
      "--background-color": "#1a1a1a",
      "--text-color": "#f5f5f5",
      "--primary-color": "#007bff",
      "--secondary-color": "#6c757d",
      "--accent-color": "#ffc107",
      "--success-color": "#28a745",
      "--danger-color": "#dc3545",
      "--warning-color": "#ffc107"
  }
};

// Define variables
let colorScheme = "light";

// Function to toggle the color scheme
function toggleColorScheme() {
  if (colorScheme === "light") {
      colorScheme = "dark";
  } else {
      colorScheme = "light";
  }
  document.documentElement.style.cssText = Object.entries(COLOR_SCHEMES[colorScheme]).map(([k, v]) => `${k}: ${v}`).join(';');
}

// Function to update the dashboard with the latest data
function updateDashboard() {
  // Get the latest data from the server
  const data = fetch('/api/data')
      .then(response => response.json())
      .then(data => {
          // Update the dashboard with the new data
          document.getElementById('price').textContent = data.price;
          document.getElementById('balance').textContent = data.balance;
          document.getElementById('transactions').innerHTML = data.transactions.map(t => `
              <tr>
                  <td>${t.type}</td>
                  <td>${t.amount}</td>
                  <td>${t.date}</td>
              </tr>
          `).join('');
      });
}

// Function to set up recurring orders
function setRecurringOrders() {
  // TODO: Implement
}

// Function to select an AI model
function selectAIModel() {
  // TODO: Implement
}

// Attach event listeners to UI elements
document.getElementById('toggle-color-scheme').addEventListener('click', toggleColorScheme);
document.getElementById('set-recurring-orders').addEventListener('click', setRecurringOrders);
document.getElementById('select-ai-model').addEventListener('change', selectAIModel);

// Update the dashboard on load and every 5 seconds
updateDashboard();
setInterval(updateDashboard, 5000);
