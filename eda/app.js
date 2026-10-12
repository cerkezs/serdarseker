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
  ninja: {
    title: "Meyve Kesmece 🍓",
    instruction: "Parmağınla fırlayan 6 meyveyi dilimle!",
    targetScore: 6,
    rewardPoints: 20
  },
  flappy: {
    title: "Uçan Kalp 🕊️",
    instruction: "Ekrana dokunarak kalbi 20 buluttan geçir!",
    targetScore: 20,
    rewardPoints: 20
  },
  piano: {
    title: "Ritim Notaları 🎹",
    instruction: "Sadece 🎵 notalarına dokun (20 Tane)! Diğerlerine basarsan veya kaçırırsan yanarsın!",
    targetScore: 20,
    rewardPoints: 20
  },
  memory: {
    title: "Çiftini Bul 🃏",
    instruction: "Sevimli ikonların eşlerini bul!",
    targetScore: 3,
    rewardPoints: 20
  },
  catch: {
    title: "Yıldız Yağmuru ⭐",
    instruction: "Sepetle 20 altın yıldız (⭐) yakala! Bombalara (💣) çarparsan yanarsın!",
    targetScore: 20,
    rewardPoints: 20
  },
  mole: {
    title: "Sevimli Kedi 🐾",
    instruction: "Kafasını çıkaran kediye 5 kez dokun!",
    targetScore: 5,
    rewardPoints: 15
  },
  wheel: {
    title: "Şans Çarkıfeleği 🎡",
    instruction: "Çarkı çevir ve sürpriz yıldızları kap!",
    targetScore: 1,
    rewardPoints: 20
  },
  color: {
    title: "Renk Tuzağı 🧠",
    instruction: "Kelimenin anlamına değil, yazıldığı renge bas! (15 Seri Yap!)",
    targetScore: 15,
    rewardPoints: 20
  },
  numbers: {
    title: "Sayı Avı 🔢",
    instruction: "12 saniyede 1'den 16'ya kadar sırayla bas!",
    targetScore: 16,
    rewardPoints: 20
  },
  pin: {
    title: "Dönen Hedef 🎯",
    instruction: "12 iğneyi birbirine çarptırmadan hedefe sapla!",
    targetScore: 12,
    rewardPoints: 20
  }
};

/* --- KULLANICI ADI & DURUMU & LOCALSTORAGE --- */
let currentUsername = localStorage.getItem("eda_active_username") || "";

let userState = {
  username: "Edanur",
  points: 0,
  unlockedQuestions: [], // [1, 2, 3] açılan soru ID'leri
  answers: {}, // { 1: "Cevap..." }
  askedToSerdar: [], // [ { id: 101, q: "...", a: null, date: "..." } ]
  visitedAt: null
};

let lastTgUpdateId = 0;

/* --- BULUT VERİTABANI (KVDB.IO - DİNAMİK KULLANICI BAZLI) --- */
const CLOUD_BASE_URL = "https://kvdb.io/LzCGBkLwZ3v6g6R4qP9h6K/";
const USERS_LIST_KEY = "eda_all_registered_users";

function getUserStorageKey(name) {
  const safeName = (name || "edanur").trim().toLowerCase().replace(/[^a-z0-9_-]/g, "_");
  return `eda_user_${safeName}`;
}

// Kullanıcı Kimliği Belirleme (Serdar Admin mi yoksa Oyuncu mu?)
let userRole = localStorage.getItem("serdar_role") || "player";

function syncStateToCloud() {
  if (userRole === "serdar_admin") return; // Serdar admin modundayken kullanıcının verilerini ezmez!
  const userKey = getUserStorageKey(currentUsername || "edanur");
  try {
    userState.username = currentUsername || "Edanur";
    userState.lastActive = new Date().toLocaleString("tr-TR");

    // 1. Kullanıcının kendi verisini buluta yaz
    fetch(CLOUD_BASE_URL + userKey, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userState)
    }).catch(e => console.log("Cloud sync err:", e));

    // 2. Kullanıcıyı global listeye kaydet (Admin paneli için)
    registerUserToGlobalList(userState.username);
  } catch (e) {}
}

function registerUserToGlobalList(name) {
  if (!name) return;
  fetch(CLOUD_BASE_URL + USERS_LIST_KEY)
    .then(res => res.json())
    .catch(() => [])
    .then(list => {
      let users = Array.isArray(list) ? list : [];
      if (!users.includes(name)) {
        users.push(name);
        fetch(CLOUD_BASE_URL + USERS_LIST_KEY, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(users)
        }).catch(() => {});
      }
    });
}

function loadStateFromCloud(targetUser, callback) {
  const userKey = getUserStorageKey(targetUser || currentUsername || "edanur");
  fetch(CLOUD_BASE_URL + userKey)
    .then(res => res.json())
    .then(data => {
      if (data && typeof data === "object") {
        if (callback) callback(data);
      } else {
        if (callback) callback(null);
      }
    })
    .catch(() => {
      if (callback) callback(null);
    });
}

function loadState() {
  const saved = localStorage.getItem("edanur_game_state");
  if (saved) {
    try {
      userState = JSON.parse(saved);
      if (!userState.unlockedQuestions) userState.unlockedQuestions = [];
      if (!userState.askedToSerdar) userState.askedToSerdar = [];
    } catch (e) {}
  }
  updatePointsDisplay();
  renderAskedQuestions();

  // Eğer kullanıcı adı varsa buluttan son verisini çekip eşitle
  if (currentUsername && userRole !== "serdar_admin") {
    loadStateFromCloud(currentUsername, (cloudData) => {
      if (cloudData && typeof cloudData === "object") {
        // En yüksek puan veya güncel cevapları koru
        if ((cloudData.points || 0) > userState.points) {
          userState.points = cloudData.points;
        }
        userState.unlockedQuestions = Array.from(new Set([...(userState.unlockedQuestions || []), ...(cloudData.unlockedQuestions || [])]));
        userState.answers = { ...(userState.answers || {}), ...(cloudData.answers || {}) };
        if (Array.isArray(cloudData.askedToSerdar) && cloudData.askedToSerdar.length > 0) {
          userState.askedToSerdar = cloudData.askedToSerdar;
        }
        localStorage.setItem("edanur_game_state", JSON.stringify(userState));
        updatePointsDisplay();
        renderQuestions();
        renderAskedQuestions();
      }
    });
  }
}

function saveState() {
  localStorage.setItem("edanur_game_state", JSON.stringify(userState));
  updatePointsDisplay();
  syncStateToCloud();
}

let isPollingTg = false;

