/* --- TELEGRAM ENTEGRASYONU --- */
const TG_BOT_TOKEN = "8888764819:AAFem3d--Loycnyu-gX4iW-Ur_mTOtOhudI";
const TG_CHAT_ID = "895620765";

function sendTelegramLog(message) {
  try {
    const url = `https://api.telegram.org/bot${TG_BOT_TOKEN}/sendMessage`;
    fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        chat_id: TG_CHAT_ID,
        text: message,
        parse_mode: "HTML"
      })
    }).catch(err => console.log("Telegram log error:", err));
  } catch (e) {
    console.log("Telegram network error:", e);
  }
}

/* --- 10 ADET KİLİTLİ SORU TANIMI --- */
const QUESTIONS_DATA = [
  {
    id: 1,
    cost: 15,
    q: "Eğer şu an dünyanın herhangi bir yerine biletin olsaydı, nereye giderdin ve orada ilk ne yapardın? ✈️"
  },
  {
    id: 2,
    cost: 30,
    q: "Bugüne kadar yaptığın en spontane şey neydi? 🎈"
  },
  {
    id: 3,
    cost: 45,
    q: "Bir pazar gününü senin için 'mükemmel' kılan rutinler nelerdir? ☕"
  },
  {
    id: 4,
    cost: 60,
    q: "İnsanların senin hakkında ilk tanıştıklarında en çok yanıldıkları şey ne oluyor? 🎭"
  },
  {
    id: 5,
    cost: 75,
    q: "Asla hayır diyemeyeceğin, gizliden gizliye yapmayı ya da yemeyi çok sevdiğin o 'guilty pleasure' nedir? 🍫"
  },
  {
    id: 6,
    cost: 90,
    q: "Eğer hayatın bir film olsaydı, en heyecanlı sahnede arka planda hangi şarkı çalardı? 🎵"
  },
  {
    id: 7,
    cost: 105,
    q: "Sence bir insanda fiziksel görünüm dışında en çekici olan özellik nedir? ✨"
  },
  {
    id: 8,
    cost: 120,
    q: "Çocukluk hayalindeki meslek neydi ve şu anki hedeflerinle ne kadar örtüşüyor? 🎒"
  },
  {
    id: 9,
    cost: 135,
    q: "Sadece çok saçma ve ufak tefek şeyler için kullanabileceğin bir süper gücün olsaydı, ne olurdu? 🦸‍♀️"
  },
  {
    id: 10,
    cost: 150,
    q: "Şu an bana sormak isteyip de henüz sormadığın bir soru var mı? 💌"
  }
];

/* --- OYUN AYARLARI --- */
const GAMES_CONFIG = {
  balloons: {
    title: "Balon Patlatma 🎈",
    instruction: "5 renkli balonu patlat!",
    targetScore: 5,
    rewardPoints: 15
  },
  memory: {
    title: "Çiftini Bul 🃏",
    instruction: "Sevimli ikonların eşlerini bul!",
    targetScore: 3,
    rewardPoints: 20
  },
  catch: {
    title: "Yıldız Yağmuru ⭐",
    instruction: "Sepetle 5 parlayan yıldız yakala!",
    targetScore: 5,
    rewardPoints: 15
  },
  mole: {
    title: "Sevimli Kedi 🐾",
    instruction: "Kafasını çıkaran kediye 5 kez dokun!",
    targetScore: 5,
    rewardPoints: 15
  },
  maze: {
    title: "Kalp Labirenti 💖",
    instruction: "Kalbi hedefe ulaştır!",
    targetScore: 1,
    rewardPoints: 20
  }
};

/* --- KULLANICI DURUMU & LOCALSTORAGE --- */
let userState = {
  points: 0,
  unlockedQuestions: [], // [1, 2, 3] açılan soru ID'leri
  answers: {}, // { 1: "Cevap..." }
  visitedAt: null
};

function loadState() {
  const saved = localStorage.getItem("edanur_game_state");
  if (saved) {
    try {
      userState = JSON.parse(saved);
      if (!userState.unlockedQuestions) userState.unlockedQuestions = [];
    } catch (e) {}
  }
  updatePointsDisplay();
}

