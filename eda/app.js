/* --- OYUN VERİLERİ VE DURUMU --- */
const LEVELS = [
  {
    id: 1,
    title: "1. Bölüm: Balon Patlatma 🎈",
    instruction: "5 renkli balonu patlat!",
    secretWord: "Birlikte",
    type: "balloons",
    targetScore: 5
  },
  {
    id: 2,
    title: "2. Bölüm: Kart Eşleştirme 🃏",
    instruction: "Tatlı çiftleri bul!",
    secretWord: "güzel",
    type: "memory",
    targetScore: 3
  },
  {
    id: 3,
    title: "3. Bölüm: Yıldızları Yakala ⭐",
    instruction: "Sepetle 5 parlayan yıldız yakala!",
    secretWord: "vakit",
    type: "catch",
    targetScore: 5
  },
  {
    id: 4,
    title: "4. Bölüm: Sevimli Kediyi Yakala 🐾",
    instruction: "Kafasını çıkaran kediye 5 kez dokun!",
    secretWord: "geçiriyoruz",
    type: "mole",
    targetScore: 5
  },
  {
    id: 5,
    title: "5. Bölüm: Kalbi Hedefe Ulaştır 💖",
    instruction: "Kalbi aşağı kaydırıp yıldıza ulaştır!",
    secretWord: "ne dersin?",
    type: "maze",
    targetScore: 1
  }
];

let currentLevelIndex = 0;
let currentScore = 0;
let collectedWords = [];
let currentGameInterval = null;

/* --- DOM ELEMENTLERİ --- */
const screenWelcome = document.getElementById("screen-welcome");
const screenGame = document.getElementById("screen-game");
const screenScratch = document.getElementById("screen-scratch");
const screenFinal = document.getElementById("screen-final");

const startBtn = document.getElementById("startBtn");
const levelBadge = document.getElementById("levelBadge");
const gameInstruction = document.getElementById("gameInstruction");
const playArea = document.getElementById("playArea");
const levelProgressFill = document.getElementById("levelProgressFill");
const levelStatusText = document.getElementById("levelStatusText");

const secretWordElement = document.getElementById("secretWordElement");
const scratchCanvas = document.getElementById("scratchCanvas");
const nextLevelBtn = document.getElementById("nextLevelBtn");
const scratchHeading = document.getElementById("scratchHeading");

const btnYes = document.getElementById("btnYes");
const btnNo = document.getElementById("btnNo");
const finalButtonsWrapper = document.getElementById("finalButtonsWrapper");
const successBox = document.getElementById("successBox");

/* --- MÜZİK YÖNETİMİ (YouTube & Yerel MP3) --- */
const localAudio = document.getElementById("localAudio");
const musicToggleBtn = document.getElementById("musicToggleBtn");
let ytPlayer = null;
let isMusicPlaying = false;
let ytReady = false;

// YouTube API Callback
window.onYouTubeIframeAPIReady = function() {
  ytPlayer = new YT.Player('ytplayer', {
    height: '1',
    width: '1',
    videoId: 'HoxStCU1hqI', // Furkan Olgaç - Benim İklimim İncitmez Seni
    playerVars: {
      'autoplay': 0,
      'controls': 0,
      'loop': 1,
      'playlist': 'HoxStCU1hqI',
      'playsinline': 1
    },
    events: {
      'onReady': () => { ytReady = true; },
      'onStateChange': (event) => {
        if (event.data === YT.PlayerState.PLAYING) {
          isMusicPlaying = true;
          musicToggleBtn.classList.remove('music-paused');
        } else if (event.data === YT.PlayerState.PAUSED) {
          isMusicPlaying = false;
          musicToggleBtn.classList.add('music-paused');
        }
      }
    }
  });
};

function startMusic() {
  localAudio.currentTime = 0;
  const playPromise = localAudio.play();
  if (playPromise !== undefined) {
    playPromise.then(() => {
      isMusicPlaying = true;
      musicToggleBtn.classList.remove('music-paused');
    }).catch(err => {
      console.log("Audio play error, trying fallback:", err);
      if (ytPlayer && typeof ytPlayer.playVideo === "function") {
        ytPlayer.playVideo();
        isMusicPlaying = true;
        musicToggleBtn.classList.remove('music-paused');
      }
    });
  }
}

function toggleMusic() {
  if (isMusicPlaying) {
    localAudio.pause();
    if (ytPlayer && typeof ytPlayer.pauseVideo === "function") {
      ytPlayer.pauseVideo();
    }
    isMusicPlaying = false;
    musicToggleBtn.classList.add('music-paused');
  } else {
    startMusic();
  }
}

