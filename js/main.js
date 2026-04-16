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
      `${tech.capability}. Stack: ${tech.stack}`,
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

  profile.innerHTML = `
    <p class="eyebrow">Apollo Technology Profile</p>
    <h1>${tech.name}</h1>
    <p><strong>Stack:</strong> ${tech.stack}</p>
    <p><strong>Current Capability:</strong> ${tech.capability}</p>
    <p><strong>Roadmap Direction:</strong> ${tech.roadmap}</p>
    <div class="profile-actions">
      <a class="btn" href="technologies.html">Back to all technologies</a>
      <a class="btn btn-ghost" href="students.html">View students</a>
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

renderStudentsGrid();
renderTechnologiesGrid();
renderStudentProfile();
renderTechnologyProfile();
revealOnLoad();