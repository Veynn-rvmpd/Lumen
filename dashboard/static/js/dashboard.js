/**
 * LUMEN Executive Dashboard Real-Time Client Controller.
 * Establishes SSE telemetry stream, handles asynchronous REST dispatches,
 * powers the command palette (Ctrl+K), and renders data visualizations with zero emojis.
 */

// Command Palette Registry
const COMMAND_PALETTE_ITEMS = [
  { title: "Switch to Focus Profile", category: "Environment", action: () => switchProfile("Focus") },
  { title: "Switch to Dev Profile", category: "Environment", action: () => switchProfile("Dev") },
  { title: "Switch to Meeting Profile", category: "Environment", action: () => switchProfile("Meeting") },
  { title: "Open Personal Finance Hub", category: "Navigation", action: () => selectTabByName("financeTab") },
  { title: "Open Productivity & Decisions", category: "Navigation", action: () => selectTabByName("productivityTab") },
  { title: "Open Code & Writing Auditor", category: "Navigation", action: () => selectTabByName("codeTab") },
  { title: "Open Athletics & Odds Hub", category: "Navigation", action: () => selectTabByName("fitnessTab") },
  { title: "Open Procurement & Review", category: "Navigation", action: () => selectTabByName("procureTab") },
  { title: "Open Filesystem Sentinel", category: "Navigation", action: () => selectTabByName("filesTab") },
  { title: "Open Gmail Inbox Triage", category: "Navigation", action: () => selectTabByName("commsTab") },
  { title: "Open Applied Philosophy", category: "Navigation", action: () => selectTabByName("philosophyTab") },
  { title: "Open Image Studio", category: "Navigation", action: () => selectTabByName("imageTab") },
  { title: "Calculate Compound Growth", category: "Finance", action: () => { selectTabByName("financeTab"); runCompoundProjection(); } },
  { title: "Generate 50/30/20 Budget Breakdown", category: "Finance", action: () => { selectTabByName("financeTab"); runBudgetBreakdown(); } },
  { title: "Generate Timeboxed Schedule", category: "Productivity", action: () => { selectTabByName("productivityTab"); generateTimeboxSchedule(); } },
  { title: "Sort Tasks into Eisenhower Quadrants", category: "Productivity", action: () => { selectTabByName("productivityTab"); runEisenhowerSort(); } },
  { title: "Audit Python Code Snippet", category: "Code", action: () => { selectTabByName("codeTab"); runCodeAudit(); } },
  { title: "Audit Prose Clarity & Fillers", category: "Writing", action: () => { selectTabByName("codeTab"); runProseAudit(); } },
  { title: "Scan Large Files (>100MB)", category: "Sentinel", action: () => { selectTabByName("filesTab"); scanLargeFiles(); } },
  { title: "Run Gmail Inbox Triage", category: "Inbox", action: () => { selectTabByName("commsTab"); runGmailTriage(); } },
  { title: "Toggle Spotify Playback", category: "Media", action: () => controlSpotify("toggle") },
  { title: "Dispatch WhatsApp Priority Alert", category: "Messaging", action: () => dispatchWhatsAppAlert() }
];

let activePaletteIndex = 0;
let filteredPaletteItems = [...COMMAND_PALETTE_ITEMS];

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

function selectTabByName(tabId) {
  const targetBtn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.getAttribute('onclick')?.includes(tabId));
  selectTab(tabId, targetBtn);
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