musicToggleBtn.addEventListener("click", toggleMusic);

/* --- EKRAN GEÇİŞLERİ --- */
function switchScreen(targetScreen) {
  [screenWelcome, screenGame, screenScratch, screenFinal].forEach(s => s.classList.remove("active"));
  targetScreen.classList.add("active");
}

/* --- OYUN BAŞLATMA --- */
startBtn.addEventListener("click", () => {
  startMusic();
  currentLevelIndex = 0;
  loadLevel(currentLevelIndex);
  switchScreen(screenGame);
});

/* --- SEVİYE YÜKLEME --- */
function loadLevel(index) {
  if (currentGameInterval) {
    clearInterval(currentGameInterval);
    currentGameInterval = null;
  }
  playArea.innerHTML = "";
  currentScore = 0;

  const level = LEVELS[index];
  levelBadge.textContent = `Bölüm ${level.id} / 5`;
  gameInstruction.textContent = level.instruction;
  updateProgress(0, level.targetScore);

  switch (level.type) {
    case "balloons":
      setupBalloonsGame(level);
      break;
    case "memory":
      setupMemoryGame(level);
      break;
    case "catch":
      setupCatchGame(level);
      break;
    case "mole":
      setupMoleGame(level);
      break;
    case "maze":
      setupMazeGame(level);
      break;
  }
}

function updateProgress(score, target) {
  currentScore = score;
  const pct = Math.min(100, Math.round((currentScore / target) * 100));
  levelProgressFill.style.width = pct + "%";
  levelStatusText.textContent = `${currentScore} / ${target}`;

  if (currentScore >= target) {
    setTimeout(levelCompleted, 400);
  }
}

function levelCompleted() {
  if (currentGameInterval) {
    clearInterval(currentGameInterval);
    currentGameInterval = null;
  }
  confetti({ particleCount: 40, spread: 60, origin: { y: 0.6 } });
  setupScratchCard(LEVELS[currentLevelIndex]);
  switchScreen(screenScratch);
}

/* --- 1. MİNİ OYUN: BALON PATLATMA --- */
function setupBalloonsGame(level) {
  const colors = ["#ff758c", "#ff7eb3", "#a18cd1", "#fbc2eb", "#ffd166", "#06d6a0"];
  const emojis = ["🎈", "✨", "🎀", "💖", "🌸"];

  function spawnBalloon() {
    if (currentScore >= level.targetScore) return;
    const balloon = document.createElement("div");
    balloon.className = "balloon";
    const bgCol = colors[Math.floor(Math.random() * colors.length)];
    balloon.style.backgroundColor = bgCol;
    balloon.style.color = bgCol;
    balloon.textContent = emojis[Math.floor(Math.random() * emojis.length)];

    const areaWidth = Math.max(100, playArea.clientWidth - 70);
    const areaHeight = Math.max(100, playArea.clientHeight - 90);
    balloon.style.left = Math.max(10, Math.random() * areaWidth) + "px";
    balloon.style.top = Math.max(10, Math.random() * areaHeight) + "px";

    let popped = false;
    const pop = (e) => {
      if (popped) return;
      popped = true;
      if (e) {
        e.preventDefault();
        e.stopPropagation();
      }
      balloon.classList.add("popping");
      setTimeout(() => balloon.remove(), 180);
      updateProgress(currentScore + 1, level.targetScore);
    };

    balloon.addEventListener("pointerdown", pop);
    balloon.addEventListener("click", pop);
    balloon.addEventListener("touchstart", pop);
    playArea.appendChild(balloon);

    setTimeout(() => {
      if (balloon.parentNode && !balloon.classList.contains("popping")) {
        balloon.remove();
      }
    }, 3800);
  }

  // İlk balonları hemen oluştur
  for (let i = 0; i < 4; i++) {
    setTimeout(spawnBalloon, i * 250);
  }
  currentGameInterval = setInterval(spawnBalloon, 850);
}

