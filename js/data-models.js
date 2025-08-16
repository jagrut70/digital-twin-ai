/**
 * Digital Twin Data Models
 * Defines the core data structures for the digital twin system
 */

class DigitalTwin {
  constructor(config = {}) {
    this.id = config.id || this.generateId();
    this.name = config.name || 'Your Digital Twin';
    this.description = config.description || 'Synthetic data-driven personality simulation';
    this.status = config.status || 'active';
    this.createdAt = config.createdAt || new Date();
    this.updatedAt = config.updatedAt || new Date();
    
    // Core attributes derived from synthetic data
    this.attributes = {
      appearance: config.appearance || this.getDefaultAppearance(),
      personality: config.personality || this.getDefaultPersonality(),
      health: config.health || this.getDefaultHealth(),
      behavior: config.behavior || this.getDefaultBehavior(),
      voice: config.voice || this.getDefaultVoice()
    };
    
    // Connected synthetic datasets
    this.dataSources = config.dataSources || this.getDefaultDataSources();
    
    // Performance metrics
    this.metrics = {
      simulationAccuracy: 94.7,
      learningProgress: 87.2,
      responseQuality: 92.1,
      dataIntegrity: 98.5
    };
    
    // Interaction history
    this.interactions = [];
    
    // Event listeners for updates
    this.eventListeners = {
      update: [],
      interact: [],
      learn: []
    };
  }
  
  generateId() {
    return 'twin_' + Math.random().toString(36).substr(2, 9);
  }
  
  getDefaultAppearance() {
    return {
      model: 'SynBody_v2.1',
      height: 175, // cm
      build: 'average',
      hairColor: 'brown',
      eyeColor: 'hazel',
      skinTone: 'medium',
      ageRange: '25-35',
      style: 'casual-professional'
    };
  }
  
  getDefaultPersonality() {
    return {
      traits: {
        openness: 0.75,
        conscientiousness: 0.82,
        extraversion: 0.68,
        agreeableness: 0.71,
        neuroticism: 0.23
      },
      interests: ['technology', 'learning', 'problem-solving', 'creativity'],
      communicationStyle: 'thoughtful',
      decisionMaking: 'analytical',
      learningStyle: 'active'
    };
  }
  
