/* ================= DROPDOWN ================= */

function toggleSelect(event, id) {
    event.stopPropagation();

    const dropdown = document.getElementById(id);

    // Close other dropdowns
    document.querySelectorAll(".select-options").forEach(el => {
        if (el.id !== id) {
            el.classList.remove("show");
        }
    });

    // Toggle current dropdown
    dropdown.classList.toggle("show");
}


// /* ================= SUBMENU ================= */

// function toggleSubmenu(id) {
//     let menu = document.getElementById(id);

//     if (menu.style.display === "block") {
//         menu.style.display = "none";
//     } else {
//         menu.style.display = "block";
//     }
// }


/* ================= SELECT OPTION ================= */

function selectOption(event, type, text) {
    event.stopPropagation();

    loadContent(type);

    // Close dropdown after click
    document.querySelectorAll(".select-options").forEach(el => {
        el.classList.remove("show");
    });
}


/* ================= OUTSIDE CLICK CLOSE ================= */

document.addEventListener("click", function (e) {
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

    // ===== STUDENT (EXAM) =====
    if (type === "exam_item") {
        c.innerHTML = "<h3>Exam - Item</h3>";
    }
    else if (type === "exam_card") {
        c.innerHTML = "<h3>Exam - Card</h3>";
    }
    else if (type === "exam_term") {
        c.innerHTML = "<h3>Exam - Term</h3>";
    }

    // ===== STUDENT (RESULT) =====
    else if (type === "result_item") {
        c.innerHTML = "<h3>Item Result</h3>";
    }
    else if (type === "result_card") {
        c.innerHTML = "<h3>Card Result</h3>";
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

    // ===== DEFAULT =====
    else {
        c.innerHTML = `<h3>${type}</h3>`;
    }
}