document.addEventListener("DOMContentLoaded", function() {
    const navLinks = document.querySelectorAll("#team_contentnav .nav-link");
    const teamSections = document.querySelectorAll(".team_section");

    // Hide all sections, show matches by default
    teamSections.forEach(section => section.classList.remove("active"));
    const defaultSection = document.querySelector("#matches_team-section");
    if (defaultSection) defaultSection.classList.add("active");

    // Handle nav clicks
    navLinks.forEach(link => {
        link.addEventListener("click", function(e) {
            e.preventDefault();

            // Update active nav link
            navLinks.forEach(nav => nav.classList.remove("active"));
            this.classList.add("active");

            // Hide all sections
            teamSections.forEach(section => section.classList.remove("active"));

            // Show the clicked one
            const sectionId = this.dataset.teamsection;
            const sectionToShow = document.querySelector(`#${sectionId}-section`);
            if (sectionToShow) {
                sectionToShow.classList.add("active");
            }
        });
    });
});