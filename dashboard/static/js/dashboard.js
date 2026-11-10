/**
 * LUMEN Executive Dashboard Real-Time Client Controller.
 * Establishes SSE connection, handles asynchronous REST dispatches,
 * and renders high-density data visualizations with strict zero-emoji enforcement.
 */

// Establish Server-Sent Events (SSE) stream for live telemetry
function initializeTelemetryStream() {
  const eventSource = new EventSource('/api/stream');

  eventSource.onmessage = function (event) {
    try {
      const data = JSON.parse(event.data);
      updateTelemetryDisplays(data.telemetry);
      updateProfileDisplay(data.profile);
      updateSpotifyDisplay(data.spotify);

      if (data.recentLogs && data.recentLogs.length > 0) {
        renderTerminalLogs(data.recentLogs);
      }
    } catch (parseErr) {
      console.error('[LUMEN ERROR] SSE parse exception:', parseErr);
    }
  };

  eventSource.onerror = function () {
    const statusText = document.getElementById('telemetryStatusText');
    if (statusText) {
      statusText.innerText = 'RECONNECTING STREAM...';
    }
  };
}

function updateTelemetryDisplays(telemetry) {
  if (!telemetry) return;

  const cpuStat = document.getElementById('cpuStat');
  const ramStat = document.getElementById('ramStat');
  const ramDetail = document.getElementById('ramDetail');
  const diskStat = document.getElementById('diskStat');
  const diskDetail = document.getElementById('diskDetail');
  const netStat = document.getElementById('netStat');
  const netSent = document.getElementById('netSent');
  const uptimeStat = document.getElementById('uptimeStat');
  const pidCount = document.getElementById('pidCount');
  const statusText = document.getElementById('telemetryStatusText');

  if (cpuStat) cpuStat.innerText = telemetry.cpuPercent + '%';
  if (ramStat) ramStat.innerText = telemetry.memoryPercent + '%';
  if (ramDetail) ramDetail.innerText = telemetry.memoryUsedGb + ' / ' + telemetry.memoryTotalGb + ' GB';
  if (diskStat) diskStat.innerText = telemetry.diskPercent + '%';
  if (diskDetail) diskDetail.innerText = telemetry.diskUsedGb + ' / ' + telemetry.diskTotalGb + ' GB';
  if (netStat) netStat.innerText = telemetry.netBytesRecvMb + ' MB';
  if (netSent) netSent.innerText = telemetry.netBytesSentMb;
  if (uptimeStat) uptimeStat.innerText = telemetry.uptimeHours + 'h';
  if (pidCount) pidCount.innerText = telemetry.activeProcessesCount;
  if (statusText) statusText.innerText = telemetry.status === '[ALERT]' ? 'SYSTEM ALERT' : 'SYSTEM ACTIVE';
}

function updateProfileDisplay(activeProfile) {
  const profileText = document.getElementById('activeProfileText');
  if (profileText && activeProfile) {
    profileText.innerText = activeProfile;
  }
}

function updateSpotifyDisplay(spotifyState) {
  if (!spotifyState || !spotifyState.playback) return;

  const currentTitle = document.getElementById('currentTrackTitle');
  const currentArtist = document.getElementById('currentTrackArtist');
  const playToggleBtn = document.getElementById('playToggleBtn');
  const spotifyStatusMeta = document.getElementById('spotifyStatusMeta');

  const playback = spotifyState.playback;
  if (currentTitle) currentTitle.innerText = playback.trackTitle;
  if (currentArtist) currentArtist.innerText = playback.artist + ' - ' + playback.album;
  if (playToggleBtn) playToggleBtn.innerText = playback.isPlaying ? 'Pause' : 'Play';
  if (spotifyStatusMeta) spotifyStatusMeta.innerText = playback.isPlaying ? 'PLAYING' : 'PAUSED';
}

function renderTerminalLogs(logsList) {
  const terminal = document.getElementById('systemLogsTerminal');
  if (!terminal) return;

  terminal.innerHTML = logsList.map(entry => {
    let levelClass = 'level-info';
    if (entry.level.includes('OK')) levelClass = 'level-ok';
    if (entry.level.includes('ALERT') || entry.level.includes('ERROR')) levelClass = 'level-alert';
    return `<div class="terminal-line"><span class="${levelClass}">[${entry.timestamp}] ${entry.level}</span> ${entry.message}</div>`;
  }).join('');
}

