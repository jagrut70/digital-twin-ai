/**
 * Main Application Entry Point
 * Initializes the Digital Twin Dashboard
 */

class DigitalTwinApp {
  constructor() {
    this.digitalTwin = null;
    this.syntheticAI = null;
    this.interactionManager = null;
    this.metricsSimulator = null;
    
    this.init();
  }
  
  async init() {
    try {
      // Initialize components
      this.initializeComponents();
      
      // Load saved data or create new twin
      await this.loadOrCreateTwin();
      
      // Initialize UI
      this.initializeUI();
      
      // Start periodic updates
      this.startPeriodicUpdates();
      
      console.log('Digital Twin Dashboard initialized successfully');
      
    } catch (error) {
      console.error('Failed to initialize Digital Twin Dashboard:', error);
      this.showErrorState();
    }
  }
  
  initializeComponents() {
    // Initialize synthetic AI
    this.syntheticAI = new SyntheticAI();
    
    // Initialize metrics simulator
    this.metricsSimulator = new MetricsSimulator();
  }
  
  async loadOrCreateTwin() {
    // Try to load from localStorage
    const savedTwin = localStorage.getItem('digitalTwin');
    
    if (savedTwin) {
      try {
        const twinData = JSON.parse(savedTwin);
        this.digitalTwin = DigitalTwin.fromJSON(twinData);
        console.log('Loaded existing digital twin from storage');
      } catch (error) {
        console.warn('Failed to load saved twin data, creating new twin:', error);
        this.digitalTwin = new DigitalTwin();
      }
    } else {
      // Create new digital twin
      this.digitalTwin = new DigitalTwin();
      console.log('Created new digital twin');
    }
    
    // Set up auto-save on changes
    this.digitalTwin.on('update', () => {
      this.saveTwinToStorage();
    });
    
    this.digitalTwin.on('interact', () => {
      this.saveTwinToStorage();
    });
  }
  
  initializeUI() {
    // Initialize interaction manager
    this.interactionManager = new InteractionManager(this.digitalTwin, this.syntheticAI);
    
    // Initialize theme
    this.interactionManager.initializeTheme();
    
    // Initialize feather icons
    feather.replace();
    
    // Add CSS for typing indicator animation
    this.addTypingIndicatorStyles();
    
    // Add form group styles for modal
    this.addFormGroupStyles();
    
    // Update initial display
    this.updateInitialDisplay();
  }
  
  updateInitialDisplay() {
    // Update status display
    const status = this.digitalTwin.getStatus();
    
    // Update meta information
    const metaElements = document.querySelectorAll('.meta-item');
    if (metaElements[0]) {
      metaElements[0].innerHTML = `
        <i data-feather="clock" class="meta-icon"></i>
        Last updated: ${status.lastUpdated}
      `;
    }
    
    if (metaElements[1]) {
      metaElements[1].innerHTML = `
        <i data-feather="database" class="meta-icon"></i>
        Data sources: ${status.connectedSources} connected
      `;
    }
    
    // Update metrics
    const metrics = this.digitalTwin.metrics;
    const accuracyElement = document.querySelector('.metric-card:first-child .metric-value');
    const learningElement = document.querySelector('.metric-card:last-child .metric-value');
    
    if (accuracyElement) {
      accuracyElement.textContent = `${metrics.simulationAccuracy.toFixed(1)}%`;
    }
    
    if (learningElement) {
      learningElement.textContent = `${metrics.learningProgress.toFixed(1)}%`;
    }
    
    // Re-render icons
    feather.replace();
  }
  
  startPeriodicUpdates() {
    // Simulate metric updates every 30 seconds
    setInterval(() => {
      const updatedMetrics = this.metricsSimulator.updateMetrics();
      this.digitalTwin.updateMetrics(updatedMetrics);
      
      if (this.interactionManager) {
        this.interactionManager.updateMetricsDisplay();
      }
    }, 30000);
    
    // Update sync times every minute
    setInterval(() => {
      // Simulate data source sync updates
      const dataSources = this.digitalTwin.dataSources;
      dataSources.forEach(source => {
        if (Math.random() < 0.3) { // 30% chance of sync update
          source.lastSync = new Date();
        }
      });
      
      this.updateSyncTimes();
    }, 60000);
    
    // Auto-save every 5 minutes
    setInterval(() => {
      this.saveTwinToStorage();
    }, 5 * 60 * 1000);
  }
  
