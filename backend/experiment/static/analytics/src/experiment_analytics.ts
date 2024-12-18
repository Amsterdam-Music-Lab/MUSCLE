declare const BLOCK_EXPORT_DATA_URL: string;
declare const blockId: string;
declare const Chart: any;

interface SessionFields {
  block: number;
  participant: number;
  playlist: number;
  started_at: string;
  finished_at: string | null;
  json_data: any;
  final_score: number;
}

interface Session {
  model: string;
  pk: number;
  fields: SessionFields;
}

interface ParticipantFields {
  unique_hash: string;
  country_code: string | null;
  access_info: string;
  participant_id_url: string | null;
}

interface Participant {
  model: string;
  pk: number;
  fields: ParticipantFields;
}

interface ResultFields {
  session: number | null;
  participant: number | null;
  section: number | null;
  created_at: string;
  question_key: string;
  expected_response: string | null;
  given_response: string | null;
  comment: string;
  score: number | null;
  scoring_rule: string;
  json_data: any;
}

interface Result {
  model: string;
  pk: number;
  fields: ResultFields;
}

interface BlockData {
  sessions: string;
  participants: string;
  results: string;
  // add other fields if necessary
}

// Helper function to format date strings (YYYY-MM-DD)
function formatDate(dateStr: string): string {
  return dateStr.slice(0, 10);
}

// Process and transform data into structures used by charts
function processData(sessions: Session[], participants: Participant[], results: Result[]) {
  // Filter completed sessions
  const completedSessions = sessions.filter(s => s.fields.finished_at !== null);

  // SESSIONS BY DATE (For line chart)
  const sessionsByDate: Record<string, number> = {};
  completedSessions.forEach(session => {
    const date = formatDate(session.fields.finished_at!);
    sessionsByDate[date] = (sessionsByDate[date] || 0) + 1;
  });

  const completionDates = Object.keys(sessionsByDate).sort();
  const completionCounts = completionDates.map(d => sessionsByDate[d]);

  // FINAL SCORES (For bar chart)
  const finalScores = completedSessions.map(s => s.fields.final_score);
  const scoreCounts: Record<string, number> = {};
  finalScores.forEach(score => {
    const scoreStr = String(score);
    scoreCounts[scoreStr] = (scoreCounts[scoreStr] || 0) + 1;
  });
  const scoreLabels = Object.keys(scoreCounts);
  const scoreData = Object.values(scoreCounts);

  // COUNTRY DISTRIBUTION (For pie chart)
  const countryCounts: Record<string, number> = {};
  participants.forEach(p => {
    const cc = p.fields.country_code || 'unknown';
    countryCounts[cc] = (countryCounts[cc] || 0) + 1;
  });
  const countryLabels = Object.keys(countryCounts);
  const countryData = Object.values(countryCounts);

  // COMPLETION RATE BY PARTICIPANT
  const participantIds = participants.map(p => p.pk);
  const sessionsByParticipant: Record<number, { started: number; completed: number }> = {};
  participantIds.forEach(pid => sessionsByParticipant[pid] = { started: 0, completed: 0 });

  sessions.forEach(s => {
    const pid = s.fields.participant;
    if (!sessionsByParticipant[pid]) {
      sessionsByParticipant[pid] = { started: 0, completed: 0 };
    }
    sessionsByParticipant[pid].started += 1;
    if (s.fields.finished_at !== null) {
      sessionsByParticipant[pid].completed += 1;
    }
  });

  const completionLabels = participantIds.map(pid => `P${pid}`);
  const startedData = participantIds.map(pid => sessionsByParticipant[pid]?.started || 0);
  const completedData = participantIds.map(pid => sessionsByParticipant[pid]?.completed || 0);

  // DURATION DISTRIBUTION
  function getDurationMinutes(start: string, end: string): number {
    const startDate = new Date(start);
    const endDate = new Date(end);
    const minutes = (endDate.getTime() - startDate.getTime()) / 60000;
    return Math.max(minutes, 0);
  }

  const durations = completedSessions.map(s => getDurationMinutes(s.fields.started_at, s.fields.finished_at!));
  const binSize = 1; // 1-minute bins
  const maxDuration = Math.ceil(Math.max(...durations, 0));
  const durationBins: number[] = [];
  for (let i = 0; i <= maxDuration; i += binSize) {
    durationBins.push(i);
  }
  const durationCounts = Array(durationBins.length).fill(0);
  durations.forEach(d => {
    const binIndex = Math.min(Math.floor(d / binSize), durationBins.length - 1);
    durationCounts[binIndex] += 1;
  });
  const durationLabels = durationBins.map(b => `${b}-${b + binSize}min`);

  // ACCURACY OVER TIME
  const dailyResults: Record<string, { correct: number; total: number }> = {};
  results.forEach(r => {
    const date = formatDate(r.fields.created_at);
    if (!dailyResults[date]) dailyResults[date] = { correct: 0, total: 0 };
    const score = r.fields.score;
    if (score !== null) {
      dailyResults[date].total += 1;
      if (score === 20.0) {
        dailyResults[date].correct += 1;
      }
    }
  });

  const accuracyDates = Object.keys(dailyResults).sort();
  const accuracyValues = accuracyDates.map(d => {
    const dayData = dailyResults[d];
    return dayData.total > 0 ? (dayData.correct / dayData.total) * 100.0 : 0;
  });

  return {
    scoreLabels, scoreData,
    completionDates, completionCounts,
    countryLabels, countryData,
    completionLabels, startedData, completedData,
    durationLabels, durationCounts,
    accuracyDates, accuracyValues
  };
}