async function runBudgetBreakdown() {
  const output = document.getElementById('financeOutput');
  output.innerText = '[PROCESSING] Generating 50/30/20 budget allocation...';

  try {
    const monthlyIncome = parseFloat(document.getElementById('monthlyContribution').value) * 4 || 3200;
    const response = await fetch('/api/finance/budget', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ monthlyNetIncome: monthlyIncome, framework: '50_30_20' })
    });
    const result = await response.json();

    let text = `[BUDGET BREAKDOWN (${result.frameworkUsed})]\n`;
    text += `Monthly Net Income: ${result.monthlyNetIncome.toFixed(2)} EUR\n\n`;
    text += `ALLOCATIONS:\n`;
    text += `- Needs (50% Essential):        ${result.allocatedNeeds.toFixed(2)} EUR / month\n`;
    text += `- Wants (30% Discretionary):    ${result.allocatedWants.toFixed(2)} EUR / month\n`;
    text += `- Savings & Invest (20% Floor): ${result.allocatedSavingsInvestment.toFixed(2)} EUR / month\n\n`;
    text += `Annual Capital Accumulation Capacity: ${result.annualSavingsCapacity.toFixed(2)} EUR`;

    output.innerText = text;
  } catch (err) {
    output.innerText = `[ERROR] Budget breakdown failed: ${err.message}`;
  }
}

async function runEmergencyFund() {
  const output = document.getElementById('financeOutput');
  output.innerText = '[PROCESSING] Computing emergency cash reserve...';

  try {
    const response = await fetch('/api/finance/emergency', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ monthlyBasicExpenses: 1750.0, incomeStability: 'stable' })
    });
    const result = await response.json();

    let text = `[EMERGENCY RESERVE MANDATE]\n`;
    text += `Baseline Non-Discretionary Expenses: ${result.monthlyBasicExpenses.toFixed(2)} EUR / month\n`;
    text += `Income Stability Rating: ${result.incomeStability}\n`;
    text += `Recommended Reserve Coverage: ${result.coverageMonths} Months\n`;
    text += `Target Cash Cushion: ${result.recommendedCashReserve.toFixed(2)} EUR\n`;
    text += `Holding Vehicle: ${result.holdingVehicle}`;

    output.innerText = text;
  } catch (err) {
    output.innerText = `[ERROR] Emergency fund calculation failed: ${err.message}`;
  }
}

// Productivity & Decisions
async function generateTimeboxSchedule() {
  const output = document.getElementById('productivityOutput');
  const focusTask = document.getElementById('timeboxFocus').value || "Distributed Architecture Execution";
  const meetings = parseInt(document.getElementById('timeboxMeetings').value, 10) || 2;
  output.innerText = '[PROCESSING] Compiling structured workday blocks...';

  try {
    const response = await fetch('/api/productivity/timebox', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ startHour: 8, endHour: 18, focusTask: focusTask, meetingBlocks: meetings })
    });
    const result = await response.json();

    let text = `[TIMEBOXED SCHEDULE: 08:00 - 18:00]\n`;
    text += `Focus Core: "${focusTask}" | Meeting Allowance: ${meetings}h\n\n`;
    result.schedule.forEach(slot => {
      text += `[${slot.timeRange}] ${slot.blockType.toUpperCase()}: ${slot.activity}\n`;
      text += `    Protocol: ${slot.protocol}\n\n`;
    });

    output.innerText = text;
  } catch (err) {
    output.innerText = `[ERROR] Timebox compilation failed: ${err.message}`;
  }
}

async function runEisenhowerSort() {
  const output = document.getElementById('productivityOutput');
  output.innerText = '[PROCESSING] Classifying task queue into Eisenhower matrix quadrants...';

  try {
    const response = await fetch('/api/productivity/eisenhower', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({}) });
    const result = await response.json();

    let text = `[EISENHOWER PRIORITIZATION MATRIX]\n\n`;
    text += `Q1: DO IMMEDIATELY (Urgent & Important) [${result.Q1_DoImmediately.length} items]:\n`;
    result.Q1_DoImmediately.forEach(t => text += `  - [${t.priority}] ${t.title} (Due: ${t.dueDate})\n`);

    text += `\nQ2: SCHEDULE DEEP WORK (Not Urgent, Important) [${result.Q2_ScheduleDeepWork.length} items]:\n`;
    result.Q2_ScheduleDeepWork.forEach(t => text += `  - [${t.priority}] ${t.title} (Due: ${t.dueDate})\n`);

    text += `\nQ3: DELEGATE OR AUTOMATE (Urgent, Not Important) [${result.Q3_DelegateOrAutomate.length} items]:\n`;
    result.Q3_DelegateOrAutomate.forEach(t => text += `  - [${t.priority}] ${t.title}\n`);

    text += `\nQ4: ELIMINATE / DEFER (Neither) [${result.Q4_Eliminate.length} items]:\n`;
    result.Q4_Eliminate.forEach(t => text += `  - ${t.title}\n`);

    output.innerText = text;
  } catch (err) {
    output.innerText = `[ERROR] Eisenhower classification failed: ${err.message}`;
  }
}

