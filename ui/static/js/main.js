// Digital Twin System - Main JavaScript
// Full interactive functionality for the new UI design

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initApp();
});

function initApp() {
    // Setup user menu dropdown
    setupUserMenu();
    
    // Setup interactive elements
    setupInteractiveElements();
    
    // Load initial data
    loadDashboardData();
    
    // Setup real-time updates
    setupRealTimeUpdates();
}

function setupUserMenu() {
    const userMenu = document.querySelector('.user-menu');
    if (userMenu) {
        userMenu.addEventListener('click', function() {
            const dropdown = document.querySelector('.user-dropdown');
            if (dropdown) {
                dropdown.classList.toggle('show');
            }
        });
    }
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.user-menu')) {
            const dropdown = document.querySelector('.user-dropdown');
            if (dropdown) {
                dropdown.classList.remove('show');
            }
        }
    });
}

function setupInteractiveElements() {
    // Setup button interactions
    setupButtons();
    
    // Setup form submissions
    setupForms();
    
    // Setup navigation
    setupNavigation();
}

function setupButtons() {
    // Edit Twin button
    const editButtons = document.querySelectorAll('.btn-edit');
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const twinId = this.dataset.twinId;
            if (twinId) {
                editTwin(twinId);
            }
        });
    });
    
    // Create Twin button
    const createButton = document.querySelector('.btn-create');
    if (createButton) {
        createButton.addEventListener('click', function() {
            showCreateTwinModal();
        });
    }
    
    // Delete Twin button
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const twinId = this.dataset.twinId;
            if (twinId) {
                deleteTwin(twinId);
            }
        });
    });
}

function setupForms() {
    // Create twin form
    const createForm = document.querySelector('#create-twin-form');
    if (createForm) {
        createForm.addEventListener('submit', function(e) {
            e.preventDefault();
            createTwin();
        });
    }
    
    // Edit twin form
    const editForm = document.querySelector('#edit-twin-form');
    if (editForm) {
        editForm.addEventListener('submit', function(e) {
            e.preventDefault();
            updateTwin();
        });
    }
}

function setupNavigation() {
    // Handle navigation between pages
    const navLinks = document.querySelectorAll('a[href^="/ui/"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // For now, let the browser handle navigation
            // In a SPA, we would prevent default and handle routing
        });
    });
}

async function loadDashboardData() {
    try {
        // Load twins data
        const twins = await fetchTwins();
        updateDashboardTwins(twins);
        
        // Load metrics
        const metrics = await fetchMetrics();
        updateDashboardMetrics(metrics);
        
        // Load interaction log
        const interactions = await fetchInteractions();
        updateInteractionLog(interactions);
        
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showError('Failed to load dashboard data');
    }
}

async function fetchTwins() {
    try {
        const response = await fetch('/api/v1/twins');
        if (!response.ok) throw new Error('Failed to fetch twins');
        
        const twinIds = await response.json();
        
        // Fetch detailed data for each twin
        const twins = [];
        for (const twinId of twinIds) {
            try {
                const twinResponse = await fetch(`/api/v1/twins/${twinId}`);
                if (twinResponse.ok) {
                    const twin = await twinResponse.json();
                    twins.push(twin);
                }
            } catch (error) {
                console.warn(`Failed to fetch twin ${twinId}:`, error);
            }
        }
        
        return twins;
    } catch (error) {
        console.error('Error fetching twins:', error);
        return [];
    }
}

async function fetchMetrics() {
    // For now, return mock metrics
    // In a real app, this would come from the API
    return {
        simulationAccuracy: 94.2,
        dataSourcesConnected: 8,
        lastSync: new Date().toLocaleString(),
        customMetric: 'Optimal'
    };
}

async function fetchInteractions() {
    // For now, return mock interactions
    // In a real app, this would come from the API
    return [
        {
            id: 1,
            user: 'You',
            message: 'Hello, how are you today?',
            timestamp: new Date(Date.now() - 300000).toLocaleString(),
            type: 'user'
        },
        {
            id: 2,
            user: 'Digital Twin',
            message: 'Hello! I\'m doing well, thank you for asking. How can I assist you today?',
            timestamp: new Date(Date.now() - 240000).toLocaleString(),
            type: 'twin'
        },
        {
            id: 3,
            user: 'You',
            message: 'Can you show me my health metrics?',
            timestamp: new Date(Date.now() - 180000).toLocaleString(),
            type: 'user'
        },
        {
            id: 4,
            user: 'Digital Twin',
            message: 'Of course! Your current health metrics show excellent status across all parameters.',
            timestamp: new Date(Date.now() - 120000).toLocaleString(),
            type: 'twin'
        }
    ];
}

function updateDashboardTwins(twins) {
    const twinOverview = document.querySelector('.twin-overview');
    if (!twinOverview || twins.length === 0) return;
    
    const twin = twins[0]; // Show first twin in overview
    
    // Update twin name
    const twinName = twinOverview.querySelector('.twin-name');
    if (twinName) {
        twinName.textContent = twin.name || 'Digital Twin';
    }
    
    // Update twin status
    const statusText = twinOverview.querySelector('.status-text');
    if (statusText) {
        statusText.textContent = twin.status || 'Active';
    }
    
    // Update last updated
    const lastUpdated = twinOverview.querySelector('.last-updated');
    if (lastUpdated) {
        lastUpdated.textContent = `Last updated: ${twin.last_updated || new Date().toLocaleString()}`;
    }
    
    // Update edit button
    const editButton = twinOverview.querySelector('.btn-edit');
    if (editButton) {
        editButton.dataset.twinId = twin.twin_id;
    }
}

