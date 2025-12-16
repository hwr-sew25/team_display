let warned20 = false;
let warned5 = false;

function showBatteryPopup(level) {
    const popup = document.createElement("div");
    popup.className = "battery-popup";

    if (level <= 5) {
        popup.classList.add("critical");
        popup.innerHTML = `
            <h2>⚠ Kritischer Akkustand</h2>
            <p>Akku bei ${level}%</p>
            <p>Bitte sofort laden.</p>
        `;
    } else {
        popup.innerHTML = `
            <h2>⚠ Niedriger Akkustand</h2>
            <p>Akku bei ${level}%</p>
        `;
    }

    document.body.appendChild(popup);

    setTimeout(() => {
        popup.remove();
    }, 8000);
}

if ('getBattery' in navigator) {
    navigator.getBattery().then(function (battery) {

        function checkBattery() {
            const level = Math.round(battery.level * 100);

            if (level <= 20 && !warned20) {
                showBatteryPopup(level);
                warned20 = true;
            }

            if (level <= 5 && !warned5) {
                showBatteryPopup(level);
                warned5 = true;
            }
        }

        checkBattery();

        battery.addEventListener("levelchange", checkBattery);
    });
}
