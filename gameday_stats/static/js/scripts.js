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
                        <td><img src='${item.logo}' width="25"> ${item.name}</td>
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
    document.querySelectorAll("#select_content .nav-link").forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const clicked = e.currentTarget;

            console.log("Clicked:", clicked.textContent);
            console.log("Classes:", clicked.classList);

            if (!selected_league_id) {
                alert("Please select a league first!");
                return;
            }

            // Update active tab
            document.querySelectorAll("#select_content .nav-link")
                .forEach(nav => nav.classList.remove("active"));
            clicked.classList.add("active");

            console.log("Classes after :", clicked.classList);

            // Hide all sections
            document.querySelectorAll(".section")
                .forEach(section => section.style.display = "none");

            // Show selected section
            const sectionToShow = document.querySelector(`#${this.dataset.section}-section`);
            if (sectionToShow) sectionToShow.style.display = "block";


            // Load standings if “table” tab
            if (this.dataset.section === "standings") {
                loadStandings(selected_league_id);
            }
        });
    });

    // Handle league selection
    leagueSelect.addEventListener("change", function () {
        selected_league_id = this.value;
        console.log("Selected League:", selected_league_id);

        const standingsSection = document.querySelector("#standings-section");

        // If currently viewing standings, reload table
        if (standingsSection && standingsSection.style.display !== "none") {
            loadStandings(selected_league_id);
        }
    });
    
});