async function runDecisionMatrix() {
  const output = document.getElementById('productivityOutput');
  output.innerText = '[PROCESSING] Evaluating weighted multi-criteria decision model...';

  try {
    const response = await fetch('/api/productivity/matrix', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({}) });
    const result = await response.json();

    let text = `[WEIGHTED DECISION SCORING MODEL]\n`;
    text += `Weights Applied: Impact (40%), Feasibility (35%), Speed (25%)\n\n`;
    text += `RANKED CANDIDATES:\n`;
    result.rankedResults.forEach((cand, idx) => {
      text += `${idx + 1}. ${cand.name} -> Score: ${cand.weightedScore} / 10\n`;
      text += `   Breakdown: Impact=${cand.breakdown.impact}, Feasibility=${cand.breakdown.feasibility}, Speed=${cand.breakdown.speed}\n`;
    });
    text += `\nRECOMMENDED ACTION: ${result.guidance}`;

    output.innerText = text;
  } catch (err) {
    output.innerText = `[ERROR] Decision matrix failed: ${err.message}`;
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

async function checkExerciseTechnique() {
  const output = document.getElementById('fitnessOutput');
  const exercise = document.getElementById('exerciseSelect').value;

  try {
    const response = await fetch('/api/fitness/technique', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ exercise: exercise })
    });
    const result = await response.json();

    let text = `[BIOMECHANICAL CUE CHECKLIST: ${result.exercise}]\n\n`;
    text += `KEY MECHANICAL CUES:\n`;
    result.biomechanicalCues.forEach(c => text += `- ${c}\n`);
    text += `\nPRIMARY FAILURE POINTS & COMPENSATION:\n`;
    result.primaryFailurePoints.forEach(f => text += `- ${f}\n`);
    text += `\nSAFETY MANDATE: ${result.injuryPreventionRule}`;

    output.innerText = text;
  } catch (err) {
    output.innerText = `[ERROR] Form check failed: ${err.message}`;
  }
}

async function refreshScoreboard() {
  const output = document.getElementById('fitnessOutput');

  try {
    const response = await fetch('/api/fitness/scoreboard');
    const matches = await response.json();

    let text = `[TRACKED SPORTS SCOREBOARD]\n\n`;
    matches.forEach(m => {
      text += `[${m.status}] ${m.tournament}: ${m.match} (${m.score})\n`;
    });

    output.innerText = text;
  } catch (err) {
    output.innerText = `[ERROR] Scoreboard fetch failed: ${err.message}`;
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

// Filesystem Sentinel
async function scanLargeFiles() {
  const output = document.getElementById('filesOutput');
  const path = document.getElementById('scanDirectory').value;
  const thresh = parseFloat(document.getElementById('sizeThreshold').value) || 100;
  output.innerText = `[PROCESSING] Scanning directory '${path}' for files > ${thresh}MB...`;

  try {
    const response = await fetch('/api/files/large', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ directory: path, thresholdMb: thresh })
    });
    const result = await response.json();

    let text = `[FILESYSTEM LARGE ARTIFACTS SCAN]\n`;
    text += `Directory: ${result.directory} | Large Files Detected: ${result.count}\n\n`;
    if (result.largeFiles.length === 0) {
      text += `No files exceeding ${thresh}MB threshold found. Storage is healthy.\n`;
    } else {
      result.largeFiles.forEach(f => {
        text += `- ${f.sizeMb} MB | ${f.fileName} (${f.filePath})\n`;
      });
    }

    output.innerText = text;
  } catch (err) {
    output.innerText = `[ERROR] Storage scan failed: ${err.message}`;
  }
}

