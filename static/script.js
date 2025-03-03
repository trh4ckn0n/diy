// Ajout d'une pulsation dynamique au bouton de soumission
document.addEventListener("DOMContentLoaded", function() {
    const button = document.querySelector("input[type='submit']");
    const pulseElement = document.createElement("div");

    pulseElement.classList.add("pulse");
    document.body.appendChild(pulseElement);
    
    // Animation de pulsation
    pulseElement.style.position = "absolute";
    pulseElement.style.left = "50%";
    pulseElement.style.top = "50%";
    pulseElement.style.width = "50px";
    pulseElement.style.height = "50px";
    pulseElement.style.borderRadius = "50%";
    pulseElement.style.backgroundColor = "rgba(0, 255, 0, 0.2)";
    pulseElement.style.transform = "translate(-50%, -50%)";
    pulseElement.style.animation = "pulse 2s infinite";

    // Effet de survol sur les liens
    const links = document.querySelectorAll('a');
    links.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.color = '#FF5733'; // Orange survol
            this.style.borderBottom = '1px solid #FF5733';
        });

        link.addEventListener('mouseleave', function() {
            this.style.color = '#00FF00'; // Vert normal
            this.style.borderBottom = '1px solid #00FF00';
        });
    });

    // Animation de survol des boutons
    button.addEventListener('mouseover', function() {
        button.style.transform = "scale(1.1)";
        button.style.boxShadow = "0 0 20px #FF5733";
    });

    button.addEventListener('mouseout', function() {
        button.style.transform = "scale(1)";
        button.style.boxShadow = "0 0 5px #FF5733";
    });
});