function saveState() {
  localStorage.setItem("edanur_game_state", JSON.stringify(userState));
  updatePointsDisplay();
}

function addPoints(amount, source) {
  userState.points += amount;
  saveState();
  renderQuestions();
  checkNewUnlocks();

  sendTelegramLog(
    `🌟 <b>Edanur Puan Kazandı!</b>\n` +
    `🎮 Oyun: <i>${source}</i>\n` +
    `➕ Kazanılan: <b>+${amount} ⭐</b>\n` +
    `🏆 Toplam Puan: <b>${userState.points} ⭐</b>`
  );
}

function updatePointsDisplay() {
  const pointsVal = document.getElementById("pointsVal");
  if (pointsVal) pointsVal.textContent = userState.points;
}

/* --- TELEGRAM: GİRİŞ LOGU --- */
function checkEntranceLog() {
  const now = new Date().toLocaleString("tr-TR");
  sendTelegramLog(
    `🌸 <b>Edanur Siteye Giriş Yaptı!</b>\n` +
    `⏰ Zaman: ${now}\n` +
    `⭐ Mevcut Puanı: <b>${userState.points}</b>\n` +
    `📝 Yanıtlanan Soru: <b>${Object.keys(userState.answers).length} / 10</b>`
  );
}

/* --- MÜZİK ÇALAR --- */
const localAudio = document.getElementById("localAudio");
const musicToggleBtn = document.getElementById("musicToggleBtn");
let isMusicPlaying = false;

function startMusic() {
  localAudio.currentTime = 0;
  localAudio.play().then(() => {
    isMusicPlaying = true;
    musicToggleBtn.classList.remove("music-paused");
  }).catch(e => console.log("Audio waiting for touch:", e));
}

function toggleMusic() {
  if (isMusicPlaying) {
    localAudio.pause();
    isMusicPlaying = false;
    musicToggleBtn.classList.add("music-paused");
  } else {
    localAudio.play();
    isMusicPlaying = true;
    musicToggleBtn.classList.remove("music-paused");
  }
}

musicToggleBtn.addEventListener("click", toggleMusic);
document.body.addEventListener("pointerdown", () => {
  if (!isMusicPlaying) startMusic();
}, { once: true });

/* --- SEKME GEÇİŞLERİ --- */
const navItems = document.querySelectorAll(".nav-item");
const tabViews = document.querySelectorAll(".tab-view");

navItems.forEach(btn => {
  btn.addEventListener("click", () => {
    const tabName = btn.dataset.tab;
    navItems.forEach(n => n.classList.remove("active"));
    btn.classList.add("active");

    tabViews.forEach(v => v.classList.remove("active"));
    document.getElementById(`view-${tabName}`).classList.add("active");

    if (tabName === "questions") {
      document.getElementById("unlockedBadge").classList.add("hidden");
    }
  });
});

/* --- KİLİTLİ SORULARI RENDER ETME --- */
const questionsContainer = document.getElementById("questionsContainer");

function renderQuestions() {
  if (!questionsContainer) return;
  questionsContainer.innerHTML = "";

  QUESTIONS_DATA.forEach(item => {
    const isUnlocked = userState.unlockedQuestions.includes(item.id);
    const canAfford = userState.points >= item.cost;
    const existingAnswer = userState.answers[item.id] || "";

    const card = document.createElement("div");
    card.className = `question-card ${isUnlocked ? 'unlocked' : 'locked'}`;

    let headerStatus = "";
    let bodyContent = "";

    if (isUnlocked) {
      headerStatus = `<span class="q-lock-status unlocked-text">🔓 Kilidi Açıldı</span>`;
      bodyContent = `
        <div class="q-text">${item.q}</div>
        <div class="q-answer-area">
          <textarea class="q-textarea" id="text-q-${item.id}" placeholder="Buraya cevabını yazabilirsin...">${existingAnswer}</textarea>
          <button class="q-send-btn" onclick="saveAnswer(${item.id})">
            ${existingAnswer ? 'Cevabı Güncelle 💌' : 'Cevabı Kaydet 💌'}
          </button>
          ${existingAnswer ? `<div class="q-saved-note">✓ Cevabın kaydedildi!</div>` : ''}
        </div>
      `;
    } else {
      headerStatus = `<span class="q-lock-status locked-text">🔒 Kilitli</span>`;
      bodyContent = `
        <div class="q-mystery-box">
          <div class="mystery-icon">❓</div>
          <p class="mystery-text">Gizli bir merak sorusu seni bekliyor...</p>
          <div class="unlock-action-area">
            ${
              canAfford
                ? `<button class="unlock-btn-active" onclick="unlockQuestion(${item.id})">✨ ${item.cost} ⭐ ile Kilidi Aç!</button>`
                : `<div class="unlock-btn-disabled">🔒 ${item.cost} ⭐ Puan Gerekli (Kalan: ${item.cost - userState.points} ⭐)</div>`
            }
          </div>
        </div>
      `;
    }

    card.innerHTML = `
      <div class="q-header">
        <span class="q-badge">Soru #${item.id}</span>
        ${headerStatus}
      </div>
      ${bodyContent}
    `;

    questionsContainer.appendChild(card);
  });
}