  getDefaultHealth() {
    return {
      physicalWellness: 85,
      mentalWellness: 88,
      energyLevel: 78,
      stressLevel: 22,
      sleepQuality: 82,
      activityLevel: 'moderate',
      lastCheckup: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000) // 1 week ago
    };
  }
  
  getDefaultBehavior() {
    return {
      routines: [
        { time: '07:00', activity: 'morning_routine', priority: 'high' },
        { time: '09:00', activity: 'work_focus', priority: 'high' },
        { time: '12:00', activity: 'break_time', priority: 'medium' },
        { time: '18:00', activity: 'evening_routine', priority: 'medium' }
      ],
      preferences: {
        workingHours: { start: '09:00', end: '17:00' },
        breakFrequency: 90, // minutes
        communicationPreference: 'concise',
        learningPreference: 'interactive'
      },
      adaptability: 0.78
    };
  }
  
  getDefaultVoice() {
    return {
      tone: 'warm',
      pace: 'moderate',
      formality: 'professional-casual',
      languageComplexity: 'moderate',
      emotionalRange: 'balanced',
      responseLength: 'medium'
    };
  }
  
  getDefaultDataSources() {
    return [
      {
        name: 'SynBody Dataset',
        type: 'appearance',
        status: 'connected',
        lastSync: new Date(Date.now() - 2 * 60 * 1000), // 2 minutes ago
        records: 15420
      },
      {
        name: 'Aria Digital Twin',
        type: 'behavior',
        status: 'connected',
        lastSync: new Date(Date.now() - 5 * 60 * 1000), // 5 minutes ago
        records: 8934
      },
      {
        name: 'SIPHER Population',
        type: 'demographics',
        status: 'connected',
        lastSync: new Date(Date.now() - 10 * 60 * 1000), // 10 minutes ago
        records: 25650
      },
      {
        name: 'NVIDIA Synthetic',
        type: 'generative',
        status: 'connected',
        lastSync: new Date(Date.now() - 1 * 60 * 1000), // 1 minute ago
        records: 12890
      }
    ];
  }
  
  // Update twin attributes
  updateAttributes(newAttributes) {
    this.attributes = { ...this.attributes, ...newAttributes };
    this.updatedAt = new Date();
    this.emit('update', { attributes: newAttributes });
    return this;
  }
  
  // Add interaction
  addInteraction(interaction) {
    const interactionRecord = {
      id: this.generateId(),
      timestamp: new Date(),
      type: interaction.type || 'chat',
      input: interaction.input,
      output: interaction.output,
      confidence: interaction.confidence || 0.95,
      processingTime: interaction.processingTime || 150 // ms
    };
    
    this.interactions.unshift(interactionRecord);
    
    // Keep only last 100 interactions
    if (this.interactions.length > 100) {
      this.interactions = this.interactions.slice(0, 100);
    }
    
    this.emit('interact', interactionRecord);
    return interactionRecord;
  }
  
  // Update metrics
  updateMetrics(newMetrics) {
    this.metrics = { ...this.metrics, ...newMetrics };
    this.updatedAt = new Date();
    return this;
  }
  
  // Learn from interaction (simulate learning)
  learn(feedback) {
    // Simulate learning by slightly adjusting metrics
    if (feedback.positive) {
      this.metrics.simulationAccuracy = Math.min(100, this.metrics.simulationAccuracy + 0.1);
      this.metrics.learningProgress = Math.min(100, this.metrics.learningProgress + 0.2);
    }
    
    this.emit('learn', feedback);
    return this;
  }
  
  // Event system
  on(event, callback) {
    if (!this.eventListeners[event]) {
      this.eventListeners[event] = [];
    }
    this.eventListeners[event].push(callback);
    return this;
  }
  
  emit(event, data) {
    if (this.eventListeners[event]) {
      this.eventListeners[event].forEach(callback => callback(data));
    }
    return this;
  }
  
  // Get formatted status
  getStatus() {
    const now = new Date();
    const timeSinceUpdate = now - this.updatedAt;
    const minutesAgo = Math.floor(timeSinceUpdate / (1000 * 60));
    
    return {
      status: this.status,
      lastUpdated: minutesAgo === 0 ? 'Just now' : 
                  minutesAgo === 1 ? '1 minute ago' : 
                  minutesAgo < 60 ? `${minutesAgo} minutes ago` : 
                  `${Math.floor(minutesAgo / 60)} hours ago`,
      connectedSources: this.dataSources.filter(ds => ds.status === 'connected').length,
      totalInteractions: this.interactions.length
    };
  }
  
  // Serialize for storage
  toJSON() {
    return {
      id: this.id,
      name: this.name,
      description: this.description,
      status: this.status,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
      attributes: this.attributes,
      dataSources: this.dataSources,
      metrics: this.metrics,
      interactions: this.interactions.slice(0, 20) // Only save recent interactions
    };
  }
  
  // Create from stored data
  static fromJSON(data) {
    return new DigitalTwin(data);
  }
}

// Synthetic Data Source class
class SyntheticDataSource {
  constructor(config) {
    this.name = config.name;
    this.type = config.type;
    this.endpoint = config.endpoint;
    this.status = 'disconnected';
    this.lastSync = null;
    this.records = 0;
    this.metadata = config.metadata || {};
  }
  
  async connect() {
    // Simulate connection
    return new Promise((resolve) => {
      setTimeout(() => {
        this.status = 'connected';
        this.lastSync = new Date();
        resolve(true);
      }, 1000);
    });
  }
  
  async sync() {
    if (this.status !== 'connected') {
      throw new Error('Data source not connected');
    }
    
    // Simulate data sync
    return new Promise((resolve) => {
      setTimeout(() => {
        this.lastSync = new Date();
        this.records += Math.floor(Math.random() * 100);
        resolve({
          records: this.records,
          timestamp: this.lastSync
        });
      }, 500);
    });
  }
  
  disconnect() {
    this.status = 'disconnected';
    return this;
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { DigitalTwin, SyntheticDataSource };
} else {
  window.DigitalTwin = DigitalTwin;
  window.SyntheticDataSource = SyntheticDataSource;
}