  updateSyncTimes() {
    const syncElement = document.querySelector('.metric-card:nth-child(3) .metric-value');
    if (syncElement && Math.random() < 0.5) { // 50% chance to update display
      const times = ['Just now', '1m ago', '2m ago', '3m ago'];
      syncElement.textContent = times[Math.floor(Math.random() * times.length)];
    }
  }
  
  saveTwinToStorage() {
    try {
      const twinData = this.digitalTwin.toJSON();
      localStorage.setItem('digitalTwin', JSON.stringify(twinData));
    } catch (error) {
      console.warn('Failed to save twin data to storage:', error);
    }
  }
  
  addTypingIndicatorStyles() {
    const style = document.createElement('style');
    style.textContent = `
      .typing-dots {
        display: flex;
        gap: 4px;
        align-items: center;
        justify-content: center;
        padding: 8px 0;
      }
      
      .typing-dots span {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: var(--muted-grey);
        animation: typingPulse 1.4s infinite ease-in-out;
      }
      
      .typing-dots span:nth-child(2) {
        animation-delay: 0.2s;
      }
      
      .typing-dots span:nth-child(3) {
        animation-delay: 0.4s;
      }
      
      @keyframes typingPulse {
        0%, 60%, 100% {
          opacity: 0.3;
          transform: scale(0.8);
        }
        30% {
          opacity: 1;
          transform: scale(1);
        }
      }
      
      .message-bubble.typing {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
      }
    `;
    document.head.appendChild(style);
  }
  
  addFormGroupStyles() {
    const style = document.createElement('style');
    style.textContent = `
      .form-group {
        margin-bottom: var(--space-3);
      }
      
      .form-group label {
        display: block;
        font-size: var(--text-sm);
        font-weight: 500;
        color: var(--text-primary);
        margin-bottom: var(--space-1);
      }
      
      .form-group .input {
        margin-bottom: 0;
      }
      
      .message-bubble.error {
        border-color: var(--status-red);
        background-color: var(--status-red-light);
      }
    `;
    document.head.appendChild(style);
  }
  
  showErrorState() {
    const dashboard = document.querySelector('.dashboard');
    if (dashboard) {
      dashboard.innerHTML = `
        <div class="error-state" style="text-align: center; padding: var(--space-8) var(--space-3);">
          <i data-feather="alert-circle" style="width: 48px; height: 48px; color: var(--status-red); margin-bottom: var(--space-2);"></i>
          <h2 style="color: var(--text-primary); margin-bottom: var(--space-2);">Failed to Initialize</h2>
          <p style="color: var(--text-secondary); max-width: 400px; margin: 0 auto var(--space-4);">
            There was an error initializing your digital twin dashboard. Please refresh the page to try again.
          </p>
          <button class="btn btn-primary" onclick="window.location.reload()">
            <i data-feather="refresh-cw" class="btn-icon"></i>
            Refresh Page
          </button>
        </div>
      `;
      feather.replace();
    }
  }
  
  // Public API methods
  getTwin() {
    return this.digitalTwin;
  }
  
  getInteractionManager() {
    return this.interactionManager;
  }
  
  exportTwinData() {
    const data = this.digitalTwin.toJSON();
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `digital-twin-${data.name.toLowerCase().replace(/\s+/g, '-')}-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }
  
  importTwinData(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const data = JSON.parse(e.target.result);
          this.digitalTwin = DigitalTwin.fromJSON(data);
          this.saveTwinToStorage();
          this.updateInitialDisplay();
          resolve(this.digitalTwin);
        } catch (error) {
          reject(error);
        }
      };
      reader.onerror = reject;
      reader.readAsText(file);
    });
  }
}

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  window.digitalTwinApp = new DigitalTwinApp();
});

// Export for debugging and external access
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { DigitalTwinApp };
} else {
  window.DigitalTwinApp = DigitalTwinApp;
}

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
  // Ctrl/Cmd + K to focus message input
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    const messageInput = document.getElementById('messageInput');
    if (messageInput) {
      messageInput.focus();
    }
  }
  
  // Escape to close modals
  if (e.key === 'Escape') {
    const activeModal = document.querySelector('.modal-overlay.active');
    if (activeModal) {
      activeModal.classList.remove('active');
      setTimeout(() => activeModal.remove(), 300);
    }
  }
});