// Workspace Navigation Tabs
function selectTab(tabId, targetBtn) {
  const panels = document.querySelectorAll('.tab-panel');
  panels.forEach(panel => panel.classList.remove('active'));

  const buttons = document.querySelectorAll('.tab-btn');
  buttons.forEach(btn => btn.classList.remove('active'));

  const selectedPanel = document.getElementById(tabId);
  if (selectedPanel) selectedPanel.classList.add('active');
  if (targetBtn) targetBtn.classList.add('active');
}

// Environment Profile Switcher
async function switchProfile(profileName) {
  try {
    const response = await fetch('/api/profile', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ profile: profileName })
    });
    const result = await response.json();
    if (result.status === '[OK]') {
      const buttons = document.querySelectorAll('.profile-btn');
      buttons.forEach(btn => {
        btn.classList.toggle('active', btn.innerText.trim().toLowerCase() === profileName.toLowerCase());
      });
      document.getElementById('activeProfileText').innerText = result.activeProfile;
    }
  } catch (err) {
    console.error('[LUMEN ERROR] Failed to switch profile:', err);
  }
}

// Personal Finance Calculations
async function runCompoundProjection() {
  const output = document.getElementById('financeOutput');
  output.innerText = '[PROCESSING] Calculating compound growth trajectory...';

  const payload = {
    initialCapital: parseFloat(document.getElementById('initialCapital').value) || 10000,
    monthlyContribution: parseFloat(document.getElementById('monthlyContribution').value) || 600,
    annualReturnRate: parseFloat(document.getElementById('annualReturnRate').value) || 7.0,
    years: parseInt(document.getElementById('timeHorizonYears').value, 10) || 15
  };

  try {
    const response = await fetch('/api/finance/compound', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await response.json();

    let formatted = `[COMPOUND WEALTH ACCUMULATION]\n`;
    formatted += `Horizon: ${result.timeHorizonYears} Years | Benchmark Return: ${result.annualReturnRate}%\n`;
    formatted += `Initial Principal: ${result.initialCapital.toFixed(2)} EUR\n`;
    formatted += `Total Principal Contributed: ${result.totalPrincipalDeposited.toFixed(2)} EUR\n`;
    formatted += `Compound Growth Earned: ${result.totalEarnings.toFixed(2)} EUR\n`;
    formatted += `Final Projected Portfolio: ${result.finalPortfolioValue.toFixed(2)} EUR (${result.growthMultiple}x Multiple)\n\n`;
    formatted += `YEARLY MILESTONES (Sample Intervals):\n`;
    formatted += `Year | Cumulative Balance | Contributions | Interest Share\n`;
    formatted += `---------------------------------------------------------\n`;

    const milestones = result.yearlyProgression.filter(m => m.year === 1 || m.year % 5 === 0 || m.year === result.timeHorizonYears);
    milestones.forEach(m => {
      formatted += `${String(m.year).padEnd(4)} | ${m.totalBalance.toFixed(2).padStart(18)} EUR | ${m.contributions.toFixed(2).padStart(13)} EUR | ${m.interestSharePercent}%\n`;
    });

    output.innerText = formatted;
  } catch (err) {
    output.innerText = `[ERROR] Failed to compute compound projection: ${err.message}`;
  }
}

async function runAssetAllocation() {
  const output = document.getElementById('financeOutput');
  output.innerText = '[PROCESSING] Generating asset allocation guidelines...';

  try {
    const horizon = parseInt(document.getElementById('timeHorizonYears').value, 10) || 10;
    const response = await fetch('/api/finance/allocation', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ riskProfile: 'moderate', timeHorizon: horizon })
    });
    const result = await response.json();

    let text = `[PORTFOLIO ALLOCATION MODEL]\n`;
    text += `Target Profile: ${result.profile} | Horizon: ${result.timeHorizonYears} Years\n`;
    text += `Volatility Expectation: ${result.volatilityExpectation}\n\n`;
    text += `ASSET WEIGHTS:\n`;
    text += `- Global Equities ETF: ${result.allocationWeights.global_equities_etf}%\n`;
    text += `- Fixed Income / Bonds: ${result.allocationWeights.bonds_fixed_income}%\n`;
    text += `- Cash Reserves: ${result.allocationWeights.cash_equivalents}%\n\n`;
    text += `REBALANCING PROTOCOL:\n${result.rebalancingPolicy}\n\n`;
    text += `TOTAL EXPENSE RATIO (TER) MANDATE:\n${result.feeImpactNotice}`;

    output.innerText = text;
  } catch (err) {
    output.innerText = `[ERROR] Asset allocation calculation failed: ${err.message}`;
  }
}

