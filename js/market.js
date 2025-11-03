// CS2 Skin Trading Simulator - Market System

// Skins data
const SKINS_DATA = [
  {
    id: 1,
    name: "AK-47 | Redline",
    category: "rifle",
    basePrice: 250,
    rarity: "rare",
    image: "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot7HxfDhjxszJemkV09-5lpKKqPrxN7LEmyVQ7MEpiLuSrYmnjQO3-UdsZGHyd4_Bd1RvNQ7T_VDrw-_ng5Pu75iY1zI97bhLDA6V"
  },
  {
    id: 2,
    name: "AWP | Asiimov",
    category: "sniper",
    basePrice: 850,
    rarity: "epic",
    image: "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot621FAR17PLfYQJD_9W7m5a0mvLwOq7c2GoFu5Ry0r_F94623ATs_xVtNW6gd4-SegI4MliF_FK5w-7u1pa5ot2XnjtM_1tT"
  },
  {
    id: 3,
    name: "M4A4 | Howl",
    category: "rifle",
    basePrice: 3500,
    rarity: "legendary",
    image: "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpou-6kejhz2v_Nfz5H_uO1gb-Gw_alDLjQhH9U5Pp9g-7J4bP5iUazrl07ZT_2cYPBdVI_YFrS-gO9x7q6hpPo6pTNzSNq63J37iuMgVXp1h2FRtJC"
  },
  {
    id: 4,
    name: "Desert Eagle | Blaze",
    category: "pistol",
    basePrice: 450,
    rarity: "rare",
    image: "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgposr-kLAtl7PLZTjlH_9mkgIWKkPvLO7zQhH9U5Pp9g-7J4bP5iUazrl1kYj3yLdSXIwA_NQrR_gXrk-nsh8C66prBmCNquyZ3tHvfgVXp1kZOYeQ3"
  },
  {
    id: 5,
    name: "Karambit | Fade",
    category: "knife",
    basePrice: 5000,
    rarity: "legendary",
    image: "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpovbSsLQJf2PLacDBA5ciJlY20k_jkI7fUhFRB4MZOhuDG_Zi72gO3-UBrZzyhcY-QdlRrYQ3Y_QS2xO-6hpDpupXAmCQyvSQjs3vfzELhiU5SLrs4B5EbGbU"
  },
  {
    id: 6,
    name: "Glock-18 | Water Elemental",
    category: "pistol",
    basePrice: 120,
    rarity: "common",
    image: "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgposbaqKAxf0v73dShD4N6_mIWZqP76DLfYkWNFppdy0-qS8NiliwXmrRJvZjvwLYHBcwFoZArR-VO5kOzxxcjr3vu5XQ"
  },
  {
    id: 7,
    name: "AK-47 | Fire Serpent",
    category: "rifle",
    basePrice: 2800,
    rarity: "legendary",
    image: "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot7HxfDhjxszJemkV08y5nY6fqPP9ILrUklRd4cJ5nqeQpNz0jgC2qEU9MGHwdY-delQ3YVCDqQe6wOjvjJC76ZrBmCYyuCR34HjD30vgF3VEn2Y"
  },
  {
    id: 8,
    name: "AWP | Dragon Lore",
    category: "sniper",
    basePrice: 8500,
    rarity: "legendary",
    image: "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot621FAR17PLfYQJD_9W7m5a0mvLwOq7cqWdQ-sJ0teXI8oThxlLkqBJsYTz1doKXcQM_NQ6FqFPqwry5h5O96pnLyHM37yF37X7D30vgd4mKZV0"
  },
  {
    id: 9,
    name: "Butterfly Knife | Crimson Web",
    category: "knife",
    basePrice: 4200,
    rarity: "epic",
    image: "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpovbSsLQJf0ebcZThQ6tCvq4GGqOP1Pb7dhFJW-fp8j-3I4IG7jVLs_UtsZ23wJI-VdFBvYw3V-1HskOjnhJDo6oOJlyWSwC3x2A"
  },
  {
    id: 10,
    name: "USP-S | Kill Confirmed",
    category: "pistol",
    basePrice: 380,
    rarity: "rare",
    image: "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpoo6m1FBRp3_bGcjhQ09-jq5WYh8jiPLfFl2xU18h0juDU-MKt3ALs-Us9Nj30coPEe1Q9ZFzW8lK2xefxxcjr2uObLNA"
  }
];

const Market = {
  skins: [],
  currentPrices: {},
  priceHistory: {}, // {skinId: [prices]}
  priceChangePercent: {},
  isRunning: false,
  intervalId: null,
  updateInterval: 5000, // 5 seconds

  // Load skins data
  loadSkins() {
    this.skins = SKINS_DATA;

    // Initialize prices and history
    this.skins.forEach(skin => {
      this.currentPrices[skin.id] = skin.basePrice;
      this.priceHistory[skin.id] = [skin.basePrice];
      this.priceChangePercent[skin.id] = 0;
    });

    console.log('Skins loaded:', this.skins.length);
    return this.skins;
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
