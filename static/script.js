const toggle = document.getElementById("themeToggle");
const body = document.body;

// Load saved theme
if (localStorage.getItem("theme") === "dark") {
    body.classList.add("dark");
    toggle.checked = true;
}

// Toggle theme
toggle.addEventListener("change", () => {
    body.classList.toggle("dark");
    localStorage.setItem("theme", body.classList.contains("dark") ? "dark" : "light");
});

// Auto-scroll to result
window.addEventListener("load", () => {
    const result = document.querySelector(".result-box");
    if (result) {
        result.scrollIntoView({ behavior: "smooth" });
    }
});