// Functions to create each chart
function createScoreChart(labels: string[], data: number[]) {
  const scoreChartCanvas = document.getElementById('scoreChart') as HTMLCanvasElement;
  const ctxScore = scoreChartCanvas.getContext('2d');
  new Chart(ctxScore, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Count of Completed Sessions by Final Score',
        data: data,
        backgroundColor: 'rgba(54, 162, 235, 0.5)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
}

function createCompletionOverTimeChart(dates: string[], counts: number[]) {
  const completionChartCanvas = document.getElementById('completionChart') as HTMLCanvasElement;
  const ctxCompletion = completionChartCanvas.getContext('2d');
  new Chart(ctxCompletion, {
    type: 'line',
    data: {
      labels: dates,
      datasets: [{
        label: 'Sessions Completed Per Day',
        data: counts,
        fill: false,
        borderColor: 'rgba(255,99,132,1)',
        tension: 0.1
      }]
    },
    options: {
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
}

function createCountryChart(labels: string[], data: number[]) {
  const countryChartCanvas = document.getElementById('countryChart') as HTMLCanvasElement;
  const ctxCountry = countryChartCanvas.getContext('2d');
  new Chart(ctxCountry, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: [
          'rgba(255, 99, 132, 0.5)',
          'rgba(54, 162, 235, 0.5)',
          'rgba(255, 206, 86, 0.5)',
          'rgba(75, 192, 192, 0.5)'
        ]
      }]
    },
    options: {
      responsive: true
    }
  });
}

function createParticipantCompletionChart(labels: string[], started: number[], completed: number[]) {
  const completionChartCanvasTwo = document.getElementById('completionChartTwo') as HTMLCanvasElement;
  const ctxCompletionTwo = completionChartCanvasTwo.getContext('2d');
  new Chart(ctxCompletionTwo, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Started',
          data: started,
          backgroundColor: 'rgba(54, 162, 235, 0.5)'
        },
        {
          label: 'Completed',
          data: completed,
          backgroundColor: 'rgba(75, 192, 192, 0.5)'
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
}

function createDurationChart(labels: string[], counts: number[]) {
  const durationChartCanvas = document.getElementById('durationChart') as HTMLCanvasElement;
  const ctxDuration = durationChartCanvas.getContext('2d');
  new Chart(ctxDuration, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Session Count',
        data: counts,
        backgroundColor: 'rgba(153, 102, 255, 0.5)',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: function (context) {
              return `Count: ${context.parsed.y}`;
            }
          }
        }
      }
    }
  });
}

function createAccuracyChart(dates: string[], values: number[]) {
  const accuracyChartCanvas = document.getElementById('accuracyChart') as HTMLCanvasElement;
  const ctxAccuracy = accuracyChartCanvas.getContext('2d');
  new Chart(ctxAccuracy, {
    type: 'line',
    data: {
      labels: dates,
      datasets: [{
        label: 'Daily Accuracy (%)',
        data: values,
        borderColor: 'rgba(255,99,132,1)',
        fill: false,
        tension: 0.1
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          suggestedMax: 100
        }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: function (context) {
              return `Accuracy: ${context.parsed.y.toFixed(2)}%`;
            }
          }
        }
      }
    }
  });
}

// Initialize all charts
function initializeCharts(data: BlockData) {
  const sessions: Session[] = JSON.parse(data.sessions);
  const participants: Participant[] = JSON.parse(data.participants);
  const results: Result[] = JSON.parse(data.results);

  const {
    scoreLabels, scoreData,
    completionDates, completionCounts,
    countryLabels, countryData,
    completionLabels, startedData, completedData,
    durationLabels, durationCounts,
    accuracyDates, accuracyValues
  } = processData(sessions, participants, results);

  createScoreChart(scoreLabels, scoreData);
  createCompletionOverTimeChart(completionDates, completionCounts);
  createCountryChart(countryLabels, countryData);
  createParticipantCompletionChart(completionLabels, startedData, completedData);
  createDurationChart(durationLabels, durationCounts);
  createAccuracyChart(accuracyDates, accuracyValues);
}

async function fetchAnalyticsData() {
  let data: BlockData;
  const errorElement = document.getElementById('error');

  try {
    const response = await fetch(BLOCK_EXPORT_DATA_URL);
    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }
    data = await response.json();
    initializeCharts(data);
  } catch (error: any) {
    const statusCode = error.response ? error.response.status : 500;
    const notFound = statusCode === 404;
    const errorMessage = notFound ? 'The data for this block is not available.' : 'An error occurred while fetching data.';
    if (errorElement) {
      errorElement.textContent = errorMessage;
      const refreshButton = document.createElement('button');
      refreshButton.textContent = 'Refresh';
      refreshButton.onclick = () => {
        window.location.reload();
      };
      errorElement.appendChild(refreshButton);
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  fetchAnalyticsData();
});