async function organizeFiles(isDryRun) {
  const output = document.getElementById('filesOutput');
  const path = document.getElementById('scanDirectory').value;
  output.innerText = `[PROCESSING] Inspecting folder '${path}' organization...`;

  try {
    const response = await fetch('/api/files/organize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ directory: path, dryRun: isDryRun })
    });
    const result = await response.json();

    let text = `[FILESYSTEM REORGANIZATION PLAN] (DryRun: ${result.dryRun})\n`;
    text += `Target Directory: ${result.targetDirectory} | Planned Movements: ${result.totalFilesPlanned}\n\n`;
    result.actions.forEach(a => {
      text += `Move: "${a.fileName}" -> "${a.targetFolder}/"\n`;
    });

    output.innerText = text;
  } catch (err) {
    output.innerText = `[ERROR] File organization failed: ${err.message}`;
  }
}

async function cleanGarbageFiles(isDryRun) {
  const output = document.getElementById('filesOutput');
  const path = document.getElementById('scanDirectory').value;
  output.innerText = `[PROCESSING] Scanning harmless garbage files in '${path}'...`;

  try {
    const response = await fetch('/api/files/clean', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ directory: path, dryRun: isDryRun })
    });
    const result = await response.json();

    let text = `[TEMPORARY STORAGE RECOVERY] (DryRun: ${result.dryRun})\n`;
    text += `Artifacts Identified: ${result.filesIdentified} | Recoverable Space: ${result.freedSpaceKb} KB\n\n`;
    result.files.forEach(f => text += `Candidate: ${f}\n`);

    output.innerText = text;
  } catch (err) {
    output.innerText = `[ERROR] Temporary garbage scan failed: ${err.message}`;
  }
}

// Gmail & Communications
async function runGmailTriage() {
  const output = document.getElementById('commsOutput');
  output.innerText = '[PROCESSING] Classifying correspondence streams...';

  try {
    const response = await fetch('/api/gmail/triage');
    const result = await response.json();

    let text = `[GMAIL INBOX TRIAGE AUDIT]\n`;
    text += `Total Messages Inspected: ${result.totalInspected}\n`;
    text += `- Priority Security Alerts: ${result.priorityAlertsCount}\n`;
    text += `- Marketing & Newsletters: ${result.newslettersDetected}\n`;
    text += `- Receipts & Invoices:     ${result.transactionalCount}\n\n`;
    text += `RECOMMENDED DISPATCH: ${result.recommendedAction}\n\n`;
    text += `CANDIDATES FOR MASS ARCHIVAL:\n`;
    result.actionableCandidates.forEach(c => {
      text += `- [${c.category}] From: ${c.sender} | Subject: "${c.subject}"\n`;
    });

    output.innerText = text;
  } catch (err) {
    output.innerText = `[ERROR] Gmail triage failed: ${err.message}`;
  }
}

async function fetchGmailFilters() {
  const output = document.getElementById('commsOutput');

  try {
    const response = await fetch('/api/gmail/filters');
    const result = await response.json();

    let text = `[RECOMMENDED GMAIL XML FILTER RULES]\n\n`;
    result.filterRules.forEach(r => {
      text += `RULE: ${r.ruleName}\n`;
      text += `  Query:  ${r.query}\n`;
      text += `  Action: ${r.action}\n\n`;
    });

    output.innerText = text;
  } catch (err) {
    output.innerText = `[ERROR] Failed to fetch filter rules: ${err.message}`;
  }
}

