// Publication state lives in assets/release-state.js.
// Full-conference waves can be activated with one boolean; custom waves can use team overrides.
// Unreleased PDFs should not be uploaded to this public repository.

const conferences = [
  {
    name: "ACC",
    slug: "acc",
    reviewFile: "pdfs/conference-reviews/ACC_2026_Preseason_Review.pdf",
    reviewAvailable: true,
    teams: [
      "Boston College", "California", "Clemson", "Duke", "Florida State", "Georgia Tech",
      "Louisville", "Miami", "NC State", "North Carolina", "Pitt", "SMU", "Stanford",
      "Syracuse", "Virginia", "Virginia Tech", "Wake Forest"
    ]
  },
  {
    name: "Big Ten",
    slug: "big-ten",
    reviewFile: "pdfs/conference-reviews/Big_Ten_2026_Preseason_Review.pdf",
    reviewAvailable: false,
    teams: [
      "Illinois", "Indiana", "Iowa", "Maryland", "Michigan", "Michigan State", "Minnesota",
      "Nebraska", "Northwestern", "Ohio State", "Oregon", "Penn State", "Purdue", "Rutgers",
      "UCLA", "USC", "Washington", "Wisconsin"
    ]
  },
  {
    name: "Big 12",
    slug: "big-12",
    reviewFile: "pdfs/conference-reviews/Big_12_2026_Preseason_Review.pdf",
    reviewAvailable: false,
    teams: [
      "Arizona", "Arizona State", "Baylor", "BYU", "Cincinnati", "Colorado", "Houston",
      "Iowa State", "Kansas", "Kansas State", "Oklahoma State", "TCU", "Texas Tech", "UCF",
      "Utah", "West Virginia"
    ]
  },
  {
    name: "SEC",
    slug: "sec",
    reviewFile: "pdfs/conference-reviews/SEC_2026_Preseason_Review.pdf",
    reviewAvailable: false,
    teams: [
      "Alabama", "Arkansas", "Auburn", "Florida", "Georgia", "Kentucky", "LSU", "Mississippi State",
      "Missouri", "Oklahoma", "Ole Miss", "South Carolina", "Tennessee", "Texas", "Texas A&M", "Vanderbilt"
    ]
  },
  {
    name: "Notre Dame",
    slug: "notre-dame",
    reviewFile: null,
    reviewAvailable: false,
    teams: ["Notre Dame"]
  }
];

const releaseState = window.CFB_RELEASE_STATE || { conferences: {}, teams: {} };

// Preserve the existing site display name "Pitt" while matching the project's canonical PDF filename.
const filenameOverrides = {
  "Pitt": "Pittsburgh",
};

function isTeamAvailable(conference, team) {
  return Boolean(releaseState.conferences[conference.name] || releaseState.teams[team]);
}

function fileSafe(team) {
  return team.replace(/\s+/g, "_");
}

function teamFile(conference, team) {
  const fileTeam = filenameOverrides[team] || team;
  return `pdfs/${conference.slug}/${fileSafe(fileTeam)}_2026_Preseason_Primer.pdf`;
}

function render() {
  const query = document.getElementById("team-search").value.trim().toLowerCase();
  const onlyAvailable = document.getElementById("available-only").checked;
  const grid = document.getElementById("conference-grid");
  grid.innerHTML = "";

  let shownTeams = 0;
  let availableCount = 0;

  conferences.forEach(conf => {
    const matchingTeams = conf.teams.filter(team => {
      const isAvailable = isTeamAvailable(conf, team);
      if (isAvailable) availableCount += 1;
      const textMatch = !query || `${team} ${conf.name}`.toLowerCase().includes(query);
      const availabilityMatch = !onlyAvailable || isAvailable;
      return textMatch && availabilityMatch;
    });

    if (!matchingTeams.length) return;
    shownTeams += matchingTeams.length;

    const card = document.createElement("article");
    card.className = "conference-card";

    const availableInConf = conf.teams.filter(t => isTeamAvailable(conf, t)).length;
    const header = document.createElement("div");
    header.className = "conference-header";
    header.innerHTML = `<h3>${conf.name}</h3><span class="conference-count">${availableInConf} / ${conf.teams.length} available</span>`;
    card.appendChild(header);

    if (conf.reviewFile) {
      const review = document.createElement("div");
      review.className = "conference-review";
      review.innerHTML = conf.reviewAvailable
        ? `<span>Conference Review</span><a class="team-link" href="${conf.reviewFile}" target="_blank" rel="noopener">View PDF ↗</a>`
        : `<span>Conference Review</span><span>Coming soon</span>`;
      card.appendChild(review);
    }

    const list = document.createElement("ul");
    list.className = "team-list";
    matchingTeams.forEach(team => {
      const isAvailable = isTeamAvailable(conf, team);
      const row = document.createElement("li");
      row.className = "team-row";
      row.innerHTML = isAvailable
        ? `<span class="team-name">${team}</span><a class="team-link" href="${teamFile(conf, team)}" target="_blank" rel="noopener">View PDF ↗</a>`
        : `<span class="team-name">${team}</span><span class="team-coming">Coming soon</span>`;
      list.appendChild(row);
    });
    card.appendChild(list);
    grid.appendChild(card);
  });

  // Count availability independently of filters for the hero statistic.
  const totalAvailable = conferences.reduce((sum, conf) => sum + conf.teams.filter(team => isTeamAvailable(conf, team)).length, 0);
  document.getElementById("available-count").textContent = totalAvailable;
  document.getElementById("no-results").hidden = shownTeams !== 0;
}

document.getElementById("team-search").addEventListener("input", render);
document.getElementById("available-only").addEventListener("change", render);
render();