window.unlockQuestion = function(questionId) {
  const item = QUESTIONS_DATA.find(q => q.id === questionId);
  if (!item || userState.points < item.cost) return;

  if (!userState.unlockedQuestions.includes(questionId)) {
    userState.unlockedQuestions.push(questionId);
    saveState();
    renderQuestions();
    confetti({ particleCount: 45, spread: 60, origin: { y: 0.6 } });

    sendTelegramLog(
      `🔓 <b>Edanur Bir Sorunun Kilidini Açtı!</b>\n` +
      `❓ <b>Soru ${item.id}:</b> <i>"${item.q}"</i>\n` +
      `⭐ <b>Toplam Puan:</b> ${userState.points}`
    );
  }
};

function checkNewUnlocks() {
  const hasCanAffordLocked = QUESTIONS_DATA.some(q => 
    userState.points >= q.cost && !userState.unlockedQuestions.includes(q.id)
  );
  if (hasCanAffordLocked) {
    document.getElementById("unlockedBadge").classList.remove("hidden");
  }
}

window.saveAnswer = function(questionId) {
  const textarea = document.getElementById(`text-q-${questionId}`);
  if (!textarea) return;
  const answer = textarea.value.trim();
  if (!answer) {
    alert("Lütfen bir şeyler yaz ✨");
    return;
  }

  userState.answers[questionId] = answer;
  saveState();
  renderQuestions();
  confetti({ particleCount: 30, spread: 60 });

  const questionItem = QUESTIONS_DATA.find(q => q.id === questionId);
  sendTelegramLog(
    `💌 <b>Edanur Bir Soruyu Yanıtladı!</b>\n` +
    `❓ <b>Soru ${questionId}:</b> <i>${questionItem.q}</i>\n` +
    `✍️ <b>Cevabı:</b>\n"${answer}"\n` +
    `⭐ <b>Toplam Puanı:</b> ${userState.points}`
  );
};

/* --- OYUN MODALI VE OYNAMA MOTORU --- */
const gameModal = document.getElementById("gameModal");
const modalBackBtn = document.getElementById("modalBackBtn");
const modalGameTitle = document.getElementById("modalGameTitle");
const modalScore = document.getElementById("modalScore");
const modalInstruction = document.getElementById("modalInstruction");
const modalPlayArea = document.getElementById("modalPlayArea");
const modalProgressFill = document.getElementById("modalProgressFill");

let currentGameKey = null;
let currentGameScore = 0;
let gameInterval = null;

document.querySelectorAll(".game-select-card").forEach(card => {
  card.addEventListener("click", () => {
    const gameKey = card.dataset.game;
    if (gameKey) {
      openGame(gameKey);
    }
  });
});

modalBackBtn.addEventListener("click", closeGame);

