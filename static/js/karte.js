
console.log("setArrow loaded", direction);

function setArrow(direction) {
    const vert = document.getElementById("arrow-vertical");
    const horiz = document.getElementById("arrow-horizontal");
    const tip = document.getElementById("arrow-tip");
    const dot = document.getElementById("arrow-dot");

    if (direction === "right") {
        
        dot.setAttribute("cx", 80);
        dot.setAttribute("cy", 120);

        // Vertikale Linie
        vert.setAttribute("x1", 80);
        vert.setAttribute("y1", 120);
        vert.setAttribute("x2", 80);
        vert.setAttribute("y2", 20);

        // Horizontale Linie
        horiz.setAttribute("x1", 80);
        horiz.setAttribute("y1", 20);
        horiz.setAttribute("x2", 140);
        horiz.setAttribute("y2", 20);

        tip.setAttribute("d", "M140 15 L150 20 L140 25 Z");
    }


    if (direction === "left") {

        dot.setAttribute("cx", 80);
        dot.setAttribute("cy", 120);

        vert.setAttribute("x1", 80);
        vert.setAttribute("y1", 120);
        vert.setAttribute("x2", 80);
        vert.setAttribute("y2", 20);

        horiz.setAttribute("x1", 80);
        horiz.setAttribute("y1", 20);
        horiz.setAttribute("x2", 20);
        horiz.setAttribute("y2", 20);

        tip.setAttribute("d", "M20 15 L10 20 L20 25 Z");
    }

    if (direction === "down") {

        dot.setAttribute("cx", 80);
        dot.setAttribute("cy", 120);
    
        vert.setAttribute("x1", 80);
        vert.setAttribute("y1", 120);
        vert.setAttribute("x2", 80);
        vert.setAttribute("y2", 200);
    
        // Keine horizontale Linie
        horiz.setAttribute("x1", 80);
        horiz.setAttribute("y1", 120);
        horiz.setAttribute("x2", 80);
        horiz.setAttribute("y2", 120);
    
        tip.setAttribute("d", "M73 200 L87 200 L80 210 Z");

    }
    
    
}