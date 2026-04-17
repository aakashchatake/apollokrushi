function createCard(title, text, href, linkLabel) {
  return `
    <article class="card reveal">
      <h3>${title}</h3>
      <p>${text}</p>
      <a href="${href}">${linkLabel}</a>
    </article>
  `;
}

function renderStudentsGrid() {
  const grid = document.getElementById("students-grid");
  if (!grid || typeof APOLLO_STUDENTS === "undefined") return;

  grid.innerHTML = APOLLO_STUDENTS.map((student) =>
    createCard(
      student.name,
      `${student.role}. Focus: ${student.focus}`,
      `student.html?id=${student.id}`,
      "Open Profile"
    )
  ).join("");
}

function renderTechnologiesGrid() {
  const grid = document.getElementById("technologies-grid");
  if (!grid || typeof APOLLO_TECH === "undefined") return;

  grid.innerHTML = APOLLO_TECH.map((tech) =>
    createCard(
      tech.name,
      `${tech.capability}. Stack: ${tech.stack}. Status: ${tech.status}`,
      `technology.html?id=${tech.id}`,
      "Open Technology"
    )
  ).join("");
}

function renderStudentProfile() {
  const profile = document.getElementById("student-profile");
  if (!profile || typeof APOLLO_STUDENTS === "undefined") return;

  const params = new URLSearchParams(window.location.search);
  const id = params.get("id");
  const student = APOLLO_STUDENTS.find((entry) => entry.id === id);

  if (!student) {
    profile.innerHTML = "<h1>Student not found</h1><p>Please return to the students page and choose a profile.</p>";
    return;
  }

  profile.innerHTML = `
    <p class="eyebrow">Team Apollo Student Profile</p>
    <h1>${student.name}</h1>
    <p><strong>Role:</strong> ${student.role}</p>
    <p><strong>Primary Focus:</strong> ${student.focus}</p>
    <p><strong>Email:</strong> ${student.email}</p>
    <p><strong>Affiliation:</strong> ${student.affiliation}</p>
    <p><strong>Current Delivery:</strong> ${student.delivery}</p>
    <div class="profile-actions">
      <a class="btn" href="students.html">Back to all students</a>
      <a class="btn btn-ghost" href="technologies.html">View technologies</a>
    </div>
  `;
}

function renderTechnologyProfile() {
  const profile = document.getElementById("technology-profile");
  if (!profile || typeof APOLLO_TECH === "undefined") return;

  const params = new URLSearchParams(window.location.search);
  const id = params.get("id");
  const tech = APOLLO_TECH.find((entry) => entry.id === id);

  if (!tech) {
    profile.innerHTML = "<h1>Technology not found</h1><p>Please return to the technologies page and choose a profile.</p>";
    return;
  }

  const demoLink = tech.demoUrl
    ? `<p><strong>Live Demo:</strong> <a href="${tech.demoUrl}" target="_blank" rel="noopener noreferrer">Launch ${tech.name}</a></p>`
    : "<p><strong>Live Demo:</strong> Available via Apollo command center deployment plan.</p>";

  profile.innerHTML = `
    <p class="eyebrow">Apollo Technology Profile</p>
    <h1>${tech.name}</h1>
    <p><strong>Stack:</strong> ${tech.stack}</p>
    <p><strong>Current Capability:</strong> ${tech.capability}</p>
    <p><strong>Roadmap Direction:</strong> ${tech.roadmap}</p>
    <p><strong>Implementation Status:</strong> ${tech.status}</p>
    ${demoLink}
    <div class="profile-actions">
      <a class="btn" href="technologies.html">Back to all technologies</a>
      <a class="btn btn-ghost" href="index.html#inference">Open AI workspace</a>
    </div>
  `;
}

function revealOnLoad() {
  const elements = document.querySelectorAll(".reveal");
  elements.forEach((el, index) => {
    el.style.animationDelay = `${Math.min(index * 90, 550)}ms`;
    el.classList.add("visible");
  });
}

function mountStatusGrid() {
  const grid = document.getElementById("statusGrid");
  if (!grid || !Array.isArray(APOLLO_STATUS_STREAM)) return;

  grid.innerHTML = APOLLO_STATUS_STREAM.map((item) => `
    <div class="status-item">
      <strong>${item.module}</strong>
      <span class="status-dot ${item.level}"></span>
    </div>
  `).join("");
}

function mountTelemetryChart() {
  const canvas = document.getElementById("telemetryChart");
  if (!canvas || typeof Chart === "undefined") return;

  const labels = Array.from({ length: 12 }, (_, i) => `${i + 1}m`);
  const values = [67, 70, 68, 73, 75, 79, 76, 81, 83, 80, 85, 87];

  const chart = new Chart(canvas, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "Field Efficiency",
        data: values,
        borderColor: "#58d9a1",
        pointRadius: 2,
        pointBackgroundColor: "#bdfbe0",
        borderWidth: 2,
        tension: 0.35,
        fill: true,
        backgroundColor: "rgba(88, 217, 161, 0.14)"
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          labels: {
            color: "#cbe4db"
          }
        }
      },
      scales: {
        x: {
          ticks: { color: "#99bdb0" },
          grid: { color: "rgba(155, 205, 184, 0.12)" }
        },
        y: {
          ticks: { color: "#99bdb0" },
          grid: { color: "rgba(155, 205, 184, 0.12)" },
          min: 40,
          max: 100
        }
      }
    }
  });

  setInterval(() => {
    const next = Math.min(98, Math.max(58, values[values.length - 1] + (Math.random() * 8 - 4)));
    values.push(Number(next.toFixed(1)));
    values.shift();
    chart.data.datasets[0].data = values;
    chart.update("none");
  }, 2500);
}