/* --- 2. MİNİ OYUN: KART EŞLEŞTİRME --- */
function setupMemoryGame(level) {
  const icons = ["🐱", "☕", "🍓"];
  const deck = [...icons, ...icons].sort(() => Math.random() - 0.5);

  const grid = document.createElement("div");
  grid.className = "memory-grid";
  playArea.appendChild(grid);

  let flippedCards = [];
  let matchedCount = 0;

  deck.forEach((icon) => {
    const card = document.createElement("div");
    card.className = "memory-card hidden-card";
    card.dataset.icon = icon;

    card.addEventListener("click", () => {
      if (flippedCards.length >= 2 || !card.classList.contains("hidden-card") || card.classList.contains("matched")) {
        return;
      }
      card.classList.remove("hidden-card");
      card.textContent = icon;
      flippedCards.push(card);

      if (flippedCards.length === 2) {
        const [c1, c2] = flippedCards;
        if (c1.dataset.icon === c2.dataset.icon) {
          c1.classList.add("matched");
          c2.classList.add("matched");
          matchedCount++;
          flippedCards = [];
          updateProgress(matchedCount, level.targetScore);
        } else {
          setTimeout(() => {
            c1.classList.add("hidden-card");
            c2.classList.add("hidden-card");
            c1.textContent = "";
            c2.textContent = "";
            flippedCards = [];
          }, 800);
        }
      }
    });

    grid.appendChild(card);
  });
}

/* --- 3. MİNİ OYUN: DÜŞENLERİ YAKALAMA --- */
function setupCatchGame(level) {
  const basket = document.createElement("div");
  basket.className = "basket";
  basket.textContent = "🧺";
  playArea.appendChild(basket);

  let basketX = playArea.clientWidth / 2;
  const updateBasketPos = (x) => {
    const areaRect = playArea.getBoundingClientRect();
    let clampedX = Math.max(35, Math.min(x - areaRect.left, areaRect.width - 35));
    basket.style.left = clampedX + "px";
    basketX = clampedX;
  };

  const onPointerMove = (e) => updateBasketPos(e.clientX);
  playArea.addEventListener("pointermove", onPointerMove);
  playArea.addEventListener("touchmove", (e) => {
    if (e.touches[0]) updateBasketPos(e.touches[0].clientX);
  });

  const starIcons = ["⭐", "✨", "💫", "🌟"];

  function spawnStar() {
    if (currentScore >= level.targetScore) return;
    const star = document.createElement("div");
    star.className = "falling-item";
    star.textContent = starIcons[Math.floor(Math.random() * starIcons.length)];
    const startX = Math.random() * (playArea.clientWidth - 40) + 20;
    star.style.left = startX + "px";
    star.style.top = "0px";
    playArea.appendChild(star);

    let starY = 0;
    const speed = 2.8 + Math.random() * 1.5;

    const fallInterval = setInterval(() => {
      starY += speed;
      star.style.top = starY + "px";

      // Sepetle çarpışma kontrolü
      const basketY = playArea.clientHeight - 44;
      if (starY >= basketY - 20 && starY <= basketY + 20) {
        const dist = Math.abs(startX - basketX);
        if (dist < 45) {
          clearInterval(fallInterval);
          star.remove();
          updateProgress(currentScore + 1, level.targetScore);
          return;
        }
      }

      if (starY > playArea.clientHeight) {
        clearInterval(fallInterval);
        star.remove();
      }
    }, 20);
  }

  currentGameInterval = setInterval(spawnStar, 1200);
}

/* --- 4. MİNİ OYUN: SEVİMLİ KEDİ / KÖSTEBEK --- */
function setupMoleGame(level) {
  const grid = document.createElement("div");
  grid.className = "mole-grid";
  playArea.appendChild(grid);

  const holes = [];
  for (let i = 0; i < 6; i++) {
    const hole = document.createElement("div");
    hole.className = "mole-hole";

    const mole = document.createElement("div");
    mole.className = "mole-character";
    mole.textContent = "🐱";

    mole.addEventListener("pointerdown", (e) => {
      e.stopPropagation();
      hole.classList.remove("active");
      mole.textContent = "😸✨";
      updateProgress(currentScore + 1, level.targetScore);
      setTimeout(() => { mole.textContent = "🐱"; }, 400);
    });

    hole.appendChild(mole);
    grid.appendChild(hole);
    holes.push(hole);
  }

  function popupMole() {
    if (currentScore >= level.targetScore) return;
    holes.forEach(h => h.classList.remove("active"));
    const randomHole = holes[Math.floor(Math.random() * holes.length)];
    randomHole.classList.add("active");

    setTimeout(() => {
      randomHole.classList.remove("active");
    }, 1200);
  }

  currentGameInterval = setInterval(popupMole, 1400);
  popupMole();
}