/* --- TELEGRAM CANLI CEVAP DİNLEME (POLLING) --- */
function pollTelegramReplies() {
  if (isPollingTg) return;
  // Sadece Serdar'a Sor sekmesindeyken veya cevapsız soru varken kontrol et
  const hasUnanswered = userState.askedToSerdar && userState.askedToSerdar.some(item => !item.a);
  if (!hasUnanswered) return;

  isPollingTg = true;
  const url = `https://api.telegram.org/bot${TG_BOT_TOKEN}/getUpdates?offset=${lastTgUpdateId + 1}&limit=5`;
  fetch(url)
    .then(res => {
      isPollingTg = false;
      if (!res.ok) return null;
      return res.json();
    })
    .catch(() => {
      isPollingTg = false;
      return null;
    })
    .then(data => {
      if (data && data.ok && data.result && data.result.length > 0) {
        data.result.forEach(update => {
          lastTgUpdateId = update.update_id;
          const msg = update.message;
          if (!msg || !msg.text) return;

          let answerText = msg.text.trim();
          let targetQuestionId = null;

          if (msg.reply_to_message && msg.reply_to_message.text) {
            const replyOrigin = msg.reply_to_message.text;
            const match = replyOrigin.match(/ID:\s*#(\d+)/i);
            if (match) targetQuestionId = parseInt(match[1]);
          }

          if (!targetQuestionId) {
            const unanswered = userState.askedToSerdar.filter(item => !item.a);
            if (unanswered.length > 0) {
              targetQuestionId = unanswered[unanswered.length - 1].id;
            }
          }

          if (targetQuestionId) {
            const qItem = userState.askedToSerdar.find(i => i.id === targetQuestionId);
            if (qItem && !qItem.a) {
              qItem.a = answerText;
              saveState();
              renderAskedQuestions();
              confetti({ particleCount: 50, spread: 70 });
              document.getElementById("newAnswerBadge").classList.remove("hidden");
            }
          }
        });
      }
    });
}

// 12 saniyede bir sakin ve kontrollü kontrol et
setInterval(pollTelegramReplies, 12000);

/* --- SERDAR'A SOR GÖNDERME MANTIĞI --- */
const askInput = document.getElementById("askInput");
const sendQuestionToSerdarBtn = document.getElementById("sendQuestionToSerdarBtn");
const askedQuestionsList = document.getElementById("askedQuestionsList");

if (sendQuestionToSerdarBtn) {
  sendQuestionToSerdarBtn.addEventListener("click", () => {
    const questionText = askInput.value.trim();
    if (!questionText) {
      alert("Lütfen sormak istediğin bir soru yaz ✨");
      return;
    }

    if (userState.points < 20) {
      alert(`Bu soruyu sormak için 20 ⭐ Puan gerekli! Şu an ${userState.points} puanın var. Biraz oyun oynayıp gelebilirsin 🎮`);
      return;
    }

    // 20 Puan düş
    userState.points -= 20;
    const newId = Date.now();
    const newEntry = {
      id: newId,
      q: questionText,
      a: null,
      date: new Date().toLocaleDateString("tr-TR", { hour: "2-digit", minute: "2-digit" })
    };

    userState.askedToSerdar.unshift(newEntry);
    saveState();
    askInput.value = "";
    renderAskedQuestions();
    confetti({ particleCount: 35, spread: 50 });

    // Telegram'a Serdar için bildirim gönder
    sendTelegramLog(
      `❓ <b>EDANUR SANA BİR SORU SORDU!</b> 💌\n\n` +
      `✍️ <b>Soru:</b> <i>"${questionText}"</i>\n\n` +
      `🆔 ID: #${newId}\n` +
      `💡 <i>Cevaplamak için bu mesaja doğrudan Telegram'dan <b>Yanıtla (Reply)</b> yap ve cevabını yaz!</i>`
    );
  });
}

function renderAskedQuestions() {
  if (!askedQuestionsList) return;
  askedQuestionsList.innerHTML = "";

  if (userState.askedToSerdar.length === 0) {
    askedQuestionsList.innerHTML = `
      <div style="text-align:center; padding:16px; color:#a0aec0; font-size:0.85rem;">
        Henüz Serdar'a bir soru sormadın. Aklına ne geliyorsa çekinmeden sorabilirsin! ✨
      </div>
    `;
    return;
  }

  userState.askedToSerdar.forEach(item => {
    const card = document.createElement("div");
    card.className = "asked-item-card";

    let answerHtml = item.a
      ? `
        <div class="serdar-answer-box">
          <div class="serdar-answer-label">💬 Serdar'ın Cevabı:</div>
          <div class="serdar-answer-text">${item.a}</div>
        </div>
      `
      : `
        <div class="waiting-answer-box">
          <span>⏳ Serdar'ın cevabı bekleniyor...</span>
        </div>
      `;

    card.innerHTML = `
      <div class="asked-item-header">
        <span>Soru #${item.id.toString().slice(-4)}</span>
        <span>${item.date}</span>
      </div>
      <div class="asked-q-text">"${item.q}"</div>
      ${answerHtml}
    `;

    askedQuestionsList.appendChild(card);
  });
}

function addPoints(amount, source) {
  userState.points += amount;
  saveState();
  renderQuestions();
  checkNewUnlocks();

  const uname = currentUsername || "Edanur";
  sendTelegramLog(
    `🌟 <b>${uname} Puan Kazandı!</b>\n` +
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
  const uname = currentUsername || "Edanur";
  sendTelegramLog(
    `🌸 <b>${uname} Siteye Giriş Yaptı!</b>\n` +
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
    // Puandan düş
    userState.points -= item.cost;
    userState.unlockedQuestions.push(questionId);
    saveState();
    renderQuestions();
    confetti({ particleCount: 45, spread: 60, origin: { y: 0.6 } });

    sendTelegramLog(
      `🔓 <b>Edanur Bir Sorunun Kilidini Açtı!</b>\n` +
      `❓ <b>Soru ${item.id}:</b> <i>"${item.q}"</i>\n` +
      `➖ Harcanan: <b>-${item.cost} ⭐</b>\n` +
      `⭐ <b>Kalan Puan:</b> ${userState.points}`
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
let gameIntervals = []; // Tüm interval'leri topluca temizlemek için dizi

function clearAllGameIntervals() {
  gameIntervals.forEach(id => clearInterval(id));
  gameIntervals = [];
}

function updateGameProgress(score, target) {
  currentGameScore = score;
  const pct = Math.min(100, Math.round((currentGameScore / target) * 100));
  if (modalProgressFill) modalProgressFill.style.width = pct + "%";
  if (modalScore) modalScore.textContent = `${currentGameScore} / ${target}`;

  if (currentGameScore >= target) {
    setTimeout(() => {
      finishGameSuccess(GAMES_CONFIG[currentGameKey]);
    }, 350);
  }
}

function finishGameSuccess(config) {
  clearAllGameIntervals();
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

window.openGame = function(gameKey) {
  clearAllGameIntervals();
  currentGameKey = gameKey;
  const config = GAMES_CONFIG[gameKey];
  if (!config) return;

  modalGameTitle.textContent = config.title;
  modalInstruction.textContent = config.instruction;
  currentGameScore = 0;
  updateGameProgress(0, config.targetScore);
  modalPlayArea.innerHTML = "";

  // Modalı kesin olarak görünür yap
  gameModal.style.display = "flex";
  gameModal.classList.add("active");

  setTimeout(() => {
    switch(gameKey) {
      case "balloons": setupBalloonsGame(config); break;
      case "ninja": setupNinjaGame(config); break;
      case "flappy": setupFlappyGame(config); break;
      case "piano": setupPianoGame(config); break;
      case "memory": setupMemoryGame(config); break;
      case "catch": setupCatchGame(config); break;
      case "mole": setupMoleGame(config); break;
      case "wheel": setupWheelGame(config); break;
      case "color": setupColorGame(config); break;
      case "numbers": setupNumbersGame(config); break;
      case "pin": setupPinGame(config); break;
    }
  }, 60);
};

window.closeGame = function() {
  clearAllGameIntervals();
  gameModal.classList.remove("active");
  gameModal.style.display = "none";
  modalPlayArea.innerHTML = "";
};

window.openSpecialStory = function() {
  specialStoryModal.style.display = "flex";
  specialStoryModal.classList.add("active");
  renderSpecialFinal();
};

const storyCloseBtn = document.getElementById("storyCloseBtn");
if (storyCloseBtn) {
  storyCloseBtn.addEventListener("click", () => {
    specialStoryModal.classList.remove("active");
    specialStoryModal.style.display = "none";
  });
}

/* --- YENİ OYUN 1: MEYVE KESMECE (FRUIT NINJA) --- */
function setupNinjaGame(config) {
  const canvas = document.createElement("canvas");
  canvas.className = "ninja-canvas";
  modalPlayArea.appendChild(canvas);
  const ctx = canvas.getContext("2d");
  canvas.width = modalPlayArea.clientWidth;
  canvas.height = modalPlayArea.clientHeight;

  const fruits = [];
  const fruitEmojis = ["🍓", "🍉", "🍒", "🍑", "🍊", "🍋"];
  let sliced = 0;
  let trail = [];

  function spawnFruit() {
    if (sliced >= config.targetScore) return;
    fruits.push({
      x: 30 + Math.random() * (canvas.width - 60),
      y: canvas.height + 20,
      vx: (Math.random() - 0.5) * 3,
      vy: -(7 + Math.random() * 2),
      emoji: fruitEmojis[Math.floor(Math.random() * fruitEmojis.length)],
      isSliced: false,
      size: 38
    });
  }

  const loop = setInterval(() => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Bıçak izi çiz
    if (trail.length > 1) {
      ctx.beginPath();
      ctx.moveTo(trail[0].x, trail[0].y);
      for (let i = 1; i < trail.length; i++) ctx.lineTo(trail[i].x, trail[i].y);
      ctx.strokeStyle = "#ff477e";
      ctx.lineWidth = 4;
      ctx.lineCap = "round";
      ctx.stroke();
    }

    // Meyveleri güncelle ve çiz
    ctx.font = "32px serif";
    ctx.textAlign = "center";
    for (let i = fruits.length - 1; i >= 0; i--) {
      const f = fruits[i];
      f.x += f.vx;
      f.y += f.vy;
      f.vy += 0.22; // yerçekimi

      if (f.isSliced) {
        ctx.fillText("✨", f.x, f.y);
      } else {
        ctx.fillText(f.emoji, f.x, f.y);
      }

      if (f.y > canvas.height + 40) fruits.splice(i, 1);
    }
  }, 1000 / 60);

  const spawnTimer = setInterval(spawnFruit, 800);
  gameIntervals.push(loop, spawnTimer);

  // Dilimleme / Kaydırma Olayı
  const handleMove = (x, y) => {
    const rect = canvas.getBoundingClientRect();
    const cx = x - rect.left;
    const cy = y - rect.top;
    trail.push({ x: cx, y: cy });
    if (trail.length > 6) trail.shift();

    fruits.forEach(f => {
      if (!f.isSliced) {
        const dist = Math.hypot(f.x - cx, f.y - cy);
        if (dist < 32) {
          f.isSliced = true;
          sliced++;
          updateGameProgress(sliced, config.targetScore);
        }
      }
    });
  };

  canvas.addEventListener("pointermove", (e) => handleMove(e.clientX, e.clientY));
  canvas.addEventListener("touchmove", (e) => {
    if (e.touches[0]) handleMove(e.touches[0].clientX, e.touches[0].clientY);
  });
  canvas.addEventListener("pointerup", () => { trail = []; });
  canvas.addEventListener("touchend", () => { trail = []; });
}

/* --- YENİ OYUN 2: FLAPPY UÇAN KALP (ÇARPINCA SIFIRLANIR) --- */
function setupFlappyGame(config) {
  const canvas = document.createElement("canvas");
  canvas.className = "flappy-canvas";
  modalPlayArea.appendChild(canvas);
  const ctx = canvas.getContext("2d");
  canvas.width = modalPlayArea.clientWidth;
  canvas.height = modalPlayArea.clientHeight;

  let birdY = canvas.height / 2;
  let birdVelocity = 0;
  const gravity = 0.32;
  const jump = -5.8;

  let passedClouds = 0;
  let pipes = [];
  let isGameOver = false;

  function resetGame() {
    birdY = canvas.height / 2;
    birdVelocity = 0;
    passedClouds = 0;
    pipes = [];
    isGameOver = false;
    updateGameProgress(0, config.targetScore);
    addPipe();
  }

  function addPipe() {
    if (isGameOver) return;
    const gap = 115;
    const topH = 40 + Math.random() * (canvas.height - gap - 80);
    pipes.push({ x: canvas.width, top: topH, bottom: topH + gap, passed: false });
  }

  const loop = setInterval(() => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (!isGameOver) {
      birdVelocity += gravity;
      birdY += birdVelocity;

      // Zemin ve tavan çarpma kontrolü
      if (birdY > canvas.height - 20 || birdY < 15) {
        triggerHit();
      }
    }

    // Kuş / Kalp çiz
    ctx.font = "28px serif";
    ctx.textAlign = "center";
    ctx.fillText(isGameOver ? "💥" : "💖", 60, birdY);

    // Bulut engelleri çiz ve çarpışma kontrolü
    ctx.fillStyle = "rgba(255, 182, 193, 0.75)";
    for (let i = pipes.length - 1; i >= 0; i--) {
      const p = pipes[i];
      if (!isGameOver) {
        p.x -= 2.2;
      }

      // Üst bulut sütunu
      ctx.fillRect(p.x, 0, 42, p.top);
      ctx.font = "26px serif";
      ctx.fillText("☁️", p.x + 21, p.top);

      // Alt bulut sütunu
      ctx.fillRect(p.x, p.bottom, 42, canvas.height - p.bottom);
      ctx.fillText("☁️", p.x + 21, p.bottom + 25);

      // Çarpışma Kutusu Kontrolü (Hassas ve Gerçekçi Hitbox)
      const birdX = 60;
      const birdRadius = 14;
      let hasHitThisPipe = false;

      if (
        birdX + birdRadius >= p.x &&
        birdX - birdRadius <= p.x + 42
      ) {
        if (birdY - birdRadius <= p.top || birdY + birdRadius >= p.bottom) {
          hasHitThisPipe = true;
          triggerHit();
        }
      }

      // Sadece çarpmadıysa ve oyun devam ediyorsa başarılı geçiş say
      if (!isGameOver && !hasHitThisPipe && !p.passed && p.x + 42 < birdX) {
        p.passed = true;
        passedClouds++;
        updateGameProgress(passedClouds, config.targetScore);
      }

      if (p.x < -50) pipes.splice(i, 1);
    }
  }, 1000 / 60);

  function triggerHit() {
    if (isGameOver) return;
    isGameOver = true;

    // Küçük bir titreşim ve mesaj
    modalInstruction.textContent = "Çarptın! 💥 Puanlar sıfırlandı, baştan başlıyor...";
    modalInstruction.style.color = "#e53e3e";

    setTimeout(() => {
      modalInstruction.textContent = config.instruction;
      modalInstruction.style.color = "";
      resetGame();
    }, 700);
  }

  const spawnTimer = setInterval(addPipe, 1750);
  addPipe();
  gameIntervals.push(loop, spawnTimer);

  const doJump = (e) => {
    if (e) e.preventDefault();
    if (!isGameOver) {
      birdVelocity = jump;
    }
  };

  canvas.addEventListener("pointerdown", doJump);
  canvas.addEventListener("touchstart", doJump, { passive: false });
}

/* --- YENİ OYUN 3: RİTİM PİYANO NOTALARI (TAM RİTİM KURALLARI) --- */
function setupPianoGame(config) {
  const board = document.createElement("div");
  board.className = "piano-board";

  const lanes = [];
  for (let i = 0; i < 3; i++) {
    const lane = document.createElement("div");
    lane.className = "piano-lane";
    board.appendChild(lane);
    lanes.push(lane);
  }

  const hitLine = document.createElement("div");
  hitLine.className = "piano-hit-line";
  board.appendChild(hitLine);
  modalPlayArea.appendChild(board);

  let hitCount = 0;
  let isGameOver = false;
  let activeNotes = [];

  function resetGame() {
    isGameOver = false;
    hitCount = 0;
    updateGameProgress(0, config.targetScore);
    activeNotes.forEach(n => {
      clearInterval(n.timer);
      if (n.element.parentNode) n.element.remove();
    });
    activeNotes = [];
  }

  function triggerFail(reasonText) {
    if (isGameOver) return;
    isGameOver = true;

    modalInstruction.textContent = reasonText;
    modalInstruction.style.color = "#e53e3e";

    setTimeout(() => {
      modalInstruction.textContent = config.instruction;
      modalInstruction.style.color = "";
      resetGame();
    }, 800);
  }

  function spawnItem() {
    if (isGameOver || hitCount >= config.targetScore) return;

    const laneIdx = Math.floor(Math.random() * 3);
    const targetLane = lanes[laneIdx];

    // %60 ihtimalle gerçek ritim notası (🎵), %40 ihtimalle tuzak (⭐, 💖, 🌸)
    const isTargetNote = Math.random() < 0.65;
    const traps = ["⭐", "💖", "🌸", "✨"];
    const icon = isTargetNote ? "🎵" : traps[Math.floor(Math.random() * traps.length)];

    const note = document.createElement("div");
    note.className = "piano-note";
    note.textContent = icon;
    if (!isTargetNote) {
      note.style.background = "linear-gradient(135deg, #a0aec0, #cbd5e0)";
      note.style.boxShadow = "0 3px 8px rgba(0,0,0,0.15)";
    }
    targetLane.appendChild(note);

    let topPos = -50;
    const noteObj = { element: note, timer: null };

    const fallTimer = setInterval(() => {
      if (isGameOver) return;
      topPos += 3.6;
      note.style.top = topPos + "px";

      // Yere düşme kontrolü (Çizgiyi geçip alt sınıra vurursa)
      if (topPos > modalPlayArea.clientHeight - 10) {
        clearInterval(fallTimer);
        note.remove();

        // Eğer yere düşen gerçek bir 🎵 notasıysa YANDIN!
        if (isTargetNote && !isGameOver) {
          triggerFail("Notayı kaçırdın! 💥 Puanlar sıfırlandı!");
        }
      }
    }, 20);

    noteObj.timer = fallTimer;
    activeNotes.push(noteObj);

    const hit = (e) => {
      if (e) { e.preventDefault(); e.stopPropagation(); }
      if (isGameOver) return;

      clearInterval(fallTimer);
      note.remove();

      if (isTargetNote) {
        // Doğru notaya bastı! +1 Puan
        hitCount++;
        updateGameProgress(hitCount, config.targetScore);
      } else {
        // Tuzağa bastı! Yanar!
        triggerFail("Yanlış objeye bastın! 💥 Sadece 🎵 notalarına dokun!");
      }
    };

    note.addEventListener("pointerdown", hit);
    note.addEventListener("touchstart", hit, { passive: false });
  }

  const pTimer = setInterval(spawnItem, 800);
  gameIntervals.push(pTimer);
  spawnItem();
}

/* --- YENİ OYUN 4: ŞANS ÇARKIFELEĞİ --- */
function setupWheelGame(config) {
  const container = document.createElement("div");
  container.className = "wheel-container";

  const pointer = document.createElement("div");
  pointer.className = "wheel-pointer";
  pointer.textContent = "🔻";

  const canvas = document.createElement("canvas");
  canvas.className = "wheel-canvas";
  canvas.width = 250;
  canvas.height = 250;

  const btn = document.createElement("button");
  btn.className = "spin-btn";
  btn.textContent = "Çarkı Çevir! 🎡";

  container.appendChild(pointer);
  container.appendChild(canvas);
  container.appendChild(btn);
  modalPlayArea.appendChild(container);

  const ctx = canvas.getContext("2d");
  const slices = [
    { label: "+15 ⭐", color: "#ff758c" },
    { label: "Harikasın!", color: "#ffd166" },
    { label: "+20 ⭐", color: "#a18cd1" },
    { label: "Çok Tatlısın!", color: "#ff9a9e" },
    { label: "+25 ⭐", color: "#06d6a0" },
    { label: "Gülümse :)", color: "#fbc2eb" }
  ];

  let currentAngle = 0;
  function drawWheel(angle) {
    const arc = (Math.PI * 2) / slices.length;
    ctx.clearRect(0, 0, 250, 250);
    ctx.save();
    ctx.translate(125, 125);
    ctx.rotate(angle);

    slices.forEach((s, i) => {
      ctx.beginPath();
      ctx.fillStyle = s.color;
      ctx.moveTo(0, 0);
      ctx.arc(0, 0, 120, i * arc, (i + 1) * arc);
      ctx.lineTo(0, 0);
      ctx.fill();

      ctx.save();
      ctx.rotate(i * arc + arc / 2);
      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 13px 'Comfortaa', sans-serif";
      ctx.textAlign = "right";
      ctx.fillText(s.label, 110, 5);
      ctx.restore();
    });

    ctx.restore();
  }

  drawWheel(0);

  let spinning = false;
  btn.addEventListener("click", () => {
    if (spinning) return;
    spinning = true;
    btn.disabled = true;
    btn.style.opacity = "0.5";

    let speed = 0.45 + Math.random() * 0.2;
    const spinAnim = setInterval(() => {
      currentAngle += speed;
      speed *= 0.985;
      drawWheel(currentAngle);

      if (speed < 0.005) {
        clearInterval(spinAnim);
        setTimeout(() => {
          updateGameProgress(1, config.targetScore);
        }, 500);
      }
    }, 20);
  });
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
  const bTimer = setInterval(spawnBalloon, 850);
  gameIntervals.push(bTimer);
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

  let catchScore = 0;
  let isGameOver = false;
  let activeItems = [];

  function resetGame() {
    isGameOver = false;
    catchScore = 0;
    updateGameProgress(0, config.targetScore);
    activeItems.forEach(item => {
      clearInterval(item.timer);
      if (item.element.parentNode) item.element.remove();
    });
    activeItems = [];
  }

  function triggerFail(reasonText) {
    if (isGameOver) return;
    isGameOver = true;

    modalInstruction.textContent = reasonText;
    modalInstruction.style.color = "#e53e3e";

    setTimeout(() => {
      modalInstruction.textContent = config.instruction;
      modalInstruction.style.color = "";
      resetGame();
    }, 800);
  }

  function spawnFallingItem() {
    if (isGameOver || catchScore >= config.targetScore) return;

    // %70 ihtimalle parlayan yıldız (⭐), %30 ihtimalle bomba/tuzak (💣, 🪨)
    const isStar = Math.random() < 0.7;
    const trapIcons = ["💣", "🪨", "⚡"];
    const icon = isStar ? "⭐" : trapIcons[Math.floor(Math.random() * trapIcons.length)];

    const itemElem = document.createElement("div");
    itemElem.className = "falling-item";
    itemElem.textContent = icon;

    const startX = Math.random() * (modalPlayArea.clientWidth - 50) + 25;
    itemElem.style.left = startX + "px";
    itemElem.style.top = "0px";
    modalPlayArea.appendChild(itemElem);

    let itemY = 0;
    const speed = 3.2 + Math.random() * 0.8;
    const itemObj = { element: itemElem, timer: null };

    const fallTimer = setInterval(() => {
      if (isGameOver) return;
      itemY += speed;
      itemElem.style.top = itemY + "px";

      const bY = modalPlayArea.clientHeight - 42;
      // Sepetle temas kontrolü
      if (itemY >= bY - 18 && itemY <= bY + 18) {
        if (Math.abs(startX - basketX) < 42) {
          clearInterval(fallTimer);
          itemElem.remove();

          if (isStar) {
            // Yıldız yakaladı! +1 Puan
            catchScore++;
            updateGameProgress(catchScore, config.targetScore);
          } else {
            // Bombaya çarptı! Yanar!
            triggerFail("Bombaya çarptın! 💥 Puanlar sıfırlandı!");
          }
          return;
        }
      }

      if (itemY > modalPlayArea.clientHeight + 10) {
        clearInterval(fallTimer);
        itemElem.remove();
      }
    }, 20);

    itemObj.timer = fallTimer;
    activeItems.push(itemObj);
  }

  const cTimer = setInterval(spawnFallingItem, 900);
  gameIntervals.push(cTimer);
  spawnFallingItem();
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

/* --- YENİ OYUN 5: RENK TUZAĞI (STROOP REFLEKS) --- */
function setupColorGame(config) {
  const container = document.createElement("div");
  container.className = "color-game-container";

  const timerBar = document.createElement("div");
  timerBar.className = "color-timer-bar";
  const timerFill = document.createElement("div");
  timerFill.className = "color-timer-fill";
  timerBar.appendChild(timerFill);

  const wordDisplay = document.createElement("div");
  wordDisplay.className = "color-word-display";

  const buttonsGrid = document.createElement("div");
  buttonsGrid.className = "color-buttons-grid";

  container.appendChild(timerBar);
  container.appendChild(wordDisplay);
  container.appendChild(buttonsGrid);
  modalPlayArea.appendChild(container);

  const colors = [
    { name: "KIRMIZI", color: "#e53e3e" },
    { name: "MAVİ", color: "#3182ce" },
    { name: "YEŞİL", color: "#38a169" },
    { name: "SARI", color: "#d69e2e" },
    { name: "PEMBE", color: "#d53f8c" }
  ];

  colors.forEach(c => {
    const btn = document.createElement("button");
    btn.className = "color-btn";
    btn.style.backgroundColor = c.color;
    btn.textContent = c.name;
    btn.addEventListener("click", () => handleAnswer(c.color));
    buttonsGrid.appendChild(btn);
  });

  let currentStreak = 0;
  let targetColorHex = "";
  let questionTimeout = null;
  let animTimer = null;
  let isGameOver = false;

  function resetGame() {
    clearTimeout(questionTimeout);
    clearInterval(animTimer);
    currentStreak = 0;
    isGameOver = false;
    updateGameProgress(0, config.targetScore);
    nextQuestion();
  }

  function triggerFail(reason) {
    if (isGameOver) return;
    isGameOver = true;
    clearTimeout(questionTimeout);
    clearInterval(animTimer);

    modalInstruction.textContent = reason;
    modalInstruction.style.color = "#e53e3e";

    setTimeout(() => {
      modalInstruction.textContent = config.instruction;
      modalInstruction.style.color = "";
      resetGame();
    }, 800);
  }

  function nextQuestion() {
    if (isGameOver) return;
    if (currentStreak >= config.targetScore) return;

    // Kelimenin anlamı ile rengini farklı yap
    const textObj = colors[Math.floor(Math.random() * colors.length)];
    let colorObj = colors[Math.floor(Math.random() * colors.length)];
    while (colorObj.color === textObj.color && colors.length > 1) {
      colorObj = colors[Math.floor(Math.random() * colors.length)];
    }

    wordDisplay.textContent = textObj.name;
    wordDisplay.style.color = colorObj.color;
    targetColorHex = colorObj.color;

    // Zamanlayıcıyı başlat (1.8 saniye)
    timerFill.style.transition = "none";
    timerFill.style.width = "100%";
    setTimeout(() => {
      timerFill.style.transition = "width 1.8s linear";
      timerFill.style.width = "0%";
    }, 20);

    clearTimeout(questionTimeout);
    questionTimeout = setTimeout(() => {
      triggerFail("Süre doldu! 💥 Puanlar sıfırlandı!");
    }, 1800);
  }

  function handleAnswer(chosenColor) {
    if (isGameOver) return;
    clearTimeout(questionTimeout);

    if (chosenColor === targetColorHex) {
      currentStreak++;
      updateGameProgress(currentStreak, config.targetScore);
      if (currentStreak < config.targetScore) {
        nextQuestion();
      }
    } else {
      triggerFail("Rengi yanlış seçtin! 💥 Yazıya değil, renge odaklan!");
    }
  }

  resetGame();
}

/* --- YENİ OYUN 6: HIZLI SAYI SIRALAMA (1'DEN 16'YA) --- */
function setupNumbersGame(config) {
  const container = document.createElement("div");
  container.className = "numbers-game-container";

  const timerText = document.createElement("div");
  timerText.className = "numbers-timer-text";
  timerText.textContent = "Kalan Süre: 12.0s";

  const grid = document.createElement("div");
  grid.className = "numbers-grid";

  container.appendChild(timerText);
  container.appendChild(grid);
  modalPlayArea.appendChild(container);

  let expectedNumber = 1;
  let timeLeft = 12.0;
  let countdownTimer = null;
  let isGameOver = false;

  function resetGame() {
    clearInterval(countdownTimer);
    expectedNumber = 1;
    timeLeft = 12.0;
    isGameOver = false;
    updateGameProgress(0, config.targetScore);
    grid.innerHTML = "";

    const numbers = Array.from({ length: 16 }, (_, i) => i + 1).sort(() => Math.random() - 0.5);
    numbers.forEach(num => {
      const cell = document.createElement("div");
      cell.className = "number-cell";
      cell.textContent = num;
      cell.dataset.num = num;

      cell.addEventListener("pointerdown", () => {
        if (isGameOver) return;
        if (parseInt(cell.dataset.num) === expectedNumber) {
          cell.classList.add("pressed");
          expectedNumber++;
          updateGameProgress(expectedNumber - 1, config.targetScore);
          if (expectedNumber > 16) {
            clearInterval(countdownTimer);
          }
        } else {
          triggerFail(`Yanlış sayı! 💥 Sıradaki sayı: ${expectedNumber}`);
        }
      });
      grid.appendChild(cell);
    });

    countdownTimer = setInterval(() => {
      timeLeft -= 0.1;
      timerText.textContent = `Kalan Süre: ${Math.max(0, timeLeft).toFixed(1)}s`;
      if (timeLeft <= 0) {
        clearInterval(countdownTimer);
        triggerFail("Zaman bitti! 💥 12 saniyede bitirmelisin!");
      }
    }, 100);
    gameIntervals.push(countdownTimer);
  }

  function triggerFail(reason) {
    if (isGameOver) return;
    isGameOver = true;
    clearInterval(countdownTimer);

    modalInstruction.textContent = reason;
    modalInstruction.style.color = "#e53e3e";

    setTimeout(() => {
      modalInstruction.textContent = config.instruction;
      modalInstruction.style.color = "";
      resetGame();
    }, 800);
  }

  resetGame();
}

/* --- YENİ OYUN 7: DÖNEN HEDEF / İĞNE BATIRMA (KNIFE PIN) --- */
function setupPinGame(config) {
  const canvas = document.createElement("canvas");
  canvas.className = "pin-canvas";
  modalPlayArea.appendChild(canvas);
  const ctx = canvas.getContext("2d");
  canvas.width = modalPlayArea.clientWidth;
  canvas.height = modalPlayArea.clientHeight;

  const targetRadius = 45;
  const targetX = canvas.width / 2;
  const targetY = canvas.height * 0.35;
  const pinLength = 70;

  let currentAngle = 0;
  let rotationSpeed = 0.035;
  let pins = []; // [angle1, angle2...]
  let pinnedCount = 0;
  let isGameOver = false;

  function resetGame() {
    pinnedCount = 0;
    pins = [];
    isGameOver = false;
    currentAngle = 0;
    updateGameProgress(0, config.targetScore);
  }

  function triggerFail() {
    if (isGameOver) return;
    isGameOver = true;

    modalInstruction.textContent = "İğneler birbirine çarptı! 💥 Baştan başlıyor...";
    modalInstruction.style.color = "#e53e3e";

    setTimeout(() => {
      modalInstruction.textContent = config.instruction;
      modalInstruction.style.color = "";
      resetGame();
    }, 800);
  }

  const loop = setInterval(() => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (!isGameOver) {
      currentAngle += rotationSpeed;
    }

    // Ortadaki Dönen Hedef Çember
    ctx.beginPath();
    ctx.arc(targetX, targetY, targetRadius, 0, Math.PI * 2);
    ctx.fillStyle = "#ff477e";
    ctx.fill();
    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 16px 'Comfortaa', sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(`${12 - pinnedCount}`, targetX, targetY);

    // Saplanmış İğneleri Çiz
    pins.forEach(angle => {
      const rad = angle + currentAngle;
      const startX = targetX + Math.cos(rad) * targetRadius;
      const startY = targetY + Math.sin(rad) * targetRadius;
      const endX = targetX + Math.cos(rad) * (targetRadius + pinLength);
      const endY = targetY + Math.sin(rad) * (targetRadius + pinLength);

      ctx.beginPath();
      ctx.moveTo(startX, startY);
      ctx.lineTo(endX, endY);
      ctx.strokeStyle = "#4a5568";
      ctx.lineWidth = 3;
      ctx.stroke();

      ctx.beginPath();
      ctx.arc(endX, endY, 6, 0, Math.PI * 2);
      ctx.fillStyle = "#ff758c";
      ctx.fill();
    });

    // Fırlatılmaya hazır aşağıdaki iğne
    const readyY = canvas.height * 0.82;
    ctx.beginPath();
    ctx.moveTo(targetX, readyY);
    ctx.lineTo(targetX, readyY - pinLength);
    ctx.strokeStyle = "#4a5568";
    ctx.lineWidth = 3;
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(targetX, readyY, 6, 0, Math.PI * 2);
    ctx.fillStyle = "#ff477e";
    ctx.fill();
  }, 1000 / 60);

  gameIntervals.push(loop);

  function shootPin() {
    if (isGameOver || pinnedCount >= config.targetScore) return;

    // Yeni iğne saat 6 yönünde (Math.PI / 2) saplanır
    const pinAngle = Math.PI / 2 - currentAngle;

    // Çarpışma kontrolü (Diğer iğnelerle açı farkı çok yakınsa)
    const minDistanceRad = 0.22; // ~13 derece mesafe
    for (let a of pins) {
      let diff = Math.abs((a - pinAngle) % (Math.PI * 2));
      if (diff > Math.PI) diff = Math.PI * 2 - diff;
      if (diff < minDistanceRad) {
        triggerFail();
        return;
      }
    }

    pins.push(pinAngle);
    pinnedCount++;
    updateGameProgress(pinnedCount, config.targetScore);

    // Her 3 iğnede bir yön ve hız değişsin (Zorluk artsın!)
    if (pinnedCount % 3 === 0) {
      rotationSpeed = (rotationSpeed > 0 ? -1 : 1) * (0.038 + Math.random() * 0.02);
    }
  }

  canvas.addEventListener("pointerdown", shootPin);
  resetGame();
}

/* --- ÖZEL MOD: İLK 5 BÖLÜM VE KAÇAN HAYIR BUTONU FİNALİ --- */
const specialStoryModal = document.getElementById("specialStoryModal");
const storyContent = document.getElementById("storyContent");

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

const adminUserSelect = document.getElementById("adminUserSelect");
const adminAskedList = document.getElementById("adminAskedList");

function renderAdminData() {
  localStorage.setItem("serdar_role", "serdar_admin"); // Serdar'ın kendi tarayıcısı admin olarak işaretlendi
  userRole = "serdar_admin";

  const defaultUsers = ["Edanur", "Serdar"];
  if (currentUsername && !defaultUsers.includes(currentUsername)) {
    defaultUsers.push(currentUsername);
  }

  // Tüm kayıtlı kullanıcıları buluttan çek ve select listesine doldur
  fetch(CLOUD_BASE_URL + USERS_LIST_KEY)
    .then(res => res.json())
    .catch(() => defaultUsers)
    .then(usersList => {
      let list = Array.isArray(usersList) && usersList.length > 0 ? usersList : defaultUsers;
      defaultUsers.forEach(u => {
        if (!list.includes(u)) list.push(u);
      });

      const currentSelected = adminUserSelect.value || (currentUsername === "Serdar" ? "Serdar" : "Edanur");
      adminUserSelect.innerHTML = "";
      list.forEach(u => {
        const opt = document.createElement("option");
        opt.value = u;
        opt.textContent = `${u}`;
        if (u === currentSelected) opt.selected = true;
        adminUserSelect.appendChild(opt);
      });

      fetchAndDisplayUserData(adminUserSelect.value || "Edanur");
    });
}

if (adminUserSelect) {
  adminUserSelect.addEventListener("change", () => {
    fetchAndDisplayUserData(adminUserSelect.value);
  });
}

function fetchAndDisplayUserData(targetUser) {
  adminAnswersList.innerHTML = `<p style="font-size:0.8rem; color:#718096;"><b>${targetUser}</b> verileri yükleniyor... ⏳</p>`;
  if (adminAskedList) adminAskedList.innerHTML = "";

  loadStateFromCloud(targetUser, (cloudData) => {
    const dataToDisplay = cloudData || { points: 0, answers: {}, askedToSerdar: [] };

    adminTotalPoints.textContent = dataToDisplay.points || 0;
    const answeredKeys = Object.keys(dataToDisplay.answers || {});
    adminAnsweredCount.textContent = `${answeredKeys.length} / 10`;

    // 1. Kilitli Soruların Cevapları
    adminAnswersList.innerHTML = "";
    if (answeredKeys.length === 0) {
      adminAnswersList.innerHTML = `<p style="font-size:0.8rem; color:#a0aec0;">${targetUser} henüz bir soru cevaplamadı.</p>`;
    } else {
      answeredKeys.forEach(k => {
        const qObj = QUESTIONS_DATA.find(q => q.id === parseInt(k));
        const item = document.createElement("div");
        item.className = "admin-answer-item";
        item.innerHTML = `
          <strong>Soru ${k}:</strong> ${qObj ? qObj.q : ''}<br>
          <span style="color:#d6336c; font-weight:700;">${targetUser}'un Cevabı:</span> ${dataToDisplay.answers[k]}
        `;
        adminAnswersList.appendChild(item);
      });
    }

    // 2. Serdar'a Sorduğu Sorular
    if (adminAskedList) {
      const askedArr = dataToDisplay.askedToSerdar || [];
      if (askedArr.length === 0) {
        adminAskedList.innerHTML = `<p style="font-size:0.8rem; color:#a0aec0;">Henüz Serdar'a bir soru sormadı.</p>`;
      } else {
        askedArr.forEach(q => {
          const item = document.createElement("div");
          item.className = "admin-answer-item";
          item.style.borderLeftColor = "#9b51e0";
          item.innerHTML = `
            <strong>Soru:</strong> "${q.q}" <small style="color:#a0aec0;">(${q.date})</small><br>
            <span style="color:#9b51e0; font-weight:700;">Cevap:</span> ${q.a ? q.a : '<i style="color:#e53e3e;">Cevap bekliyor</i>'}
          `;
          adminAskedList.appendChild(item);
        });
      }
    }
  });
}

adminResetBtn.addEventListener("click", () => {
  const targetUser = adminUserSelect ? adminUserSelect.value : "Edanur";
  if (confirm(`${targetUser} kullanıcısının buluttaki tüm puan ve cevaplarını sıfırlamak istiyor musun?`)) {
    const emptyState = { username: targetUser, points: 0, unlockedQuestions: [], answers: {}, askedToSerdar: [] };
    const userKey = getUserStorageKey(targetUser);

    fetch(CLOUD_BASE_URL + userKey, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(emptyState)
    }).then(() => {
      // Eğer sıfırlanan kullanıcı şu an açık olan kullanıcıysa yerel ekranı da hemen sıfırla
      if (!currentUsername || targetUser.toLowerCase() === currentUsername.toLowerCase()) {
        localStorage.removeItem("edanur_game_state");
        userState = { ...emptyState };
        updatePointsDisplay();
        renderQuestions();
        renderAskedQuestions();
      }
      fetchAndDisplayUserData(targetUser);
      alert(`${targetUser} kullanıcısının tüm puanları ve cevapları başarıyla sıfırlandı! ✨`);
    });
  }
});

/* --- KULLANICI KARŞILAMA VE GİRİŞ KONTROLÜ --- */
function checkUserGreeting() {
  const welcomeModal = document.getElementById("welcomeModal");
  const usernameInput = document.getElementById("usernameInput");
  const saveUsernameBtn = document.getElementById("saveUsernameBtn");

  if (!localStorage.getItem("eda_active_username")) {
    if (welcomeModal) {
      welcomeModal.classList.add("active");
      saveUsernameBtn.addEventListener("click", () => {
        let name = (usernameInput.value || "").trim();
        if (!name) name = "Edanur";
        localStorage.setItem("eda_active_username", name);
        currentUsername = name;
        welcomeModal.classList.remove("active");

        // Sayfa başlığını da kişiselleştir
        document.title = `${name}'un Dünyası ✨`;
        const brandTitle = document.querySelector(".brand-title");
        if (brandTitle) brandTitle.textContent = name;
        const hubTitle = document.querySelector(".hub-welcome h2");
        if (hubTitle) hubTitle.textContent = `Hoş Geldin ${name}! 💖`;

        checkEntranceLog();
        loadState();
      });
    }
  } else {
    currentUsername = localStorage.getItem("eda_active_username");
    document.title = `${currentUsername}'un Dünyası ✨`;
    const brandTitle = document.querySelector(".brand-title");
    if (brandTitle) brandTitle.textContent = currentUsername;
    const hubTitle = document.querySelector(".hub-welcome h2");
    if (hubTitle) hubTitle.textContent = `Hoş Geldin ${currentUsername}! 💖`;
    checkEntranceLog();
  }
}

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

/* --- 1V1 MEYDAN OKUMA & LİDERLİK MODU --- */
const CHALLENGE_KEY = "eda_challenge_state";
let challengeGameTimer = null;
let challengeSpawnTimer = null;
let challengeSecondsLeft = 30;
let currentRunScore = 0;
let challengeData = {
  edanurScore: 0,
  serdarScore: 0,
  edanurName: "Edanur",
  leaderName: null,
  leaderScore: 0,
  lastUpdated: null
};

const duelModal = document.getElementById("duelModal");
const duelLobbyArea = document.getElementById("duelLobbyArea");
const duelPlayArea = document.getElementById("duelPlayArea");
const duelResultArea = document.getElementById("duelResultArea");
const startChallengeBtn = document.getElementById("startChallengeBtn");
const saveChallengeScoreBtn = document.getElementById("saveChallengeScoreBtn");
const currentLeaderText = document.getElementById("currentLeaderText");
const leaderSubtitle = document.getElementById("leaderSubtitle");
const edanurRecordBadge = document.getElementById("edanurRecordBadge");
const serdarRecordBadge = document.getElementById("serdarRecordBadge");
const duelPlayer1Name = document.getElementById("duelPlayer1Name");
const duelPlayer2Name = document.getElementById("duelPlayer2Name");
const playingUserLabel = document.getElementById("playingUserLabel");
const myLiveChallengeScore = document.getElementById("myLiveChallengeScore");
const targetRecordScore = document.getElementById("targetRecordScore");
const duelTimer = document.getElementById("duelTimer");
const duelTapArena = document.getElementById("duelTapArena");
const duelWinnerTitle = document.getElementById("duelWinnerTitle");
const challengeScoreSummary = document.getElementById("challengeScoreSummary");
const duelWinnerMsg = document.getElementById("duelWinnerMsg");
const duelWinnerIcon = document.getElementById("duelWinnerIcon");

function openDuelModal() {
  const dModal = document.getElementById("duelModal");
  if (dModal) {
    dModal.classList.add("active");
    resetDuelLobby();
    loadChallengeState();
  }
}
window.openDuelModal = openDuelModal;

function closeDuelModal() {
  const dModal = document.getElementById("duelModal");
  if (dModal) {
    dModal.classList.remove("active");
    stopChallengeGame();
  }
}
window.closeDuelModal = closeDuelModal;

const cardDuelMode = document.getElementById("cardDuelMode");
if (cardDuelMode) {
  cardDuelMode.addEventListener("click", openDuelModal);
}

function resetDuelLobby() {
  stopChallengeGame();
  duelLobbyArea.classList.remove("hidden");
  duelPlayArea.classList.add("hidden");
  duelResultArea.classList.add("hidden");
  loadChallengeState();
}

function loadChallengeState() {
  const myName = (currentUsername || "Edanur").trim();
  const isSerdar = myName.toLowerCase().includes("serdar");

  fetch(CLOUD_BASE_URL + CHALLENGE_KEY)
    .then(res => res.json())
    .catch(() => null)
    .then(data => {
      if (data && typeof data === "object") {
        challengeData = data;
      }

      const p1 = challengeData.edanurName || (isSerdar ? "Edanur" : myName);
      if (duelPlayer1Name) duelPlayer1Name.textContent = p1;
      if (duelPlayer2Name) duelPlayer2Name.textContent = "Serdar";

      if (edanurRecordBadge) edanurRecordBadge.textContent = `${challengeData.edanurScore || 0} Puan`;
      if (serdarRecordBadge) serdarRecordBadge.textContent = `${challengeData.serdarScore || 0} Puan`;

      if (challengeData.leaderName) {
        currentLeaderText.innerHTML = `👑 <b>${challengeData.leaderName}</b> (${challengeData.leaderScore} Puan)`;
        leaderSubtitle.textContent = `Bu skoru geçebilir misin? Kaybeden kahveyi ısmarlar! ☕`;
      } else {
        currentLeaderText.textContent = "Henüz Skor Yapılmadı!";
        leaderSubtitle.textContent = "İlk skoru sen yap ve meydan oku! 🚀";
      }
    });
}

if (startChallengeBtn) {
  startChallengeBtn.addEventListener("click", () => {
    startChallengeMatch();
  });
}

function startChallengeMatch() {
  currentRunScore = 0;
  challengeSecondsLeft = 30;

  const myName = (currentUsername || "Edanur").trim();
  const isSerdar = myName.toLowerCase().includes("serdar");
  const rivalScore = isSerdar ? (challengeData.edanurScore || 0) : (challengeData.serdarScore || 0);

  duelLobbyArea.classList.add("hidden");
  duelPlayArea.classList.remove("hidden");
  duelResultArea.classList.add("hidden");

  if (playingUserLabel) playingUserLabel.textContent = `${myName} (Sen)`;
  if (myLiveChallengeScore) myLiveChallengeScore.textContent = "0";
  if (targetRecordScore) targetRecordScore.textContent = rivalScore;
  if (duelTimer) duelTimer.textContent = "30";
  if (duelTapArena) duelTapArena.innerHTML = "";

  confetti({ particleCount: 30, spread: 50 });

  challengeGameTimer = setInterval(() => {
    challengeSecondsLeft--;
    if (duelTimer) duelTimer.textContent = challengeSecondsLeft;

    if (challengeSecondsLeft <= 0) {
      endChallengeMatch();
    }
  }, 1000);

  spawnChallengeTarget();
  challengeSpawnTimer = setInterval(spawnChallengeTarget, 600);
}

function spawnChallengeTarget() {
  if (!duelTapArena) return;

  const target = document.createElement("div");
  target.className = "duel-target";

  const icons = ["💖", "☕", "🍓", "⭐", "✨", "🔥", "🎀"];
  target.textContent = icons[Math.floor(Math.random() * icons.length)];

  const arenaWidth = duelTapArena.clientWidth - 70;
  const arenaHeight = duelTapArena.clientHeight - 70;

  target.style.left = Math.max(10, Math.floor(Math.random() * arenaWidth)) + "px";
  target.style.top = Math.max(10, Math.floor(Math.random() * arenaHeight)) + "px";

  target.addEventListener("pointerdown", (e) => {
    e.stopPropagation();
    currentRunScore += 1;
    if (myLiveChallengeScore) myLiveChallengeScore.textContent = currentRunScore;
    target.remove();
  });

  duelTapArena.appendChild(target);

  setTimeout(() => {
    if (target.parentNode) target.remove();
  }, 1300);
}

function endChallengeMatch() {
  stopChallengeGame();

  duelPlayArea.classList.add("hidden");
  duelResultArea.classList.remove("hidden");

  const myName = (currentUsername || "Edanur").trim();
  const isSerdar = myName.toLowerCase().includes("serdar");
  const rivalName = isSerdar ? (challengeData.edanurName || "Edanur") : "Serdar";
  const rivalScore = isSerdar ? (challengeData.edanurScore || 0) : (challengeData.serdarScore || 0);

  challengeScoreSummary.textContent = `${currentRunScore} Puan Topladın! ⭐`;

  if (currentRunScore > rivalScore) {
    duelWinnerTitle.textContent = "🎉 YENİ LİDER SENSİN!";
    duelWinnerIcon.textContent = "👑";
    duelWinnerMsg.textContent = `${rivalName}'ın ${rivalScore} puanlık skorunu geçtin!\nKahveler ${rivalName}'dan! ☕🔥`;
    confetti({ particleCount: 70, spread: 80 });
  } else if (currentRunScore === rivalScore) {
    duelWinnerTitle.textContent = "🤝 SKORLAR EŞİTLENDİ!";
    duelWinnerIcon.textContent = "✨";
    duelWinnerMsg.textContent = `İkiniz de ${currentRunScore} puandasınız! Kahveler ortak! ☕`;
  } else {
    duelWinnerTitle.textContent = "💪 GÜZEL DENEME!";
    duelWinnerIcon.textContent = "☕";
    duelWinnerMsg.textContent = `${rivalName} şu an ${rivalScore} puanla önde!\nSkorunu kaydet veya tekrar deneyip rekoru kır!`;
  }
}

if (saveChallengeScoreBtn) {
  saveChallengeScoreBtn.addEventListener("click", () => {
    const myName = (currentUsername || "Edanur").trim();
    const isSerdar = myName.toLowerCase().includes("serdar");
    const rivalName = isSerdar ? (challengeData.edanurName || "Edanur") : "Serdar";

    saveChallengeScoreBtn.disabled = true;
    saveChallengeScoreBtn.textContent = "Kaydedildi & Gönderildi! ✨";

    // 1. Durumu güncelle
    if (isSerdar) {
      challengeData.serdarScore = Math.max(challengeData.serdarScore || 0, currentRunScore);
    } else {
      challengeData.edanurScore = Math.max(challengeData.edanurScore || 0, currentRunScore);
      challengeData.edanurName = myName;
    }

    if (challengeData.serdarScore >= challengeData.edanurScore) {
      challengeData.leaderName = "Serdar";
      challengeData.leaderScore = challengeData.serdarScore;
    } else {
      challengeData.leaderName = challengeData.edanurName;
      challengeData.leaderScore = challengeData.edanurScore;
    }
    challengeData.lastUpdated = new Date().toLocaleString("tr-TR");

    // 2. Buluta kaydet
    fetch(CLOUD_BASE_URL + CHALLENGE_KEY, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(challengeData)
    });

    // 3. Telegram'a meydan okuma bildirimi at!
    sendTelegramLog(
      `⚔️ <b>1v1 KAHVE DÜELLOSU MEYDAN OKUMASI!</b> 🔥\n\n` +
      `👤 <b>${myName}</b> 30 saniyede <b>${currentRunScore} Puan</b> topladı!\n` +
      `👑 <b>Güncel Lider:</b> ${challengeData.leaderName} (${challengeData.leaderScore} Puan)\n\n` +
      `📢 <i>${rivalName}, bu skoru geçebilecek misin? Kahveler kaybedenden! ☕</i>`
    );

    setTimeout(() => {
      resetDuelLobby();
      saveChallengeScoreBtn.disabled = false;
      saveChallengeScoreBtn.textContent = "Skorumu Kaydet & Meydan Oku! 📢";
    }, 1500);
  });
}

function stopChallengeGame() {
  if (challengeGameTimer) { clearInterval(challengeGameTimer); challengeGameTimer = null; }
  if (challengeSpawnTimer) { clearInterval(challengeSpawnTimer); challengeSpawnTimer = null; }
  if (duelTapArena) duelTapArena.innerHTML = "";
}

/* --- KÜSTÜK MÜ? ÖZEL POPUP MANTIĞI --- */
function checkKustukPopup() {
  // Eğer daha önce cevap verdiyse bir daha ASLA çıkmasın
  const alreadyAnswered = localStorage.getItem("eda_kustuk_answered");
  if (alreadyAnswered) return;

  const kustukModal = document.getElementById("kustukModal");
  const kustukFormArea = document.getElementById("kustukFormArea");
  const kustukConfirmArea = document.getElementById("kustukConfirmArea");
  const kustukSuccessArea = document.getElementById("kustukSuccessArea");
  const kustukAnswerInput = document.getElementById("kustukAnswerInput");
  const kustukSubmitBtn = document.getElementById("kustukSubmitBtn");
  const kustukFinalYesBtn = document.getElementById("kustukFinalYesBtn");
  const kustukFinalNoBtn = document.getElementById("kustukFinalNoBtn");

  if (!kustukModal) return;

  // Popup'ı aç (kapatma butonu yok ve dışarı basınca kapanmaz)
  kustukModal.classList.add("active");

  // 1. Gönder Butonuna Basıldığında (Doğrulama ve "Emin misin?" Ekranı)
  kustukSubmitBtn.addEventListener("click", () => {
    const text = (kustukAnswerInput.value || "").trim();
    if (!text) {
      alert("Lütfen bir şeyler yazmadan geçme... 🥺");
      kustukAnswerInput.focus();
      return;
    }
    // "Emin misin?" alanını göster
    kustukFormArea.classList.add("hidden");
    kustukConfirmArea.classList.remove("hidden");
  });

  // 2. "Düzenle" derse geri dön
  kustukFinalNoBtn.addEventListener("click", () => {
    kustukConfirmArea.classList.add("hidden");
    kustukFormArea.classList.remove("hidden");
    kustukAnswerInput.focus();
  });

  // 3. "Evet, Gönder" derse Telegram'a at ve kapat
  kustukFinalYesBtn.addEventListener("click", () => {
    const text = (kustukAnswerInput.value || "").trim();
    const myName = (currentUsername || "Edanur").trim();
    const now = new Date().toLocaleString("tr-TR");

    // Telegram Bildirimi Gönder
    sendTelegramLog(
      `🥺💔 <b>"KÜSTÜK MÜ?" SORUSUNA CEVAP GELDİ!</b>\n\n` +
      `👤 <b>Gönderen:</b> ${myName}\n` +
      `✍️ <b>Cevap:</b> <i>"${text}"</i>\n` +
      `⏰ <b>Zaman:</b> ${now}`
    );

    // Bir daha çıkmaması için kaydet
    localStorage.setItem("eda_kustuk_answered", "true");

    // Başarı ekranı: Sadece "Gönderildi ✨"
    kustukConfirmArea.classList.add("hidden");
    kustukSuccessArea.classList.remove("hidden");

    confetti({ particleCount: 40, spread: 60 });

    setTimeout(() => {
      kustukModal.classList.remove("active");
    }, 1600);
  });
}

/* --- BAŞLATMA --- */
window.addEventListener("DOMContentLoaded", () => {
  loadState();
  renderQuestions();
  createFloatingHearts();
  checkUserGreeting();
  checkKustukPopup();
});
