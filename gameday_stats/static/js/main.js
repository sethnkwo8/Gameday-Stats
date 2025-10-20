/*!
* Start Bootstrap - Scrolling Nav v5.0.6 (https://startbootstrap.com/template/scrolling-nav)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-scrolling-nav/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

    // Hide all sections initially
    document.querySelectorAll(".section").forEach(section => section.style.display = "none");

    const leagueSelect = document.querySelector("#league_select");
    let selected_league_id = null;

    //  Define loadStandings function
    function loadStandings(leagueId) {
        const tbody = document.querySelector("#standingsTable tbody");
        tbody.innerHTML = "<tr><td colspan='10'>Loading...</td></tr>";

        fetch(`/football/standings/${leagueId}`)
            .then(response => {
                return response.json();
            })
            .then(data => {
                tbody.innerHTML = "";
                data.standings.forEach(item => {
                    const row = `
                    <tr>
                        <td>${item.position}</td>
                        <td><a href="${item.team_id}" style="text-decoration: none; color:black;"><img src='${item.logo}' width="25"> ${item.name}</a></td>
                        <td>${item.played}</td>
                        <td>${item.wins}</td>
                        <td>${item.draws}</td>
                        <td>${item.lost}</td>
                        <td>${item.points}</td>
                        <td>${item.goalsFor}</td>
                        <td>${item.goalsAgainst}</td>
                        <td>${item.goalDifference}</td>
                    </tr>`;
                    tbody.insertAdjacentHTML("beforeend", row);
                });
            })
            .catch(error => {
                console.error("Error loading standings:", error);
                tbody.innerHTML = "<tr><td colspan='10'>Failed to load data</td></tr>";
            });
    }

    // Handle nav tab clicks
    const navLinks = document.querySelectorAll("#select_content .nav-link");
    const sections = document.querySelectorAll(".section");

    // Get saved tab from storage
    const savedTab = localStorage.getItem("activeMainTab");

    // Hide all sections first
    sections.forEach(sec => sec.style.display = "none");

    if (savedTab) {
        // If user has a previous tab saved, restore it
        const defaultSection = document.querySelector(`#${savedTab}-section`);
        if (defaultSection) defaultSection.style.display = "block";

        navLinks.forEach(link => {
            link.classList.toggle("active", link.dataset.section === savedTab);
        });
    } else {
        // If no previous tab, keep all sections hidden and none active
        navLinks.forEach(link => link.classList.remove("active"));
    }

    // ✅ Same event listener logic for tab switching
    navLinks.forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const clicked = e.currentTarget;
            const section = this.dataset.section;

            if (!selected_league_id) {
                alert("Please select a league first!");
                return;
            }

            console.log("Switching to:", section);

            // Save selected tab
            localStorage.setItem("activeMainTab", section);

            // Update active nav
            navLinks.forEach(nav => nav.classList.remove("active"));
            clicked.classList.add("active");

            // Hide all sections
            sections.forEach(sec => sec.style.display = "none");

            // Show the clicked section
            const sectionToShow = document.querySelector(`#${section}-section`);
            if (sectionToShow) sectionToShow.style.display = "block";

            // Load appropriate data
            if (section === "standings") {
                loadStandings(selected_league_id);
            } else if (section === "matches") {
                const matchdaySelect = document.querySelector("#matchday_select");
                if (matchdaySelect && matchdaySelect.value && selected_league_id) {
                    loadMatches(matchdaySelect.value);
                } else {
                    console.warn("No matchday selected or found.");
                }
            } else if (section === "teams") {
                loadTeams(selected_league_id);
            } else if (section === "top_scorers") {
                loadScorers(selected_league_id);
            }
        });
    });


    //  Handle back navigation
    window.addEventListener("pageshow", () => {
        const savedTab = localStorage.getItem("activeMainTab");
        const sections = document.querySelectorAll(".section");
        const navLinks = document.querySelectorAll("#select_content .nav-link");

        // Hide all first
        sections.forEach(sec => sec.style.display = "none");

        // Show only the previously active one
        const sectionToShow = document.querySelector(`#${savedTab}-section`);
        if (sectionToShow) sectionToShow.style.display = "block";

        // Fix nav state
        navLinks.forEach(link => {
            link.classList.toggle("active", link.dataset.section === savedTab);
        });
    });

    // Handle league selection
    if (leagueSelect) {
        leagueSelect.addEventListener("change", function () {
        selected_league_id = this.value;
        console.log("Selected League:", selected_league_id);

        // Hide all sections first
        sections.forEach(sec => sec.style.display = "none");

        // Show only the active tab section
        const savedTab = localStorage.getItem("activeMainTab") || "standings";
        const sectionToShow = document.querySelector(`#${savedTab}-section`);
        if (sectionToShow) sectionToShow.style.display = "block";

        // Load data for that section
        switch (savedTab) {
            case "standings":
                loadStandings(selected_league_id);
                break;
            case "matches":
                if (matchdaySelect && matchdaySelect.value) {
                    loadMatches(matchdaySelect.value);
                }
                break;
            case "teams":
                loadTeams(selected_league_id);
                break;
            case "top_scorers":
                loadScorers(selected_league_id);
                break;
        }
    });
    }

    window.addEventListener("load", () => {
        const activeTab = document.querySelector("#select_content .nav-link.active");
        const matchesSection = document.querySelector("#matches-section");
        const matchdaySelect = document.querySelector("#matchday_select");
        const matchesContent = document.querySelector("#matches");

        // Check if "Matches" tab is active by default
        if (activeTab && activeTab.dataset.section === "matches") {
            matchesSection.style.display = "block";

            // ✅ If a league is already selected on load, fetch matches immediately
            if (leagueSelect.value) {
                selected_league_id = leagueSelect.value;
                console.log("Initial load — Matches tab active for league:", selected_league_id);

                if (matchdaySelect && matchdaySelect.value) {
                    loadMatches(matchdaySelect.value);
                } else {
                    matchesContent.innerHTML = "<p>No matchday selected or found.</p>";
                }
            } else {
                matchesContent.innerHTML = "<p>Please select a league to view matches.</p>";
            }
        }
    });

    // Handle matches
    const matchdaySelect = document.querySelector("#matchday_select");
    const matchesContent = document.querySelector("#matches");

    if (matchdaySelect) {
        if (selected_league_id && matchdaySelect.value) {
            loadMatches(matchdaySelect.value)
        }

        matchdaySelect.addEventListener('change', function () {

            if (!selected_league_id) {
                alert("Please select a league first!")
                return;
            }

            loadMatches(this.value);

        });
    };
    
    function loadMatches(matchdayId) {
        console.log("Fetching matches for:", selected_league_id, matchdayId);
        fetch(`/football/matchday/${selected_league_id}/${matchdayId}`)
        .then(response => {
            return response.json();
        })
        .then(data => {
            // Clear previous results
            matchesContent.innerHTML = "";

            if (data.matches.length === 0) {
                matchesContent.innerHTML = "<p>No matches found for this matchday</p>"
                return
            }

            data.matches.forEach(item => {
                const match = `
                    <div class="match-item mb-3 p-2 border rounded">
                        <p class="mb-1">
                            <strong>${item.date}</strong> — ${item.status}
                        </p>
                        <p class="mb-0">
                            <img src="${item.home_logo || ''}" width="25"> ${item.home} 
                            <strong>${item.home_score ?? ''}</strong> 
                            vs 
                            <strong>${item.away_score ?? ''}</strong> 
                            ${item.away} <img src="${item.away_logo || ''}" width="25">
                        </p>
                        <p class="mb-0 text-warning small d-flex align-items-center justify-content-center">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-whistle me-2" viewBox="0 0 16 16">
                                <path d="M10 1a1 1 0 0 0-1 1v1H5a2 2 0 0 0-2 2v2.5l-.447.894A1 1 0 0 0 2 9v3a1 1 0 0 0 1 1h1v1a1 1 0 0 0 1 1h2.586a1 1 0 0 0 .707-.293l4.414-4.414a1 1 0 0 0 .293-.707V2a1 1 0 0 0-1-1H10zm-1 2v8.586L6.414 14H5v-1h1a1 1 0 0 0 1-1V3h3z"/>
                            </svg>
                            Referee: <span class="fw-semibold">${item.referee}</span>
                        </p>
                    </div>
                `;
                matchesContent.insertAdjacentHTML("beforeend", match);
            });
        })
        .catch(error => {
            console.error("Error loading matches", error)
            matchesContent.innerHTML = "<p class='text-danger'>Failed to load matches.</p>";
        });
    }

    const teamsContent = document.querySelector('#teams');
    const teamRows = document.querySelector('#teams_rows')
    // Define loadMatches function
    function loadTeams(leagueId) {
        fetch(`/football/teams/${leagueId}`)
        .then(response => {
            return response.json();
        })
        .then(data => {
            // Clear previous content
            teamRows.innerHTML = '';

            if (data.teams.length === 0) {
                teamsContent.innerHTML = '<p>No teams found</p>'
            }

            data.teams.forEach(item => {
                const team = `
                    <div class="col-md-3 mb-4">
                        <a href="${item.team_id}" class="team_icon">
                            <div class="card border team-card text-center h-100">
                                <div class="card-body">
                                    <img src="${item.team_logo}" 
                                        class="mb-3" 
                                        alt="${item.team_name} logo" 
                                        style="width: 60px; height: 60px; object-fit: contain;">
                                    <h5 class="card-title fw-bold text-dark">${item.team_name}</h5>
                                    <p class="text-secondary mb-1">${item.team_league}</p>
                                    <p class="mb-1 text-dark"><strong>Coach:</strong> ${item.team_coach}</p>
                                    <p class="mb-0 text-muted"><small>${item.team_venue}</small></p>
                                </div>
                            </div>
                        </a>
                    </div> 
                `;
                teamRows.insertAdjacentHTML('beforeend', team);
            });
        })
        .catch(error => {
            console.error("Error is", error)
        });
    };

    // Handle top_scorers
    const scorersSection = document.querySelector("#scorers-section");

    function loadScorers(leagueId) {
        if (!scorersSection) return;
        scorersSection.style.display = "block";
        scorersSection.innerHTML = "<p>Loading top scorers...</p>";

        fetch(`/football/top_scorers/${leagueId}`)
            .then(res => res.json())
            .then(data => {
                scorersSection.innerHTML = "";
                if (!data.scorers || data.scorers.length === 0) {
                    scorersSection.innerHTML = '<p class="text-muted">No players found</p>';
                    return;
                }

                const grid = document.createElement("div");
                grid.className = "scorers-grid";
                scorersSection.appendChild(grid);

                const defaultPhoto = "/static/img/placeholder.png";

                data.scorers.forEach(item => {
                    const card = document.createElement("div");
                    card.className = "scorer-card";

                    card.innerHTML = `
                        <div class="player-photo">
                            <img src="${item.scorer_photo || defaultPhoto}" alt="${item.scorer_name}">
                        </div>
                        <div class="player-info">
                            <h5>${item.scorer_name || 'Unknown'} <small>(${item.scorer_position || 'N/A'})</small></h5>
                            <p class="team">
                                <img src="${item.scorer_team_photo || defaultPhoto}" alt="${item.scorer_team || 'Team'}">
                                ${item.scorer_team || 'Unknown Team'}
                            </p>
                            <div class="stats">
                                <span>⚽ Goals: ${item.scorer_goals ?? 0}</span>
                                <span>🎯 Assists: ${item.scorer_assists ?? 0}</span>
                                <span>⛔ Penalties: ${item.scorer_penalties ?? 0}</span>
                            </div>
                        </div>
                    `;

                    grid.appendChild(card);
                });
            })
            .catch(error => {
                console.error("Error loading top scorers:", error);
                scorersSection.innerHTML = "<p class='text-danger'>Failed to load top scorers.</p>";
            });
    }

    // Back and forward button
    const backBtn = document.querySelector('#back_button');
    const forwardBtn = document.querySelector('#forward_button')

    if (!matchdaySelect || !backBtn || !forwardBtn) return;

    function updateMatchdaySelect(offset) {
        let currentIndex = matchdaySelect.selectedIndex;
        let newIndex = currentIndex + offset

        // If out of bounds
        if (newIndex < 0) {
            newIndex = matchdaySelect.options.length - 1;
        } else if (newIndex >= matchdaySelect.options.length) {
            newIndex = 0;
        }

        matchdaySelect.selectedIndex = newIndex;

        const event = new Event("change");
        matchdaySelect.dispatchEvent(event);
    }

    backBtn.addEventListener('click', () => updateMatchdaySelect(-1));
    forwardBtn.addEventListener('click', () => updateMatchdaySelect(1));

    window.addEventListener("pageshow", (event) => {
        const savedLeague = localStorage.getItem("selectedLeague");
        const savedTab = localStorage.getItem("activeMainTab");
        const savedMatchday = localStorage.getItem("selectedMatchday");

        // Restore league selection
        if (savedLeague && leagueSelect) {
            leagueSelect.value = savedLeague;
            selected_league_id = savedLeague;
        }

        // Hide all sections first
        sections.forEach(sec => sec.style.display = "none");

        // Show the previously active section
        if (savedTab) {
            const sectionToShow = document.querySelector(`#${savedTab}-section`);
            if (sectionToShow) sectionToShow.style.display = "block";

            // Update nav links
            navLinks.forEach(link => {
                link.classList.toggle("active", link.dataset.section === savedTab);
            });

            // Load data for that tab
            switch (savedTab) {
                case "standings":
                    loadStandings(selected_league_id);
                    break;
                case "matches":
                    if (matchdaySelect && savedMatchday) {
                        matchdaySelect.value = savedMatchday;
                        loadMatches(savedMatchday);
                    }
                    break;
                case "teams":
                    loadTeams(selected_league_id);
                    break;
                case "top_scorers":
                    loadScorers(selected_league_id);
                    break;
            }
        }
    });

    // Save league and matchday whenever they change
    leagueSelect.addEventListener("change", function () {
        selected_league_id = this.value;
        localStorage.setItem("selectedLeague", selected_league_id);
    });

    if (matchdaySelect) {
        matchdaySelect.addEventListener("change", function () {
            localStorage.setItem("selectedMatchday", this.value);
        });
    }

    // Save active tab whenever user switches tabs
    navLinks.forEach(link => {
        link.addEventListener("click", function () {
            const section = this.dataset.section;
            localStorage.setItem("activeMainTab", section);
        });
    });

});