async function evaluateExpenseDecision() {
  const output = document.getElementById('financeOutput');
  output.innerText = '[PROCESSING] Evaluating capital opportunity cost...';

  try {
    const initialCap = parseFloat(document.getElementById('initialCapital').value) || 2500;
    const response = await fetch('/api/finance/evaluate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        concept: 'Discretionary Capital Deployment',
        cost: initialCap,
        benchmarkRate: 7.0
      })
    });
    const result = await response.json();

    let text = `[OPPORTUNITY COST EVALUATION]\n`;
    text += `${result.assessmentSummary}\n\n`;
    text += `COMPOUNDED VALUE LOST IF INVESTED:\n`;
    for (const [horizon, val] of Object.entries(result.opportunityCostByHorizon)) {
      text += `- ${horizon.replace('_', ' ')}: ${val.toFixed(2)} EUR\n`;
    }
    text += `\nDECISION CRITERIA: ${result.decisionThreshold}`;

    output.innerText = text;
  } catch (err) {
    output.innerText = `[ERROR] Evaluation failed: ${err.message}`;
  }
}

// Code & Writing Actions
async function runCodeAudit() {
  const output = document.getElementById('codeOutput');
  const code = document.getElementById('codeSnippet').value;
  output.innerText = '[PROCESSING] Running AST static inspection...';

  try {
    const response = await fetch('/api/code/audit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code: code })
    });
    const result = await response.json();

    let text = `[STATIC AUDIT REPORT] Status: ${result.status}\n`;
    text += `Functions Detected: ${result.functionCount} | Classes: ${result.classCount} | Issues: ${result.issuesCount}\n`;
    text += `Verdict: ${result.pragmaticVerdict}\n\n`;

    if (result.issues && result.issues.length > 0) {
      text += `DETECTED BOTTLENECK / CONCERNS:\n`;
      result.issues.forEach((iss, idx) => {
        text += `${idx + 1}. [${iss.severity}] ${iss.type}: ${iss.observation}\n   Remedy: ${iss.remedy}\n\n`;
      });
    }

    output.innerText = text;
  } catch (err) {
    output.innerText = `[ERROR] Code audit failure: ${err.message}`;
  }
}

async function runProseAudit() {
  const output = document.getElementById('codeOutput');
  const code = document.getElementById('codeSnippet').value;
  output.innerText = '[PROCESSING] Inspecting prose clarity and filler phrases...';

  try {
    const response = await fetch('/api/editor/audit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: code })
    });
    const result = await response.json();

    let text = `[PROSE CLARITY AUDIT]\n`;
    text += `Clarity Score: ${result.clarityScorePercent}% | Average Sentence Length: ${result.averageSentenceLengthWords} words\n`;
    text += `Words: ${result.wordCount} | Sentences: ${result.sentenceCount} | Passive Voice Count: ${result.passiveConstructionsDetected}\n`;
    text += `Verdict: ${result.verdict}\n\n`;

    if (result.detectedFillers && result.detectedFillers.length > 0) {
      text += `IDENTIFIED FILLERS & ALTERNATIVES:\n`;
      result.detectedFillers.forEach(f => {
        text += `- "${f.phrase}" -> Replace with "${f.suggestedAlternative}"\n`;
      });
    }

    output.innerText = text;
  } catch (err) {
    output.innerText = `[ERROR] Prose audit failure: ${err.message}`;
  }
}

async function runProseRefine() {
  const output = document.getElementById('codeOutput');
  const code = document.getElementById('codeSnippet').value;

  try {
    const response = await fetch('/api/editor/refine', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: code })
    });
    const result = await response.json();

    output.innerText = `[STREAMLINED EXECUTIVE DRAFT] (${result.characterReductionPercent}% character reduction):\n\n${result.streamlinedDraft}`;
  } catch (err) {
    output.innerText = `[ERROR] Prose refinement failed: ${err.message}`;
  }
}

// Athletics & Odds Actions
async function generateWorkoutPlan() {
  const output = document.getElementById('fitnessOutput');
  const days = parseInt(document.getElementById('trainingDays').value, 10);
  output.innerText = '[PROCESSING] Structuring periodized workout plan...';

  try {
    const response = await fetch('/api/fitness/split', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ days: days, focus: 'hypertrophy' })
    });
    const result = await response.json();

    let text = `[PROGRAMMING SPLIT: ${result.routineName}]\n`;
    text += `Frequency: ${result.frequencyWeekly} | Focus: ${result.primaryFocus}\n`;
    text += `Overload Protocol: ${result.progressiveOverloadProtocol}\n\n`;
    text += `WEEKLY SESSIONS:\n`;
    result.weeklyPlan.forEach(s => {
      text += `- ${s.session}: ${s.focus}\n`;
    });

    output.innerText = text;
  } catch (err) {
    output.innerText = `[ERROR] Workout generation failed: ${err.message}`;
  }
}