function updateDashboardMetrics(metrics) {
    // Update metric cards
    const metricCards = document.querySelectorAll('.metric-card');
    metricCards.forEach(card => {
        const metricType = card.dataset.metric;
        const valueElement = card.querySelector('.metric-value');
        
        if (valueElement && metrics[metricType]) {
            valueElement.textContent = metrics[metricType];
        }
    });
}

function updateInteractionLog(interactions) {
    const interactionLog = document.querySelector('.interaction-log');
    if (!interactionLog) return;
    
    // Clear existing interactions
    const existingInteractions = interactionLog.querySelectorAll('.interaction-item');
    existingInteractions.forEach(item => item.remove());
    
    // Add new interactions
    interactions.forEach(interaction => {
        const interactionItem = createInteractionItem(interaction);
        interactionLog.appendChild(interactionItem);
    });
}

function createInteractionItem(interaction) {
    const item = document.createElement('div');
    item.className = `interaction-item ${interaction.type}`;
    
    item.innerHTML = `
        <div class="interaction-bubble">
            <div class="interaction-header">
                <span class="interaction-user">${interaction.user}</span>
                <span class="interaction-time">${interaction.timestamp}</span>
            </div>
            <div class="interaction-message">${interaction.message}</div>
        </div>
    `;
    
    return item;
}

async function createTwin() {
    const form = document.querySelector('#create-twin-form');
    const formData = new FormData(form);
    
    try {
        const response = await fetch('/api/v1/twins', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: formData.get('name'),
                description: formData.get('description')
            })
        });
        
        if (response.ok) {
            const result = await response.json();
            showSuccess('Digital twin created successfully!');
            closeModal('create-twin-modal');
            form.reset();
            
            // Reload dashboard data
            loadDashboardData();
        } else {
            throw new Error('Failed to create twin');
        }
    } catch (error) {
        console.error('Error creating twin:', error);
        showError('Failed to create digital twin');
    }
}

async function editTwin(twinId) {
    try {
        const response = await fetch(`/api/v1/twins/${twinId}`);
        if (!response.ok) throw new Error('Failed to fetch twin');
        
        const twin = await response.json();
        
        // Populate edit form
        const editForm = document.querySelector('#edit-twin-form');
        if (editForm) {
            editForm.querySelector('[name="name"]').value = twin.name || '';
            editForm.querySelector('[name="description"]').value = twin.description || '';
            editForm.dataset.twinId = twinId;
        }
        
        // Show edit modal
        showModal('edit-twin-modal');
        
    } catch (error) {
        console.error('Error editing twin:', error);
        showError('Failed to load twin data');
    }
}

async function updateTwin() {
    const form = document.querySelector('#edit-twin-form');
    const twinId = form.dataset.twinId;
    const formData = new FormData(form);
    
    try {
        const response = await fetch(`/api/v1/twins/${twinId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: formData.get('name'),
                description: formData.get('description')
            })
        });
        
        if (response.ok) {
            showSuccess('Digital twin updated successfully!');
            closeModal('edit-twin-modal');
            
            // Reload dashboard data
            loadDashboardData();
        } else {
            throw new Error('Failed to update twin');
        }
    } catch (error) {
        console.error('Error updating twin:', error);
        showError('Failed to update digital twin');
    }
}

async function deleteTwin(twinId) {
    if (!confirm('Are you sure you want to delete this digital twin? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/v1/twins/${twinId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showSuccess('Digital twin deleted successfully!');
            
            // Reload dashboard data
            loadDashboardData();
        } else {
            throw new Error('Failed to delete twin');
        }
    } catch (error) {
        console.error('Error deleting twin:', error);
        showError('Failed to delete digital twin');
    }
}

function showCreateTwinModal() {
    showModal('create-twin-modal');
}

function showModal(modalId) {
    const modal = document.querySelector(`#${modalId}`);
    if (modal) {
        modal.classList.add('show');
        document.body.classList.add('modal-open');
    }
}

function closeModal(modalId) {
    const modal = document.querySelector(`#${modalId}`);
    if (modal) {
        modal.classList.remove('show');
        document.body.classList.remove('modal-open');
    }
}

function showSuccess(message) {
    showNotification(message, 'success');
}

function showError(message) {
    showNotification(message, 'error');
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Show notification
    setTimeout(() => notification.classList.add('show'), 100);
    
    // Hide and remove notification
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function setupRealTimeUpdates() {
    // Set up periodic refresh of dashboard data
    setInterval(() => {
        loadDashboardData();
    }, 30000); // Refresh every 30 seconds
}

// Global functions for use in HTML
window.createTwin = createTwin;
window.editTwin = editTwin;
window.deleteTwin = deleteTwin;
window.showCreateTwinModal = showCreateTwinModal;
window.closeModal = closeModal;
