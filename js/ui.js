// CS2 Skin Trading Simulator - UI Updates

const UI = {
  // Format currency
  formatCurrency(amount) {
    return '$' + amount.toLocaleString('en-US', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });
  },

  // Format percent
  formatPercent(value) {
    const sign = value >= 0 ? '+' : '';
    return sign + value.toFixed(1) + '%';
  },

  // Update stats display
  updateStats() {
    const cash = Game.getCash();
    const totalValue = Game.getTotalValue();
    const profitLossPercent = Game.calculateProfitLossPercent();

    document.getElementById('cash').textContent = this.formatCurrency(cash);
    document.getElementById('totalValue').textContent = this.formatCurrency(totalValue);

    const profitElement = document.getElementById('profit');
    profitElement.textContent = this.formatPercent(profitLossPercent);
    profitElement.className = profitLossPercent >= 0 ? 'positive' : 'negative';
  },

  // Update market status
  updateMarketStatus() {
    const statusBtn = document.getElementById('toggleMarket');
    const isRunning = Market.isMarketRunning();

    if (isRunning) {
      statusBtn.textContent = '⏸️ Pause Market';
      statusBtn.classList.add('active');
    } else {
      statusBtn.textContent = '▶️ Start Market';
      statusBtn.classList.remove('active');
    }
  },

  // Render skin cards
  renderSkins() {
    const container = document.getElementById('marketList');
    const skins = Market.getSkins();

    if (!container || skins.length === 0) {
      return;
    }

    container.innerHTML = '';

    skins.forEach(skin => {
      const price = Market.getCurrentPrice(skin.id);
      const priceChange = Market.getPriceChangePercent(skin.id);
      const owned = Game.getSkinCount(skin.id);
      const cash = Game.getCash();

      const card = document.createElement('div');
      card.className = 'skin-card';
      card.setAttribute('data-rarity', skin.rarity);

      const priceChangeClass = priceChange >= 0 ? 'positive' : 'negative';
      const canBuy = cash >= price;
      const canSell = owned > 0;

      card.innerHTML = `
        <div class="skin-icon">
          <img src="${skin.image}" alt="${skin.name}" loading="lazy">
        </div>
        <div class="skin-name">${skin.name}</div>
        <div class="skin-meta">
          <span class="category">${skin.category}</span>
          <span class="rarity ${skin.rarity}">${skin.rarity}</span>
        </div>
        <div class="skin-price">${this.formatCurrency(price)}</div>
        <div class="price-change ${priceChangeClass}">${this.formatPercent(priceChange)}</div>
        <div class="skin-owned">Owned: <strong>${owned}</strong></div>
        <div class="skin-actions">
          <button class="btn-buy" data-skin-id="${skin.id}" ${!canBuy ? 'disabled' : ''}>
            Buy
          </button>
          <button class="btn-sell" data-skin-id="${skin.id}" ${!canSell ? 'disabled' : ''}>
            Sell
          </button>
        </div>
      `;

      container.appendChild(card);
    });

    // Add event listeners
    this.attachButtonListeners();
  },

  // Attach button event listeners
  attachButtonListeners() {
    // Buy buttons
    document.querySelectorAll('.btn-buy').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const skinId = parseInt(e.target.getAttribute('data-skin-id'));
        this.handleBuy(skinId);
      });
    });

    // Sell buttons
    document.querySelectorAll('.btn-sell').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const skinId = parseInt(e.target.getAttribute('data-skin-id'));
        this.handleSell(skinId);
      });
    });
  },

  // Handle buy action
  handleBuy(skinId) {
    const result = Market.buySkin(skinId);
    if (result.success) {
      this.showNotification(result.message, 'success');
      Market.calculateTotalValue();
      this.updateAll();
    } else {
      this.showNotification(result.message, 'error');
    }
  },

  // Handle sell action
  handleSell(skinId) {
    const result = Market.sellSkin(skinId);
    if (result.success) {
      this.showNotification(result.message, 'success');
      Market.calculateTotalValue();
      this.updateAll();
    } else {
      this.showNotification(result.message, 'error');
    }
  },

  // Show notification
  showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    document.body.appendChild(notification);

    // Trigger animation
    setTimeout(() => {
      notification.classList.add('show');
    }, 10);

    // Remove after 3 seconds
    setTimeout(() => {
      notification.classList.remove('show');
      setTimeout(() => {
        notification.remove();
      }, 300);
    }, 3000);
  },

  // Update last update time
  updateLastUpdate() {
    const lastUpdateElement = document.getElementById('lastUpdate');
    if (lastUpdateElement) {
      const now = new Date();
      lastUpdateElement.textContent = now.toLocaleTimeString();
    }
  },

  // Update all UI elements
  updateAll() {
    this.updateStats();
    this.renderSkins();
    this.updateLastUpdate();
  },

  // Initialize UI
  init() {
    console.log('UI initialized');

    // Toggle market button
    const toggleBtn = document.getElementById('toggleMarket');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => {
        Market.toggle();
        this.updateMarketStatus();
      });
    }

    // Reset button
    const resetBtn = document.getElementById('resetGame');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        if (Game.resetGame()) {
          Market.stop();
          this.updateAll();
          this.updateMarketStatus();
          this.showNotification('Game reset successfully', 'success');
        }
      });
    }

    // Initial update
    this.updateAll();
    this.updateMarketStatus();
  }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  Market.loadSkins();
  UI.init();
});