async function calculateOddsProbability() {
  const output = document.getElementById('fitnessOutput');
  const rawInput = document.getElementById('oddsInput').value;
  const odds = rawInput.split(',').map(s => parseFloat(s.trim())).filter(n => !isNaN(n));

  try {
    const response = await fetch('/api/fitness/odds', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ odds: odds })
    });
    const result = await response.json();

    let text = `[IMPLIED PROBABILITY & OVERROUND ANALYSIS]\n`;
    text += `Bookmaker Margin: ${result.bookmakerOverroundPercent}%\n`;
    text += `${result.marketEfficiencyAnalysis}\n\n`;
    text += `OUTCOME BREAKDOWN:\n`;
    result.outcomes.forEach(o => {
      text += `Outcome ${o.outcomeIndex}: Odds ${o.offeredDecimalOdds} | Raw Implied: ${o.rawImpliedProbabilityPercent}% | Fair Odds: ${o.fairDecimalOdds}\n`;
    });
    text += `\nNOTICE: ${result.disclaimer}`;

    output.innerText = text;
  } catch (err) {
    output.innerText = `[ERROR] Odds calculation failed: ${err.message}`;
  }
}

// Procurement Actions
async function searchAmazonCatalog() {
  const output = document.getElementById('procureOutput');
  const query = document.getElementById('searchQuery').value;
  const domain = document.getElementById('marketDomain').value;
  output.innerText = `[PROCESSING] Querying ${domain} for '${query}'...`;

  try {
    const response = await fetch('/api/amazon/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: query, marketplace: domain })
    });
    const result = await response.json();

    let text = `[AMAZON PROCUREMENT RESULTS] Domain: ${result.marketplace} | Total: ${result.resultsFound}\n\n`;
    result.products.forEach((p, idx) => {
      text += `${idx + 1}. ASIN: ${p.asin} | ${p.title}\n`;
      text += `   Product URL: ${p.productUrl}\n`;
      text += `   Direct Cart Addition URL: ${p.cartAddUrl}\n\n`;
    });

    output.innerText = text;
  } catch (err) {
    output.innerText = `[ERROR] Amazon catalog query failed: ${err.message}`;
  }
}

async function generateProductReview() {
  const output = document.getElementById('procureOutput');
  const query = document.getElementById('searchQuery').value;

  try {
    const response = await fetch('/api/review/product', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: query, category: 'Hardware Equipment', price: 299.0 })
    });
    const result = await response.json();

    let text = `[OBJECTIVE PRODUCT REVIEW: ${result.productName}]\n`;
    text += `Category: ${result.category} | Price Tier: ${result.priceTier} (${result.retailPriceEur.toFixed(2)} EUR)\n\n`;
    text += `DOCUMENTED STRENGTHS:\n`;
    result.verifiedStrengths.forEach(s => text += `- ${s}\n`);
    text += `\nDOCUMENTED LIMITATIONS:\n`;
    result.documentedLimitations.forEach(d => text += `- ${d}\n`);
    text += `\nDURABILITY ASSESSMENT:\n${result.durabilityAssessment}\n\n`;
    text += `VERDICT:\n${result.verdictSummary}`;

    output.innerText = text;
  } catch (err) {
    output.innerText = `[ERROR] Review synthesis failed: ${err.message}`;
  }
}

// Applied Philosophy Actions
async function applyPhilosophyLens() {
  const output = document.getElementById('philosophyOutput');
  const problem = document.getElementById('problemDescription').value;
  const school = document.getElementById('philosophySchool').value;
  output.innerText = '[PROCESSING] Applying conceptual framework...';

  try {
    const response = await fetch('/api/philosophy/lens', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ problem: problem, school: school })
    });
    const result = await response.json();

    let text = `[PHILOSOPHICAL DIRECTIVE: ${result.school}]\n`;
    text += `Historical Thinkers: ${result.historicalThinkers.join(', ')}\n`;
    text += `Core Axiom: "${result.coreAxiom}"\n\n`;
    text += `OPERATIONAL DIRECTIVES:\n`;
    result.appliedDirectives.forEach((d, idx) => {
      text += `${idx + 1}. ${d}\n`;
    });

    output.innerText = text;
  } catch (err) {
    output.innerText = `[ERROR] Framework application failed: ${err.message}`;
  }
}