async function mountWeatherNode() {
  const temp = document.getElementById("tempValue");
  const wind = document.getElementById("windValue");
  const rain = document.getElementById("rainValue");
  const source = document.getElementById("weatherSource");
  const weatherMetric = document.getElementById("metric-weather");
  if (!temp || !wind || !rain || !source) return;

  try {
    const url = "https://api.open-meteo.com/v1/forecast?latitude=17.6599&longitude=75.9064&current=temperature_2m,wind_speed_10m,rain";
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error("weather api failed");
    }

    const data = await response.json();
    const current = data.current || {};

    temp.textContent = `${current.temperature_2m ?? "--"} C`;
    wind.textContent = `${current.wind_speed_10m ?? "--"} km/h`;
    rain.textContent = `${current.rain ?? "--"} mm`;
    source.textContent = "Live Feed";
    if (weatherMetric) {
      weatherMetric.textContent = `${current.temperature_2m ?? "--"} C`;
    }
  } catch (_error) {
    temp.textContent = "31 C";
    wind.textContent = "11 km/h";
    rain.textContent = "0.0 mm";
    source.textContent = "Fallback";
    if (weatherMetric) {
      weatherMetric.textContent = "31 C";
    }
  }
}

function mockInference(fileName, cropInput) {
  const crop = (cropInput || "wheat").toLowerCase();
  const confidence = (87 + Math.random() * 10).toFixed(2);
  const issues = [
    "Healthy leaf pattern",
    "Mild nutrient stress",
    "Possible fungal risk",
    "Moisture imbalance"
  ];
  const advice = {
    wheat: "Monitor irrigation cycle and inspect lower leaves in next 24h.",
    rice: "Schedule nutrient check and verify standing water consistency.",
    cotton: "Inspect underside for early pest signature and tune spray schedule.",
    default: "Perform field scan and cross-validate with disease model service."
  };

  return {
    mode: "demo",
    file: fileName,
    crop,
    confidence,
    finding: issues[Math.floor(Math.random() * issues.length)],
    recommendation: advice[crop] || advice.default
  };
}

function mountInferenceWorkspace() {
  const imageInput = document.getElementById("imageInput");
  const cropInput = document.getElementById("cropInput");
  const apiInput = document.getElementById("apiInput");
  const runBtn = document.getElementById("runInferenceBtn");
  const demoBtn = document.getElementById("runDemoBtn");
  const resultConsole = document.getElementById("resultConsole");
  const previewImage = document.getElementById("previewImage");
  const previewPlaceholder = document.getElementById("previewPlaceholder");

  if (!imageInput || !runBtn || !demoBtn || !resultConsole) return;

  let selectedFile = null;
  if (apiInput && APOLLO_CONFIG && APOLLO_CONFIG.defaultInferenceApi) {
    apiInput.value = APOLLO_CONFIG.defaultInferenceApi;
  }

  imageInput.addEventListener("change", (event) => {
    const file = event.target.files && event.target.files[0];
    if (!file) return;
    selectedFile = file;

    const objectUrl = URL.createObjectURL(file);
    previewImage.src = objectUrl;
    previewImage.hidden = false;
    if (previewPlaceholder) {
      previewPlaceholder.hidden = true;
    }
  });

  demoBtn.addEventListener("click", () => {
    if (!selectedFile) {
      resultConsole.textContent = "Upload an image first to run demo inference.";
      return;
    }

    const output = mockInference(selectedFile.name, cropInput ? cropInput.value : "");
    resultConsole.textContent = JSON.stringify(output, null, 2);
  });

  runBtn.addEventListener("click", async () => {
    if (!selectedFile) {
      resultConsole.textContent = "Upload an image first, then run AI analysis.";
      return;
    }

    const endpoint = apiInput && apiInput.value ? apiInput.value.trim() : "";
    if (!endpoint) {
      resultConsole.textContent = "Please provide an inference API endpoint or use Demo Mode.";
      return;
    }

    resultConsole.textContent = "Running inference request...";

    const payload = new FormData();
    payload.append("file", selectedFile);
    payload.append("crop", cropInput && cropInput.value ? cropInput.value : "");

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        body: payload
      });
      if (!response.ok) {
        throw new Error(`Inference API returned ${response.status}`);
      }

      const result = await response.json();
      resultConsole.textContent = JSON.stringify(result, null, 2);
    } catch (error) {
      const fallback = mockInference(selectedFile.name, cropInput ? cropInput.value : "");
      resultConsole.textContent = `Live endpoint failed: ${error.message}\n\nFallback demo result:\n${JSON.stringify(fallback, null, 2)}`;
    }
  });
}

function hydrateMetrics() {
  const studentMetric = document.getElementById("metric-students");
  const techMetric = document.getElementById("metric-tech");
  if (studentMetric && Array.isArray(APOLLO_STUDENTS)) {
    studentMetric.textContent = String(APOLLO_STUDENTS.length);
  }
  if (techMetric && Array.isArray(APOLLO_TECH)) {
    techMetric.textContent = `${APOLLO_TECH.length}+`;
  }
}

renderStudentsGrid();
renderTechnologiesGrid();
renderStudentProfile();
renderTechnologyProfile();
mountStatusGrid();
mountTelemetryChart();
mountWeatherNode();
mountInferenceWorkspace();
hydrateMetrics();
revealOnLoad();
