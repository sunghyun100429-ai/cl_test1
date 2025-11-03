// CS2 Skin Trading Simulator - Game Logic

const Game = {
  state: {
    cash: 10000,
    portfolio: {}, // {skinId: count}
    totalValue: 10000,
    startValue: 10000,
    lastUpdate: new Date().toISOString()
  },

  // Initialize game
  init() {
    this.loadGame();
    console.log('Game initialized:', this.state);
  },

  // Save game state to localStorage
  saveGame() {
    try {
      this.state.lastUpdate = new Date().toISOString();
      localStorage.setItem('cs2SimulatorState', JSON.stringify(this.state));
      console.log('Game saved');
    } catch (error) {
      console.error('Failed to save game:', error);
    }
  },

  // Load game state from localStorage
  loadGame() {
    try {
      const saved = localStorage.getItem('cs2SimulatorState');
      if (saved) {
        this.state = JSON.parse(saved);
        console.log('Game loaded from save');
      } else {
        console.log('No saved game found, starting fresh');
      }
    } catch (error) {
      console.error('Failed to load game:', error);
    }
  },

  // Reset game to initial state
  resetGame() {
    if (confirm('Are you sure you want to reset the game? All progress will be lost.')) {
      this.state = {
        cash: 10000,
        portfolio: {},
        totalValue: 10000,
        startValue: 10000,
        lastUpdate: new Date().toISOString()
      };
      this.saveGame();
      console.log('Game reset');
      return true;
    }
    return false;
  },

  // Get current cash
  getCash() {
    return this.state.cash;
  },

  // Update cash amount
  updateCash(amount) {
    this.state.cash += amount;
    this.saveGame();
  },

  // Get portfolio
  getPortfolio() {
    return this.state.portfolio;
  },

  // Get skin count from portfolio
  getSkinCount(skinId) {
    return this.state.portfolio[skinId] || 0;
  },

  // Add skin to portfolio
  addSkin(skinId) {
    if (!this.state.portfolio[skinId]) {
      this.state.portfolio[skinId] = 0;
    }
    this.state.portfolio[skinId]++;
    this.saveGame();
  },

  // Remove skin from portfolio
  removeSkin(skinId) {
    if (this.state.portfolio[skinId] && this.state.portfolio[skinId] > 0) {
      this.state.portfolio[skinId]--;
      if (this.state.portfolio[skinId] === 0) {
        delete this.state.portfolio[skinId];
      }
      this.saveGame();
      return true;
    }
    return false;
  },

  // Update total value
  updateTotalValue(value) {
    this.state.totalValue = value;
  },

  // Get total value
  getTotalValue() {
    return this.state.totalValue;
  },

  // Get start value
  getStartValue() {
    return this.state.startValue;
  },

  // Calculate profit/loss
  calculateProfitLoss() {
    return this.state.totalValue - this.state.startValue;
  },

  // Calculate profit/loss percentage
  calculateProfitLossPercent() {
    return ((this.state.totalValue - this.state.startValue) / this.state.startValue) * 100;
  }
};

// Initialize game when module loads
Game.init();