// Task Management
async function addNewTask() {
  const titleInput = document.getElementById('newTaskTitle');
  const prioritySelect = document.getElementById('newTaskPriority');
  const title = titleInput.value.trim();
  const priority = prioritySelect.value;

  if (!title) return;

  try {
    const response = await fetch('/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: title, priority: priority, category: 'Executive' })
    });
    const result = await response.json();

    if (result.status === '[OK]') {
      const tableBody = document.getElementById('tasksTableBody');
      const row = document.createElement('tr');
      row.id = `task-row-${result.task.taskId}`;
      row.innerHTML = `
        <td><span class="badge badge-${result.task.priority.toLowerCase()}">${result.task.priority}</span></td>
        <td>${result.task.title}</td>
        <td style="font-family: var(--font-mono);">${result.task.dueDate}</td>
        <td>${result.task.category}</td>
        <td style="text-align: right;">
          <button class="btn btn-sm" onclick="completeTask(${result.task.taskId})">Done</button>
        </td>
      `;
      tableBody.prepend(row);
      titleInput.value = '';
    }
  } catch (err) {
    console.error('[LUMEN ERROR] Failed to add task:', err);
  }
}

async function completeTask(taskId) {
  try {
    const response = await fetch(`/api/tasks/${taskId}/complete`, { method: 'POST' });
    const result = await response.json();
    if (result.status === '[OK]') {
      const row = document.getElementById(`task-row-${taskId}`);
      if (row) row.remove();
    }
  } catch (err) {
    console.error('[LUMEN ERROR] Failed to complete task:', err);
  }
}

// Spotify Multimedia Actions
async function controlSpotify(action) {
  try {
    const response = await fetch('/api/spotify/control', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: action })
    });
    const result = await response.json();
    if (result.currentTrack) {
      document.getElementById('currentTrackTitle').innerText = result.currentTrack;
    }
  } catch (err) {
    console.error('[LUMEN ERROR] Media dispatch failed:', err);
  }
}

async function setVolume(level) {
  try {
    await fetch('/api/spotify/control', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'volume', volume: parseInt(level, 10) })
    });
  } catch (err) {
    console.error('[LUMEN ERROR] Volume change failed:', err);
  }
}

async function generatePlaylistFromText() {
  const input = document.getElementById('playlistTextInput');
  const rawText = input.value.trim();
  if (!rawText) return;

  try {
    const response = await fetch('/api/spotify/playlist', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: rawText, title: 'LUMEN Executive Session' })
    });
    const result = await response.json();
    alert(`[OK] Playlist '${result.playlistTitle}' created with ${result.trackCount} tracks.`);
    input.value = '';
  } catch (err) {
    alert(`[ERROR] Failed to compile playlist: ${err.message}`);
  }
}

// Steam Local Launch Action
async function launchSteamGame(appId, title) {
  try {
    const response = await fetch('/api/steam/launch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ appId: appId })
    });
    const result = await response.json();
    alert(`[STEAM PROTOCOL] ${result.status} Dispatched launch protocol for ${title} (AppId ${appId}).`);
  } catch (err) {
    alert(`[ERROR] Failed to launch title: ${err.message}`);
  }
}

// Dual Remote Messaging Dispatches
async function dispatchWhatsAppAlert() {
  const input = document.getElementById('priorityMessageInput');
  const message = input.value.trim();
  if (!message) return;

  try {
    const response = await fetch('/api/notify/whatsapp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: message, priority: 'P1' })
    });
    const result = await response.json();
    alert(`[WHATSAPP DISPATCH] ${result.status} ${result.message}`);
    input.value = '';
  } catch (err) {
    alert(`[ERROR] WhatsApp alert failed: ${err.message}`);
  }
}

async function dispatchTelegramCommand() {
  const input = document.getElementById('priorityMessageInput');
  const cmd = input.value.trim() || '/status';

  try {
    const response = await fetch('/api/telegram/command', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ command: cmd })
    });
    const result = await response.json();
    alert(`[TELEGRAM OUTPUT]\n${result.response}`);
    input.value = '';
  } catch (err) {
    alert(`[ERROR] Telegram command failed: ${err.message}`);
  }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', function () {
  initializeTelemetryStream();
});