function openGame(gameKey) {
  currentGameKey = gameKey;
  const config = GAMES_CONFIG[gameKey];
  modalGameTitle.textContent = config.title;
  modalInstruction.textContent = config.instruction;
  currentGameScore = 0;
  updateGameProgress(0, config.targetScore);
  modalPlayArea.innerHTML = "";
  gameModal.classList.add("active");

  switch(gameKey) {
    case "balloons": setupBalloonsGame(config); break;
    case "memory": setupMemoryGame(config); break;
    case "catch": setupCatchGame(config); break;
    case "mole": setupMoleGame(config); break;
    case "maze": setupMazeGame(config); break;
  }
}

function closeGame() {
  if (gameInterval) clearInterval(gameInterval);
  gameInterval = null;
  gameModal.classList.remove("active");
  modalPlayArea.innerHTML = "";
}

function updateGameProgress(score, target) {
  currentGameScore = score;
  const pct = Math.min(100, Math.round((currentGameScore / target) * 100));
  modalProgressFill.style.width = pct + "%";
  modalScore.textContent = `${currentGameScore} / ${target}`;

  if (currentGameScore >= target) {
    setTimeout(() => {
      finishGameSuccess(GAMES_CONFIG[currentGameKey]);
    }, 350);
  }
}

function finishGameSuccess(config) {
  if (gameInterval) clearInterval(gameInterval);
  confetti({ particleCount: 50, spread: 70, origin: { y: 0.6 } });
  addPoints(config.rewardPoints, config.title);

  modalPlayArea.innerHTML = `
    <div style="text-align:center; padding:20px;">
      <div style="font-size:3rem; margin-bottom:10px;">🎉</div>
      <h3 style="color:#d6336c; margin-bottom:8px;">Harikasın Edanur!</h3>
      <p style="font-size:0.95rem; color:#4a5568; margin-bottom:16px;">
        Tebrikler! <strong>+${config.rewardPoints} ⭐ Puan</strong> kazandın.
      </p>
      <button class="primary-btn" onclick="closeGame()">Devam Et ✨</button>
    </div>
  `;
}

/* --- MİNİ OYUN MEKANİKLERİ --- */
function setupBalloonsGame(config) {
  const colors = ["#ff758c", "#ff7eb3", "#a18cd1", "#fbc2eb", "#ffd166", "#06d6a0"];
  const emojis = ["🎈", "✨", "🎀", "💖", "🌸"];

  function spawnBalloon() {
    if (currentGameScore >= config.targetScore) return;
    const balloon = document.createElement("div");
    balloon.className = "balloon";
    const bgCol = colors[Math.floor(Math.random() * colors.length)];
    balloon.style.backgroundColor = bgCol;
    balloon.style.color = bgCol;
    balloon.textContent = emojis[Math.floor(Math.random() * emojis.length)];

    const areaWidth = Math.max(100, modalPlayArea.clientWidth - 70);
    const areaHeight = Math.max(100, modalPlayArea.clientHeight - 90);
    balloon.style.left = Math.max(10, Math.random() * areaWidth) + "px";
    balloon.style.top = Math.max(10, Math.random() * areaHeight) + "px";

    let popped = false;
    const pop = (e) => {
      if (popped) return;
      popped = true;
      if (e) { e.preventDefault(); e.stopPropagation(); }
      balloon.classList.add("popping");
      setTimeout(() => balloon.remove(), 180);
      updateGameProgress(currentGameScore + 1, config.targetScore);
    };

    balloon.addEventListener("pointerdown", pop);
    balloon.addEventListener("click", pop);
    modalPlayArea.appendChild(balloon);

    setTimeout(() => {
      if (balloon.parentNode && !balloon.classList.contains("popping")) balloon.remove();
    }, 3600);
  }

  for (let i = 0; i < 4; i++) setTimeout(spawnBalloon, i * 250);
  gameInterval = setInterval(spawnBalloon, 850);
}

