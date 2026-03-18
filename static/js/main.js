
/* ================= SELECT STYLE NAVBAR ================= */

// open / close dropdown
function toggleSelect(id, event) {

    const dropdown = document.getElementById(id);
    const button = event.currentTarget;

    // close others
    document.querySelectorAll(".select-options").forEach(el => {
        if (el !== dropdown) {
            el.classList.remove("show");
        }
    });

    // position fix
    const rect = button.getBoundingClientRect();
    dropdown.style.top = rect.bottom + "px";
    dropdown.style.left = rect.left + "px";

    dropdown.classList.toggle("show");
}


// option select
function selectOption(event, type, text) {

    event.stopPropagation();

    loadContent(type);

    // text change
    const parent = document.querySelector(`[onclick*="${type}"]`).closest(".nav-select");
    if (parent) {
        parent.querySelector(".select-box").innerText = text + " ▾";
    }

    // close
    document.querySelectorAll(".select-options").forEach(el => {
        el.classList.remove("show");
    });
}


// outside click → close
document.addEventListener("click", function(e) {
    if (!e.target.closest(".nav-select")) {
        document.querySelectorAll(".select-options").forEach(el => {
            el.classList.remove("show");
        });
    }
});


/* ================= LOAD CONTENT ================= */

function loadContent(type) {

    let c = document.getElementById("content-area");
    if (!c) return;

    // ===== STUDENT =====
    if (type === "exam_item") {
        c.innerHTML = "<h3>Exam - Item</h3>";
    }
    else if (type === "exam_card") {
        c.innerHTML = "<h3>Exam - Card</h3>";
    }
    else if (type === "exam_term") {
        c.innerHTML = "<h3>Exam - Term</h3>";
    }

    else if (type === "result_history") {
        c.innerHTML = "<h3>Result History</h3>";
    }
    else if (type === "result_item") {
        c.innerHTML = "<h3>Item Result</h3>";
    }
    else if (type === "result_term") {
        c.innerHTML = "<h3>Term Result</h3>";
    }

    // ===== INTERN =====
    else if (type === "duty_department") {
        c.innerHTML = "<h3>Department Duty</h3>";
    }
    else if (type === "duty_ward") {
        c.innerHTML = "<h3>Ward Duty</h3>";
    }
    else if (type === "duty_ot") {
        c.innerHTML = "<h3>OT Duty</h3>";
    }

    // ===== WARD =====
    else if (type === "attendance_ward") {
        c.innerHTML = "<h3>Ward Attendance</h3>";
    }
    else if (type === "attendance_ot") {
        c.innerHTML = "<h3>OT Attendance</h3>";
    }

    // ===== COMMON =====
    else {
        c.innerHTML = `<h3>${type}</h3>`;
    }
}