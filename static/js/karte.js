function setArrow(direction) {
    const arrow = document.getElementById("arrow");
    arrow.classList.remove("right", "left", "down");
    arrow.classList.add(direction);
}