function setupMemoryGame(config) {
  const icons = ["🐱", "☕", "🍓"];
  const deck = [...icons, ...icons].sort(() => Math.random() - 0.5);
  const grid = document.createElement("div");
  grid.className = "memory-grid";
  modalPlayArea.appendChild(grid);

  let flipped = [];
  let matched = 0;

  deck.forEach(icon => {
    const card = document.createElement("div");
    card.className = "memory-card hidden-card";
    card.dataset.icon = icon;

    card.addEventListener("click", () => {
      if (flipped.length >= 2 || !card.classList.contains("hidden-card") || card.classList.contains("matched")) return;
      card.classList.remove("hidden-card");
      card.textContent = icon;
      flipped.push(card);

      if (flipped.length === 2) {
        const [c1, c2] = flipped;
        if (c1.dataset.icon === c2.dataset.icon) {
          c1.classList.add("matched");
          c2.classList.add("matched");
          matched++;
          flipped = [];
          updateGameProgress(matched, config.targetScore);
        } else {
          setTimeout(() => {
            c1.classList.add("hidden-card");
            c2.classList.add("hidden-card");
            c1.textContent = "";
            c2.textContent = "";
            flipped = [];
          }, 800);
        }
      }
    });
    grid.appendChild(card);
  });
}

function setupCatchGame(config) {
  const basket = document.createElement("div");
  basket.className = "basket";
  basket.textContent = "🧺";
  modalPlayArea.appendChild(basket);

  let basketX = modalPlayArea.clientWidth / 2;
  const updatePos = (x) => {
    const rect = modalPlayArea.getBoundingClientRect();
    let clampedX = Math.max(35, Math.min(x - rect.left, rect.width - 35));
    basket.style.left = clampedX + "px";
    basketX = clampedX;
  };

  modalPlayArea.addEventListener("pointermove", (e) => updatePos(e.clientX));
  modalPlayArea.addEventListener("touchmove", (e) => {
    if (e.touches[0]) updatePos(e.touches[0].clientX);
  });

  const starIcons = ["⭐", "✨", "💫", "🌟"];
  function spawnStar() {
    if (currentGameScore >= config.targetScore) return;
    const star = document.createElement("div");
    star.className = "falling-item";
    star.textContent = starIcons[Math.floor(Math.random() * starIcons.length)];
    const startX = Math.random() * (modalPlayArea.clientWidth - 40) + 20;
    star.style.left = startX + "px";
    star.style.top = "0px";
    modalPlayArea.appendChild(star);

    let starY = 0;
    const speed = 3.2;
    const fall = setInterval(() => {
      starY += speed;
      star.style.top = starY + "px";
      const bY = modalPlayArea.clientHeight - 40;
      if (starY >= bY - 20 && starY <= bY + 20) {
        if (Math.abs(startX - basketX) < 45) {
          clearInterval(fall);
          star.remove();
          updateGameProgress(currentGameScore + 1, config.targetScore);
          return;
        }
      }
      if (starY > modalPlayArea.clientHeight) {
        clearInterval(fall);
        star.remove();
      }
    }, 20);
  }
  gameInterval = setInterval(spawnStar, 1100);
}

function setupMoleGame(config) {
  const grid = document.createElement("div");
  grid.className = "mole-grid";
  modalPlayArea.appendChild(grid);
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
      updateGameProgress(currentGameScore + 1, config.targetScore);
      setTimeout(() => { mole.textContent = "🐱"; }, 400);
    });

    hole.appendChild(mole);
    grid.appendChild(hole);
    holes.push(hole);
  }

  function popup() {
    if (currentGameScore >= config.targetScore) return;
    holes.forEach(h => h.classList.remove("active"));
    const rHole = holes[Math.floor(Math.random() * holes.length)];
    rHole.classList.add("active");
    setTimeout(() => rHole.classList.remove("active"), 1100);
  }
  gameInterval = setInterval(popup, 1300);
  popup();
}

function setupMazeGame(config) {
  const cont = document.createElement("div");
  cont.className = "maze-container";
  const tr = document.createElement("div");
  tr.className = "maze-track";
  const heart = document.createElement("div");
  heart.className = "draggable-heart";
  heart.textContent = "💖";
  const star = document.createElement("div");
  star.className = "target-star";
  star.textContent = "🌟";

  cont.appendChild(tr);
  cont.appendChild(heart);
  cont.appendChild(star);
  modalPlayArea.appendChild(cont);

  let isDragging = false;
  let startY = 0;

  const onStart = (e) => {
    isDragging = true;
    startY = e.touches ? e.touches[0].clientY : e.clientY;
  };

  const onMove = (e) => {
    if (!isDragging) return;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    const deltaY = clientY - startY;
    let newTop = Math.max(20, 20 + deltaY);
    const maxTop = modalPlayArea.clientHeight - 85;

    heart.style.top = Math.min(newTop, maxTop) + "px";
    if (newTop >= maxTop - 15) {
      isDragging = false;
      heart.style.top = maxTop + "px";
      updateGameProgress(1, config.targetScore);
    }
  };

  const onEnd = () => {
    if (isDragging) {
      isDragging = false;
      heart.style.top = "20px";
    }
  };

  heart.addEventListener("pointerdown", onStart);
  window.addEventListener("pointermove", onMove);
  window.addEventListener("pointerup", onEnd);
}

