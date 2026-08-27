function filterApplications() {
    const searchInput = document.getElementById("searchInput");
    const statusFilter = document.getElementById("statusFilter");
    const table = document.getElementById("applicationsTable");

    if (!searchInput || !statusFilter || !table) {
        return;
    }

    const searchText = searchInput.value.toLowerCase();
    const selectedStatus = statusFilter.value.toLowerCase();

    const rows = table.querySelectorAll("tbody tr");

    rows.forEach(row => {
        const cells = row.querySelectorAll("td");

        if (cells.length < 5) {
            return;
        }

        const company = cells[0].textContent.toLowerCase();
        const position = cells[1].textContent.toLowerCase();
        const status = cells[3].textContent.toLowerCase();

        const matchesSearch =
            company.includes(searchText) ||
            position.includes(searchText);

        const matchesStatus =
            selectedStatus === "" ||
            status.includes(selectedStatus);

        row.style.display =
            matchesSearch && matchesStatus ? "" : "none";
    });
}
// ========================================
// THEME SETTINGS
// ========================================

document.addEventListener("DOMContentLoaded", function () {

    const themeSelect = document.getElementById("themeSelect");
    const colorSelect = document.getElementById("colorSelect");

    // ---------- Load saved appearance ----------

    const savedTheme =
        localStorage.getItem("careertrackTheme");

    if (savedTheme === "dark-mode") {

        document.body.classList.add("dark-mode");

        if (themeSelect) {
            themeSelect.value = "dark";
        }

    } else {

        document.body.classList.remove("dark-mode");

        if (themeSelect) {
            themeSelect.value = "light";
        }
    }


    // ---------- Load saved color ----------

    const savedColor =
        localStorage.getItem("careertrackColor") || "blue";

    document.body.classList.remove(
        "theme-blue",
        "theme-purple",
        "theme-green"
    );

    document.body.classList.add(
        "theme-" + savedColor
    );

    if (colorSelect) {
        colorSelect.value = savedColor;
    }


    // ---------- Change appearance ----------

    if (themeSelect) {

        themeSelect.addEventListener("change", function () {

            if (this.value === "dark") {

                document.body.classList.add("dark-mode");

                localStorage.setItem(
                    "careertrackTheme",
                    "dark-mode"
                );

            } else {

                document.body.classList.remove("dark-mode");

                localStorage.setItem(
                    "careertrackTheme",
                    "light-mode"
                );
            }

        });
    }


    // ---------- Change theme color ----------

    if (colorSelect) {

        colorSelect.addEventListener("change", function () {

            document.body.classList.remove(
                "theme-blue",
                "theme-purple",
                "theme-green"
            );

            document.body.classList.add(
                "theme-" + this.value
            );

            localStorage.setItem(
                "careertrackColor",
                this.value
            );

            console.log(
                "Theme changed to:",
                this.value
            );
            

        });
    }
    

});