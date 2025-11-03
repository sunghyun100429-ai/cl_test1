// CS2 Skin Trading Simulator - Market System

const Market = {
  skins: [],
  currentPrices: {},
  priceHistory: {}, // {skinId: [prices]}
  priceChangePercent: {},
  isRunning: false,
  intervalId: null,
  updateInterval: 5000, // 5 seconds

  // Load skins data from JSON
  async loadSkins() {
    try {
      const response = await fetch('data/skins.json');
      this.skins = await response.json();

      // Initialize prices and history
      this.skins.forEach(skin => {
        this.currentPrices[skin.id] = skin.basePrice;
        this.priceHistory[skin.id] = [skin.basePrice];
        this.priceChangePercent[skin.id] = 0;
      });

      console.log('Skins loaded:', this.skins.length);
      return this.skins;
    } catch (error) {
      console.error('Failed to load skins:', error);
      return [];
    }
  },

  // Get all skins
  getSkins() {
    return this.skins;
  },

  // Get skin by ID
  getSkinById(id) {
    return this.skins.find(skin => skin.id === id);
  },

  // Get current price
  getCurrentPrice(skinId) {
    return this.currentPrices[skinId] || 0;
  },

  // Get price change percent
  getPriceChangePercent(skinId) {
    return this.priceChangePercent[skinId] || 0;
  },

  // Update prices (random fluctuation -8% to +8%)
  updatePrices() {
    this.skins.forEach(skin => {
      const oldPrice = this.currentPrices[skin.id];
      const changePercent = (Math.random() * 16 - 8); // -8 to +8
      const changeAmount = oldPrice * (changePercent / 100);
      const newPrice = Math.max(oldPrice + changeAmount, skin.basePrice * 0.1); // Min 10% of base price

      this.currentPrices[skin.id] = newPrice;
      this.priceChangePercent[skin.id] = changePercent;

      // Update price history (keep last 30 entries)
      this.priceHistory[skin.id].push(newPrice);
      if (this.priceHistory[skin.id].length > 30) {
        this.priceHistory[skin.id].shift();
      }
    });

    console.log('Prices updated');
  },

  // Buy skin
  buySkin(skinId) {
    const skin = this.getSkinById(skinId);
    if (!skin) {
      return { success: false, message: 'Skin not found' };
    }

    const price = this.getCurrentPrice(skinId);
    const cash = Game.getCash();

    if (cash < price) {
      return { success: false, message: 'Not enough cash' };
    }

    Game.updateCash(-price);
    Game.addSkin(skinId);

    return {
      success: true,
      message: `Bought ${skin.name} for $${price.toFixed(2)}`
    };
  },

  // Sell skin
  sellSkin(skinId) {
    const skin = this.getSkinById(skinId);
    if (!skin) {
      return { success: false, message: 'Skin not found' };
    }

    const count = Game.getSkinCount(skinId);
    if (count <= 0) {
      return { success: false, message: 'You don\'t own this skin' };
    }

    const price = this.getCurrentPrice(skinId);
    Game.updateCash(price);
    Game.removeSkin(skinId);

    return {
      success: true,
      message: `Sold ${skin.name} for $${price.toFixed(2)}`
    };
  },

  // Calculate portfolio value
  calculatePortfolioValue() {
    const portfolio = Game.getPortfolio();
    let totalValue = 0;

    for (const [skinId, count] of Object.entries(portfolio)) {
      const price = this.getCurrentPrice(parseInt(skinId));
      totalValue += price * count;
    }

    return totalValue;
  },

  // Calculate total value (cash + portfolio)
  calculateTotalValue() {
    const cash = Game.getCash();
    const portfolioValue = this.calculatePortfolioValue();
    const totalValue = cash + portfolioValue;

    Game.updateTotalValue(totalValue);
    return totalValue;
  },

  // Start market updates
  start() {
    if (this.isRunning) {
      console.log('Market already running');
      return;
    }

    this.isRunning = true;
    this.intervalId = setInterval(() => {
      this.updatePrices();
      this.calculateTotalValue();
      UI.updateAll();
    }, this.updateInterval);

    console.log('Market started');
  },

  // Stop market updates
  stop() {
    if (!this.isRunning) {
      console.log('Market already stopped');
      return;
    }

    this.isRunning = false;
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }

    console.log('Market stopped');
  },

  // Toggle market
  toggle() {
    if (this.isRunning) {
      this.stop();
    } else {
      this.start();
    }
    return this.isRunning;
  },

  // Get market status
  isMarketRunning() {
    return this.isRunning;
  }
};