/* --- 5. MİNİ OYUN: KALBİ HEDEFE ULAŞTIR --- */
function setupMazeGame(level) {
  const container = document.createElement("div");
  container.className = "maze-container";

  const track = document.createElement("div");
  track.className = "maze-track";

  const heart = document.createElement("div");
  heart.className = "draggable-heart";
  heart.textContent = "💖";

  const star = document.createElement("div");
  star.className = "target-star";
  star.textContent = "🌟";

  container.appendChild(track);
  container.appendChild(heart);
  container.appendChild(star);
  playArea.appendChild(container);

  let isDragging = false;
  let startY = 0;
  let initialTop = 30;

  const onStart = (e) => {
    isDragging = true;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    startY = clientY;
  };

  const onMove = (e) => {
    if (!isDragging) return;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    const deltaY = clientY - startY;
    let newTop = Math.max(30, initialTop + deltaY);
    const maxTop = playArea.clientHeight - 95;

    heart.style.top = Math.min(newTop, maxTop) + "px";

    if (newTop >= maxTop - 15) {
      isDragging = false;
      heart.style.top = maxTop + "px";
      updateProgress(1, level.targetScore);
    }
  };

  const onEnd = () => {
    if (isDragging) {
      isDragging = false;
      heart.style.top = "30px";
      initialTop = 30;
    }
  };

  heart.addEventListener("pointerdown", onStart);
  window.addEventListener("pointermove", onMove);
  window.addEventListener("pointerup", onEnd);
  heart.addEventListener("touchstart", onStart);
  window.addEventListener("touchmove", onMove);
  window.addEventListener("touchend", onEnd);
}

/* --- KAZIMA KARTI (SCRATCH CARD) MANTIĞI --- */
function setupScratchCard(level) {
  secretWordElement.textContent = level.secretWord;
  scratchHeading.textContent = `${level.id}. Bölümü Tamamladın! 🎉`;
  nextLevelBtn.classList.add("hidden");

  const canvas = scratchCanvas;
  const ctx = canvas.getContext("2d");
  const rect = canvas.getBoundingClientRect();
  canvas.width = 300;
  canvas.height = 150;

  // Gri parlak simülasyon kaplama
  const grad = ctx.createLinearGradient(0, 0, 300, 150);
  grad.addColorStop(0, "#d1d5db");
  grad.addColorStop(0.5, "#9ca3af");
  grad.addColorStop(1, "#d1d5db");
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Üzerine yazı ve desen
  ctx.fillStyle = "#ffffff";
  ctx.font = "bold 16px 'Comfortaa', sans-serif";
  ctx.textAlign = "center";
  ctx.fillText("✨ Burayı Kazı ✨", canvas.width / 2, canvas.height / 2 + 5);

  let isScratching = false;
  let scratchedPixels = 0;
  let totalPixels = canvas.width * canvas.height;
  let isUnlocked = false;

  const scratch = (clientX, clientY) => {
    const cRect = canvas.getBoundingClientRect();
    const x = ((clientX - cRect.left) / cRect.width) * canvas.width;
    const y = ((clientY - cRect.top) / cRect.height) * canvas.height;

    ctx.globalCompositeOperation = "destination-out";
    ctx.beginPath();
    ctx.arc(x, y, 22, 0, Math.PI * 2);
    ctx.fill();

    checkScratchProgress();
  };

  function checkScratchProgress() {
    if (isUnlocked) return;
    const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    let transparentCount = 0;
    // Her 16 pikselde bir örnekleme yap (performans için)
    for (let i = 3; i < imgData.data.length; i += 16) {
      if (imgData.data[i] === 0) {
        transparentCount++;
      }
    }
    const ratio = transparentCount / (imgData.data.length / 16);
    if (ratio > 0.45) {
      isUnlocked = true;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      confetti({ particleCount: 30, spread: 50 });
      nextLevelBtn.classList.remove("hidden");

      // Kelime slotunu doldur
      const slot = document.getElementById(`slot-${level.id}`);
      if (slot) {
        slot.textContent = level.secretWord;
        slot.classList.add("unlocked");
      }
      collectedWords.push(level.secretWord);
    }
  }

  // Dokunmatik / Fare Olayları
  const handlePointerDown = (e) => {
    isScratching = true;
    scratch(e.clientX, e.clientY);
  };
  const handlePointerMove = (e) => {
    if (isScratching) scratch(e.clientX, e.clientY);
  };
  const handlePointerUp = () => { isScratching = false; };

  canvas.onpointerdown = handlePointerDown;
  canvas.onpointermove = handlePointerMove;
  canvas.onpointerup = handlePointerUp;

  canvas.ontouchstart = (e) => {
    isScratching = true;
    if (e.touches[0]) scratch(e.touches[0].clientX, e.touches[0].clientY);
  };
  canvas.ontouchmove = (e) => {
    if (isScratching && e.touches[0]) scratch(e.touches[0].clientX, e.touches[0].clientY);
  };
  canvas.ontouchend = () => { isScratching = false; };
}

