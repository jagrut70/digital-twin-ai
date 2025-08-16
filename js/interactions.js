/**
 * Interaction Handlers
 * Manages user interactions with the digital twin interface
 */

class InteractionManager {
  constructor(digitalTwin, syntheticAI) {
    this.digitalTwin = digitalTwin;
    this.syntheticAI = syntheticAI;
    this.isProcessing = false;
    this.messageHistory = [];
    
    this.initializeEventListeners();
    this.loadInitialMessages();
  }
  
  initializeEventListeners() {
    // Chat input handling
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendMessage');
    const clearButton = document.querySelector('.clear-log-btn');
    
    if (messageInput && sendButton) {
      // Send message on button click
      sendButton.addEventListener('click', (e) => {
        e.preventDefault();
        this.sendMessage();
      });
      
      // Send message on Enter key
      messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.sendMessage();
        }
      });
      
      // Auto-resize input
      messageInput.addEventListener('input', this.autoResizeInput);
    }
    
    // Clear log button
    if (clearButton) {
      clearButton.addEventListener('click', () => {
        this.clearMessageHistory();
      });
    }
    
    // Edit twin button
    const editTwinButton = document.querySelector('.edit-twin-btn');
    if (editTwinButton) {
      editTwinButton.addEventListener('click', () => {
        this.openTwinEditor();
      });
    }
    
    // Theme toggle
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
      themeToggle.addEventListener('click', () => {
        this.toggleTheme();
      });
    }
    
    // Listen for twin updates
    this.digitalTwin.on('interact', (interaction) => {
      this.updateMetricsAfterInteraction(interaction);
    });
  }
  
  loadInitialMessages() {
    // Add some initial conversation examples
    const initialMessages = [
      {
        type: 'user',
        text: 'How are you feeling today?',
        timestamp: new Date(Date.now() - 2 * 60 * 1000)
      },
      {
        type: 'twin',
        text: "Based on my synthetic health data, I'm experiencing optimal wellness parameters. My mood simulation indicates a positive state with 92% confidence.",
        timestamp: new Date(Date.now() - 2 * 60 * 1000)
      },
      {
        type: 'user',
        text: "What's your favorite activity?",
        timestamp: new Date(Date.now() - 8 * 60 * 1000)
      },
      {
        type: 'twin',
        text: "According to my behavioral modeling from synthetic lifestyle data, I find creative problem-solving and learning new concepts most engaging. Would you like to explore a topic together?",
        timestamp: new Date(Date.now() - 8 * 60 * 1000)
      }
    ];
    
    this.messageHistory = [...initialMessages];
    this.renderMessageHistory();
  }
  
  async sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    if (!message || this.isProcessing) return;
    
    this.isProcessing = true;
    messageInput.value = '';
    messageInput.disabled = true;
    
    // Add user message
    const userMessage = {
      type: 'user',
      text: message,
      timestamp: new Date()
    };
    
    this.addMessage(userMessage);
    
    // Show typing indicator
    this.showTypingIndicator();
    
    try {
      // Generate AI response
      const response = await this.syntheticAI.generateResponse(message);
      
      // Remove typing indicator
      this.hideTypingIndicator();
      
      // Add twin response
      const twinMessage = {
        type: 'twin',
        text: response.text,
        timestamp: new Date(),
        metadata: response.metadata
      };
      
      this.addMessage(twinMessage);
      
      // Record interaction in digital twin
      this.digitalTwin.addInteraction({
        input: message,
        output: response.text,
        confidence: response.metadata.confidence,
        processingTime: response.metadata.processingTime
      });
      
    } catch (error) {
      console.error('Error generating response:', error);
      this.hideTypingIndicator();
      
      // Add error message
      const errorMessage = {
        type: 'twin',
        text: "I'm having some difficulty processing that right now. Could you try rephrasing your question?",
        timestamp: new Date(),
        isError: true
      };
      
      this.addMessage(errorMessage);
    } finally {
      this.isProcessing = false;
      messageInput.disabled = false;
      messageInput.focus();
    }
  }
  
  addMessage(message) {
    this.messageHistory.unshift(message);
    
    // Keep only last 50 messages
    if (this.messageHistory.length > 50) {
      this.messageHistory = this.messageHistory.slice(0, 50);
    }
    
    this.renderNewMessage(message);
    this.scrollToLatest();
  }
  
  renderNewMessage(message) {
    const logContent = document.getElementById('logContent');
    if (!logContent) return;
    
    const messageElement = this.createMessageElement(message);
    
    // Add to beginning (latest messages first)
    if (logContent.firstChild) {
      logContent.insertBefore(messageElement, logContent.firstChild);
    } else {
      logContent.appendChild(messageElement);
    }
    
    // Animate in
    messageElement.style.opacity = '0';
    messageElement.style.transform = 'translateY(-10px)';
    
    requestAnimationFrame(() => {
      messageElement.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
      messageElement.style.opacity = '1';
      messageElement.style.transform = 'translateY(0)';
    });
  }
  
  createMessageElement(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `interaction-item ${message.type}-message`;
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    if (message.isError) {
      bubble.classList.add('error');
    }
    
    const text = document.createElement('p');
    text.textContent = message.text;
    bubble.appendChild(text);
    
    const timestamp = document.createElement('span');
    timestamp.className = 'message-timestamp';
    timestamp.textContent = this.formatTime(message.timestamp);
    
    messageDiv.appendChild(bubble);
    messageDiv.appendChild(timestamp);
    
    return messageDiv;
  }
  
  renderMessageHistory() {
    const logContent = document.getElementById('logContent');
    if (!logContent) return;
    
    logContent.innerHTML = '';
    
    // Render messages in reverse chronological order (newest first)
    this.messageHistory.forEach(message => {
      const messageElement = this.createMessageElement(message);
      logContent.appendChild(messageElement);
    });
  }
  
  showTypingIndicator() {
    const logContent = document.getElementById('logContent');
    if (!logContent) return;
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'interaction-item twin-message typing-indicator';
    typingDiv.id = 'typing-indicator';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble typing';
    
    const dots = document.createElement('div');
    dots.className = 'typing-dots';
    dots.innerHTML = '<span></span><span></span><span></span>';
    
    bubble.appendChild(dots);
    typingDiv.appendChild(bubble);
    
    if (logContent.firstChild) {
      logContent.insertBefore(typingDiv, logContent.firstChild);
    } else {
      logContent.appendChild(typingDiv);
    }
    
    this.scrollToLatest();
  }
  
  hideTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
      typingIndicator.remove();
    }
  }
  
  scrollToLatest() {
    const logContent = document.getElementById('logContent');
    if (logContent) {
      logContent.scrollTop = 0; // Scroll to top since newest messages are first
    }
  }
  
  clearMessageHistory() {
    this.messageHistory = [];
    this.renderMessageHistory();
    
    // Show empty state
    const logContent = document.getElementById('logContent');
    if (logContent) {
      const emptyState = document.createElement('div');
      emptyState.className = 'empty-state';
      emptyState.innerHTML = `
        <i data-feather="message-circle" class="empty-state-icon"></i>
        <h3>No conversations yet</h3>
        <p>Start a conversation with your digital twin to see interactions here.</p>
      `;
      logContent.appendChild(emptyState);
      feather.replace();
    }
  }
  
  formatTime(timestamp) {
    return timestamp.toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    });
  }
  
  autoResizeInput(event) {
    const input = event.target;
    input.style.height = 'auto';
    input.style.height = Math.min(input.scrollHeight, 120) + 'px';
  }
  
  updateMetricsAfterInteraction(interaction) {
    // Simulate slight improvements in metrics after successful interactions
    const currentMetrics = this.digitalTwin.metrics;
    const improvements = {
      simulationAccuracy: Math.min(100, currentMetrics.simulationAccuracy + 0.05),
      responseQuality: Math.min(100, currentMetrics.responseQuality + 0.03)
    };
    
    this.digitalTwin.updateMetrics(improvements);
    this.updateMetricsDisplay();
  }
  
  updateMetricsDisplay() {
    const metrics = this.digitalTwin.metrics;
    
    // Update metric cards
    const accuracyElement = document.querySelector('.metric-card:first-child .metric-value');
    if (accuracyElement) {
      accuracyElement.textContent = `${metrics.simulationAccuracy.toFixed(1)}%`;
    }
    
    const learningElement = document.querySelector('.metric-card:last-child .metric-value');
    if (learningElement) {
      learningElement.textContent = `${metrics.learningProgress.toFixed(1)}%`;
    }
    
    // Update last sync time
    const syncElement = document.querySelector('.metric-card:nth-child(3) .metric-value');
    if (syncElement) {
      syncElement.textContent = 'Just now';
    }
  }
  
  toggleTheme() {
    const body = document.body;
    const themeIcon = document.querySelector('.theme-icon');
    
    if (body.classList.contains('light-mode')) {
      body.classList.remove('light-mode');
      body.classList.add('dark-mode');
      if (themeIcon) {
        themeIcon.setAttribute('data-feather', 'sun');
      }
      localStorage.setItem('theme', 'dark');
    } else {
      body.classList.remove('dark-mode');
      body.classList.add('light-mode');
      if (themeIcon) {
        themeIcon.setAttribute('data-feather', 'moon');
      }
      localStorage.setItem('theme', 'light');
    }
    
    // Re-render feather icons
    feather.replace();
  }
  
  openTwinEditor() {
    // Create modal for editing twin attributes
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
      <div class="modal">
        <div class="modal-header">
          <h3 class="modal-title">Edit Digital Twin</h3>
          <button class="icon-btn close-modal">
            <i data-feather="x"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Name</label>
            <input type="text" class="input" value="${this.digitalTwin.name}" id="twin-name">
          </div>
          <div class="form-group">
            <label>Description</label>
            <input type="text" class="input" value="${this.digitalTwin.description}" id="twin-description">
          </div>
          <div class="form-group">
            <label>Communication Style</label>
            <select class="input" id="twin-voice">
              <option value="warm" ${this.digitalTwin.attributes.voice.tone === 'warm' ? 'selected' : ''}>Warm</option>
              <option value="professional" ${this.digitalTwin.attributes.voice.tone === 'professional' ? 'selected' : ''}>Professional</option>
              <option value="casual" ${this.digitalTwin.attributes.voice.tone === 'casual' ? 'selected' : ''}>Casual</option>
              <option value="analytical" ${this.digitalTwin.attributes.voice.tone === 'analytical' ? 'selected' : ''}>Analytical</option>
            </select>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary cancel-edit">Cancel</button>
          <button class="btn btn-primary save-twin">Save Changes</button>
        </div>
      </div>
    `;
    
    document.body.appendChild(modal);
    feather.replace();
    
    // Show modal
    requestAnimationFrame(() => {
      modal.classList.add('active');
    });
    
    // Event listeners
    const closeBtn = modal.querySelector('.close-modal');
    const cancelBtn = modal.querySelector('.cancel-edit');
    const saveBtn = modal.querySelector('.save-twin');
    
    const closeModal = () => {
      modal.classList.remove('active');
      setTimeout(() => modal.remove(), 300);
    };
    
    closeBtn.addEventListener('click', closeModal);
    cancelBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });
    
    saveBtn.addEventListener('click', () => {
      const name = document.getElementById('twin-name').value;
      const description = document.getElementById('twin-description').value;
      const voiceTone = document.getElementById('twin-voice').value;
      
      // Update twin
      this.digitalTwin.name = name;
      this.digitalTwin.description = description;
      this.digitalTwin.attributes.voice.tone = voiceTone;
      this.digitalTwin.updatedAt = new Date();
      
      // Update UI
      this.updateTwinDisplay();
      
      closeModal();
    });
  }
  
  updateTwinDisplay() {
    const nameElement = document.querySelector('.twin-name');
    const descElement = document.querySelector('.twin-description');
    
    if (nameElement) {
      nameElement.textContent = this.digitalTwin.name;
    }
    
    if (descElement) {
      descElement.textContent = this.digitalTwin.description;
    }
    
    // Update last updated time
    const metaElements = document.querySelectorAll('.meta-item');
    if (metaElements[0]) {
      metaElements[0].innerHTML = `
        <i data-feather="clock" class="meta-icon"></i>
        Last updated: Just now
      `;
      feather.replace();
    }
  }
  
  // Initialize theme from localStorage
  initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    const body = document.body;
    const themeIcon = document.querySelector('.theme-icon');
    
    if (savedTheme === 'dark') {
      body.classList.remove('light-mode');
      body.classList.add('dark-mode');
      if (themeIcon) {
        themeIcon.setAttribute('data-feather', 'sun');
      }
    } else {
      body.classList.remove('dark-mode');
      body.classList.add('light-mode');
      if (themeIcon) {
        themeIcon.setAttribute('data-feather', 'moon');
      }
    }
    
    feather.replace();
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { InteractionManager };
} else {
  window.InteractionManager = InteractionManager;
}