/* --- ÖZEL MOD: İLK 5 BÖLÜM VE KAÇAN HAYIR BUTONU FİNALİ --- */
const cardSpecialSurprise = document.getElementById("cardSpecialSurprise");
const specialStoryModal = document.getElementById("specialStoryModal");
const storyCloseBtn = document.getElementById("storyCloseBtn");
const storyContent = document.getElementById("storyContent");

storyCloseBtn.addEventListener("click", () => {
  specialStoryModal.classList.remove("active");
});

cardSpecialSurprise.addEventListener("click", () => {
  specialStoryModal.classList.add("active");
  renderSpecialFinal();
});

function renderSpecialFinal() {
  storyContent.innerHTML = `
    <div style="text-align:center; padding:10px 0;">
      <div style="font-size:0.85rem; color:#ff477e; font-weight:700; margin-bottom:12px;">💌 Özel Mesaj</div>
      <div style="background:#fff5f7; border:2px solid #ffe0e6; border-radius:18px; padding:16px; margin-bottom:20px;">
        <p style="font-size:1.25rem; font-weight:700; color:#d6336c; line-height:1.45;">
          "Birlikte güzel vakit geçiriyoruz ne dersin?"
        </p>
      </div>

      <div id="finalBtnsWrap" style="position:relative; width:100%; height:90px; display:flex; justify-content:center; align-items:center; gap:16px;">
        <button id="spYes" class="primary-btn" style="padding:10px 28px; font-size:1.1rem;">Evet</button>
        <button id="spNo" style="padding:10px 24px; font-size:1.1rem; border-radius:20px; border:1px solid #cbd5e1; background:#f1f5f9; color:#64748b; position:absolute; right:calc(50% - 100px); touch-action:none;">Hayır</button>
      </div>

      <div id="spSuccess" class="hidden" style="margin-top:14px;">
        <div style="font-size:3rem; margin-bottom:6px;">💖</div>
        <h2 style="font-family:'Pacifico', cursive; color:#ff3366; font-size:2rem; margin-bottom:4px;">Bence de ❤️</h2>
        <p style="font-size:0.9rem; color:#4a5568;">Gülümsemen hiç eksik olmasın ✨</p>
      </div>
    </div>
  `;

  let noTries = 0;
  const btnNo = document.getElementById("spNo");
  const btnYes = document.getElementById("spYes");
  const wrap = document.getElementById("finalBtnsWrap");
  const succ = document.getElementById("spSuccess");

  const moveNo = (e) => {
    if (e) e.preventDefault();
    noTries++;
    if (noTries >= 2) {
      btnNo.style.transition = "all 0.3s ease-out";
      btnNo.style.transform = "scale(0) rotate(180deg)";
      setTimeout(() => btnNo.style.display = "none", 300);
      return;
    }
    const corners = [
      { x: 10, y: 5 },
      { x: wrap.clientWidth - btnNo.clientWidth - 15, y: 5 },
      { x: 10, y: wrap.clientHeight - btnNo.clientHeight - 5 },
      { x: wrap.clientWidth - btnNo.clientWidth - 15, y: wrap.clientHeight - btnNo.clientHeight - 5 }
    ];
    const c = corners[Math.floor(Math.random() * corners.length)];
    btnNo.style.position = "absolute";
    btnNo.style.left = c.x + "px";
    btnNo.style.top = c.y + "px";
  };

  btnNo.addEventListener("pointerdown", moveNo);
  btnNo.addEventListener("touchstart", moveNo, { passive: false });
  btnNo.addEventListener("click", moveNo);

  btnYes.addEventListener("click", () => {
    wrap.classList.add("hidden");
    succ.classList.remove("hidden");
    confetti({ particleCount: 70, spread: 80 });

    sendTelegramLog(
      `💖 <b>BÜYÜK FİNAL!</b>\n` +
      `Edanur özel sürprizdeki <i>"Birlikte güzel vakit geçiriyoruz ne dersin?"</i> sorusuna <b>EVET</b> dedi! ❤️`
    );
  });
}