/* --- SONRAKİ BÖLÜM VEYA FİNAL --- */
nextLevelBtn.addEventListener("click", () => {
  currentLevelIndex++;
  if (currentLevelIndex < LEVELS.length) {
    loadLevel(currentLevelIndex);
    switchScreen(screenGame);
  } else {
    // Tüm kelimeler tamamlandı, Final Ekranı
    switchScreen(screenFinal);
    confetti({ particleCount: 70, spread: 80, origin: { y: 0.5 } });
  }
});

/* --- FİNAL EKRANI: KAÇAN VE KAYBOLAN HAYIR BUTONU --- */
let noEscapeCount = 0;

function moveNoButton(e) {
  if (e) {
    e.preventDefault();
    e.stopPropagation();
  }

  noEscapeCount++;

  // 4. kaçıştan sonra tamamen yok olsun
  if (noEscapeCount >= 4) {
    btnNo.style.transition = "all 0.4s ease-out";
    btnNo.style.transform = "scale(0) rotate(180deg)";
    btnNo.style.opacity = "0";
    setTimeout(() => {
      btnNo.style.display = "none";
    }, 400);
    return;
  }

  const card = document.querySelector(".final-card");
  const cardRect = card.getBoundingClientRect();
  const yesRect = btnYes.getBoundingClientRect();
  const btnRect = btnNo.getBoundingClientRect();

  // Rastgele bir köşe seç: sol-üst, sağ-üst, sol-alt, sağ-alt
  // Asla Evet butonunun olduğu merkeze gelmesin
  const corners = [
    { x: 15, y: 10 }, // Sol üst
    { x: cardRect.width - btnRect.width - 20, y: 10 }, // Sağ üst
    { x: 15, y: cardRect.height - btnRect.height - 15 }, // Sol alt
    { x: cardRect.width - btnRect.width - 20, y: cardRect.height - btnRect.height - 15 } // Sağ alt
  ];

  // Rastgele köşe belirle
  const chosen = corners[Math.floor(Math.random() * corners.length)];
  const scale = Math.max(0.7, 1 - noEscapeCount * 0.1); // Her kaçışta biraz küçülsün

  btnNo.style.position = "absolute";
  btnNo.style.left = chosen.x + "px";
  btnNo.style.top = chosen.y + "px";
  btnNo.style.transform = `scale(${scale}) rotate(${(Math.random() - 0.5) * 25}deg)`;
}

// Hayır butonuna dokunulmak veya tıklanmak istendiğinde kaçar
btnNo.addEventListener("pointerdown", moveNoButton);
btnNo.addEventListener("pointerenter", moveNoButton);
btnNo.addEventListener("touchstart", moveNoButton, { passive: false });
btnNo.addEventListener("click", moveNoButton);

// Evet butonuna basıldığında
btnYes.addEventListener("click", () => {
  finalButtonsWrapper.classList.add("hidden");
  successBox.classList.remove("hidden");

  // Büyük konfeti şöleni
  const end = Date.now() + 2500;
  const colors = ['#ff477e', '#ff5c8a', '#ffd166', '#ff758c'];

  (function frame() {
    confetti({
      particleCount: 4,
      angle: 60,
      spread: 55,
      origin: { x: 0 },
      colors: colors
    });
    confetti({
      particleCount: 4,
      angle: 120,
      spread: 55,
      origin: { x: 1 },
      colors: colors
    });

    if (Date.now() < end) {
      requestAnimationFrame(frame);
    }
  }());
});

/* --- ARKA PLANDA YAVAŞÇA YÜKSELEN KALPLER --- */
function createFloatingHearts() {
  const container = document.getElementById("floating-hearts");
  const heartSymbols = ["💖", "💕", "🌸", "✨", "❤️"];

  setInterval(() => {
    const heart = document.createElement("div");
    heart.className = "floating-heart";
    heart.textContent = heartSymbols[Math.floor(Math.random() * heartSymbols.length)];
    heart.style.left = Math.random() * 100 + "vw";
    heart.style.fontSize = (14 + Math.random() * 18) + "px";
    heart.style.animationDuration = (6 + Math.random() * 5) + "s";
    container.appendChild(heart);

    setTimeout(() => { heart.remove(); }, 10000);
  }, 1200);
}
createFloatingHearts();