async function extractUnsubscribeUrls() {
  const output = document.getElementById('commsOutput');
  const body = document.getElementById('emailRawBody').value;
  if (!body) {
    output.innerText = '[NOTICE] Paste email body content into the textarea above first.';
    return;
  }

  try {
    const response = await fetch('/api/gmail/unsubscribe', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ body: body })
    });
    const result = await response.json();

    let text = `[UNSUBSCRIBE HYPERLINK EXTRACTION]\n`;
    text += `Discovered Direct Opt-Out Links: ${result.linksFound}\n\n`;
    result.unsubscribeUrls.forEach((u, i) => {
      text += `${i + 1}. ${u}\n`;
    });

    output.innerText = text;
  } catch (err) {
    output.innerText = `[ERROR] Extraction failed: ${err.message}`;
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

async function detectCognitiveBiases() {
  const output = document.getElementById('philosophyOutput');
  const problem = document.getElementById('problemDescription').value;

  try {
    const response = await fetch('/api/philosophy/bias', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scenario: problem })
    });
    const result = await response.json();

    let text = `[COGNITIVE BIAS DETECTION & MITIGATION]\n`;
    text += `Biases Isolated: ${result.biasesDetected}\n\n`;
    result.biasProfiles.forEach(b => {
      text += `BIAS: ${b.bias}\n`;
      text += `  Mechanism: ${b.mechanism}\n`;
      text += `  Remedy:    ${b.remedy}\n\n`;
    });

    output.innerText = text;
  } catch (err) {
    output.innerText = `[ERROR] Bias analysis failed: ${err.message}`;
  }
}

async function generateDeliberatePractice() {
  const output = document.getElementById('philosophyOutput');
  const skill = document.getElementById('skillPractice').value || "Architecture Profiling";

  try {
    const response = await fetch('/api/philosophy/practice', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ skill: skill })
    });
    const result = await response.json();

    let text = `[DELIBERATE PRACTICE PROTOCOL: ${result.skill}]\n`;
    text += `Framework: ${result.framework}\n\n`;
    text += `1. Chunking:           ${result.phase1_Chunking}\n`;
    text += `2. Friction Threshold: ${result.phase2_Friction}\n`;
    text += `3. Immediate Feedback: ${result.phase3_ImmediateFeedback}\n`;
    text += `4. Rest & Repetition:  ${result.phase4_RestRepetition}\n`;

    output.innerText = text;
  } catch (err) {
    output.innerText = `[ERROR] Deliberate practice generation failed: ${err.message}`;
  }
}

// Image Studio Actions
async function inspectLocalImage() {
  const output = document.getElementById('imageOutput');
  const path = document.getElementById('imageSourcePath').value;
  if (!path) {
    output.innerText = '[NOTICE] Specify an absolute image source path first.';
    return;
  }

  try {
    const response = await fetch('/api/image/inspect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: path })
    });
    const result = await response.json();

    if (result.status === '[OK]') {
      let text = `[IMAGE ARTIFACT METRICS]\n`;
      text += `File:         ${result.filePath}\n`;
      text += `Format:       ${result.format} (${result.mode})\n`;
      text += `Dimensions:   ${result.width} x ${result.height} px (Aspect: ${result.aspectRatio})\n`;
      text += `Disk Payload: ${result.fileSizeKb} KB\n`;
      output.innerText = text;
    } else {
      output.innerText = `[ERROR] ${result.message}`;
    }
  } catch (err) {
    output.innerText = `[ERROR] Image inspection failed: ${err.message}`;
  }
}

async function compressImageWeb() {
  const output = document.getElementById('imageOutput');
  const src = document.getElementById('imageSourcePath').value;
  const out = document.getElementById('imageOutputPath').value || src.replace(/\.[^.]+$/, '_optimized.webp');
  const fmt = document.getElementById('imageTargetFormat').value;

  try {
    const response = await fetch('/api/image/compress', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sourcePath: src, outputPath: out, format: fmt, quality: 82 })
    });
    const result = await response.json();

    if (result.status === '[OK]') {
      let text = `[IMAGE COMPRESSION REPORT]\n`;
      text += `Original Size:    ${result.originalSizeKb} KB\n`;
      text += `Compressed Size:  ${result.compressedSizeKb} KB\n`;
      text += `Bandwidth Saved:  ${result.spaceSavedPercent}%\n`;
      text += `Exported Format:  ${result.format}\n`;
      text += `Output Location:  ${result.outputPath}\n`;
      output.innerText = text;
    } else {
      output.innerText = `[ERROR] ${result.message}`;
    }
  } catch (err) {
    output.innerText = `[ERROR] Compression failed: ${err.message}`;
  }
}