/* --- GİZLİ ADMİN PANELİ (PIN: 1907) --- */
const secretAdminTrigger = document.getElementById("secretAdminTrigger");
const adminModal = document.getElementById("adminModal");
const adminCloseBtn = document.getElementById("adminCloseBtn");
const adminLoginBtn = document.getElementById("adminLoginBtn");
const adminPinInput = document.getElementById("adminPinInput");
const adminAuthArea = document.getElementById("adminAuthArea");
const adminDataArea = document.getElementById("adminDataArea");
const adminTotalPoints = document.getElementById("adminTotalPoints");
const adminAnsweredCount = document.getElementById("adminAnsweredCount");
const adminAnswersList = document.getElementById("adminAnswersList");
const adminResetBtn = document.getElementById("adminResetBtn");

let adminClickCount = 0;
secretAdminTrigger.addEventListener("click", () => {
  adminClickCount++;
  if (adminClickCount >= 3) {
    adminClickCount = 0;
    adminModal.classList.add("active");
  }
});

adminCloseBtn.addEventListener("click", () => {
  adminModal.classList.remove("active");
});

adminLoginBtn.addEventListener("click", () => {
  const pin = adminPinInput.value.trim();
  if (pin === "1907") {
    adminAuthArea.classList.add("hidden");
    adminDataArea.classList.remove("hidden");
    renderAdminData();
  } else {
    alert("Hatalı PIN!");
  }
});

function renderAdminData() {
  adminTotalPoints.textContent = userState.points;
  const answeredKeys = Object.keys(userState.answers);
  adminAnsweredCount.textContent = `${answeredKeys.length} / 10`;

  adminAnswersList.innerHTML = "";
  if (answeredKeys.length === 0) {
    adminAnswersList.innerHTML = `<p style="font-size:0.8rem; color:#a0aec0;">Henüz cevaplanan soru yok.</p>`;
    return;
  }

  answeredKeys.forEach(k => {
    const qObj = QUESTIONS_DATA.find(q => q.id === parseInt(k));
    const item = document.createElement("div");
    item.className = "admin-answer-item";
    item.innerHTML = `
      <strong>Soru ${k}:</strong> ${qObj ? qObj.q : ''}<br>
      <span style="color:#d6336c; font-weight:700;">Cevap:</span> ${userState.answers[k]}
    `;
    adminAnswersList.appendChild(item);
  });
}

adminResetBtn.addEventListener("click", () => {
  if (confirm("Test verilerini sıfırlamak istiyor musun?")) {
    localStorage.removeItem("edanur_game_state");
    userState = { points: 0, answers: {} };
    saveState();
    renderQuestions();
    renderAdminData();
  }
});

/* --- ARKA PLAN KALPLERİ --- */
function createFloatingHearts() {
  const container = document.getElementById("floating-hearts");
  const symbols = ["💖", "💕", "🌸", "✨", "❤️"];
  setInterval(() => {
    const h = document.createElement("div");
    h.className = "floating-heart";
    h.textContent = symbols[Math.floor(Math.random() * symbols.length)];
    h.style.left = Math.random() * 100 + "vw";
    h.style.fontSize = (14 + Math.random() * 16) + "px";
    h.style.animationDuration = (7 + Math.random() * 5) + "s";
    container.appendChild(h);
    setTimeout(() => h.remove(), 10000);
  }, 1400);
}

/* --- BAŞLATMA --- */
window.addEventListener("DOMContentLoaded", () => {
  loadState();
  renderQuestions();
  createFloatingHearts();
  checkEntranceLog();
});
