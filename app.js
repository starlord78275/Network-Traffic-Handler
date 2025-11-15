let updateInterval = null;
let lastMessageCount = 0;

function formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function updateStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            // Update stat cards
            document.getElementById('activeConnections').textContent = data.active_connections;
            document.getElementById('totalConnections').textContent = data.total_connections;
            document.getElementById('bytesReceived').textContent = formatBytes(data.total_bytes_received);
            document.getElementById('bytesSent').textContent = formatBytes(data.total_bytes_sent);
            
            // Update connected clients
            const clientsList = document.getElementById('clientsList');
            if (data.connected_clients && data.connected_clients.length > 0) {
                clientsList.innerHTML = '';
                data.connected_clients.forEach(client => {
                    const chip = document.createElement('div');
                    chip.className = 'client-chip';
                    chip.innerHTML = `<span>👤</span> ${client}`;
                    clientsList.appendChild(chip);
                });
            } else {
                clientsList.innerHTML = '<p class="empty-state">No clients connected</p>';
            }
            
            // Update messages
            const messagesContainer = document.getElementById('messages');
            if (data.messages && data.messages.length > 0) {
                if (data.messages.length !== lastMessageCount) {
                    messagesContainer.innerHTML = '';
                    data.messages.slice().reverse().forEach(msg => {
                        const messageDiv = document.createElement('div');
                        messageDiv.className = 'message-item';
                        messageDiv.innerHTML = `
                            <div class="message-header">
                                <span class="message-from">${msg.from}</span>
                                <span class="message-time">${msg.time}</span>
                            </div>
                            <div class="message-text">${escapeHtml(msg.message)}</div>
                        `;
                        messagesContainer.appendChild(messageDiv);
                    });
                    lastMessageCount = data.messages.length;
                }
            } else {
                messagesContainer.innerHTML = '<p class="empty-state">Waiting for messages...</p>';
                lastMessageCount = 0;
            }
        })
        .catch(error => {
            console.error('Error fetching stats:', error);
            document.getElementById('statusBadge').innerHTML = '<span>⚠️ Connection Error</span>';
        });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Start updating
updateInterval = setInterval(updateStats, 1000);
updateStats();

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (updateInterval) {
        clearInterval(updateInterval);
    }
});