async function applyWatermarkImage() {
  const output = document.getElementById('imageOutput');
  const src = document.getElementById('imageSourcePath').value;
  const out = document.getElementById('imageOutputPath').value || src.replace(/\.[^.]+$/, '_watermarked.png');
  const markText = document.getElementById('imageWatermarkText').value || "CONFIDENTIAL";

  try {
    const response = await fetch('/api/image/watermark', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sourcePath: src, outputPath: out, text: markText, opacity: 40 })
    });
    const result = await response.json();

    if (result.status === '[OK]') {
      output.innerText = `[OK] Watermark applied successfully.\nText: "${result.text}"\nOutput: ${result.outputPath}`;
    } else {
      output.innerText = `[ERROR] ${result.message}`;
    }
  } catch (err) {
    output.innerText = `[ERROR] Watermarking failed: ${err.message}`;
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
  const message = input.value.trim() || "Priority hardware and operational status review.";

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

// Command Palette (Raycast / Linear Style Ctrl + K)
function openCommandPalette() {
  const backdrop = document.getElementById('commandPaletteBackdrop');
  const input = document.getElementById('commandPaletteInput');
  if (backdrop && input) {
    backdrop.classList.add('active');
    input.value = '';
    filterPaletteCommands('');
    input.focus();
  }
}

function closeCommandPalette() {
  const backdrop = document.getElementById('commandPaletteBackdrop');
  if (backdrop) {
    backdrop.classList.remove('active');
  }
}

function handlePaletteBackdropClick(event) {
  if (event.target.id === 'commandPaletteBackdrop') {
    closeCommandPalette();
  }
}

function filterPaletteCommands(query) {
  const cleanQuery = query.trim().toLowerCase();
  filteredPaletteItems = COMMAND_PALETTE_ITEMS.filter(item =>
    item.title.toLowerCase().includes(cleanQuery) ||
    item.category.toLowerCase().includes(cleanQuery)
  );
  activePaletteIndex = 0;
  renderPaletteResults();
}

function renderPaletteResults() {
  const container = document.getElementById('commandPaletteResults');
  if (!container) return;

  if (filteredPaletteItems.length === 0) {
    container.innerHTML = '<div style="padding: 12px; color: var(--text-muted); font-size: 11px;">No matching commands found.</div>';
    return;
  }

  container.innerHTML = filteredPaletteItems.map((item, idx) => `
    <div class="command-palette-item ${idx === activePaletteIndex ? 'selected' : ''}" onclick="executePaletteCommand(${idx})">
      <span>${item.title}</span>
      <span class="item-category">${item.category}</span>
    </div>
  `).join('');
}

function handlePaletteKeydown(event) {
  if (event.key === 'ArrowDown') {
    event.preventDefault();
    activePaletteIndex = (activePaletteIndex + 1) % filteredPaletteItems.length;
    renderPaletteResults();
  } else if (event.key === 'ArrowUp') {
    event.preventDefault();
    activePaletteIndex = (activePaletteIndex - 1 + filteredPaletteItems.length) % filteredPaletteItems.length;
    renderPaletteResults();
  } else if (event.key === 'Enter') {
    event.preventDefault();
    executePaletteCommand(activePaletteIndex);
  } else if (event.key === 'Escape') {
    closeCommandPalette();
  }
}

function executePaletteCommand(index) {
  const item = filteredPaletteItems[index];
  if (item && item.action) {
    closeCommandPalette();
    item.action();
  }
}

// Global Keyboard Shortcuts
document.addEventListener('keydown', function (event) {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
    event.preventDefault();
    const backdrop = document.getElementById('commandPaletteBackdrop');
    if (backdrop && backdrop.classList.contains('active')) {
      closeCommandPalette();
    } else {
      openCommandPalette();
    }
  } else if (event.key === 'Escape') {
    closeCommandPalette();
  }
});

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', function () {
  initializeTelemetryStream();
});
