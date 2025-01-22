const canvas = document.getElementById("interactive-canvas");
const ctx = canvas.getContext("2d");
let circles = [];

const repos = {+}{repos_json}

// Track mouse position
const mouse = { x: 0, y: 0 };

// Resize canvas to maintain a 4:3 aspect ratio
function resizeCanvas() {
	const width = canvas.clientWidth;
	const height = (width * 3) / 4; // Maintain 4:3 ratio
	canvas.width = width;
	canvas.height = height;

	// Recalculate circles' positions relative to the new size
	generateCircles();
	drawCircles();
}

window.addEventListener("resize", resizeCanvas);
resizeCanvas();

// Generate pseudorandom positions for the circles within the 4:3 canvas
function generateCircles() {
	circles = repos.map((repo) => {
		// Position relative to canvas size
		const x = Math.random() * canvas.width * 0.9 + canvas.width * 0.05; // Avoid edges
		const y = Math.random() * canvas.height * 0.9 + canvas.height * 0.05; // Avoid edges
		const z = repo.lines_committed;
		const radius = 10 + z / 1000; // Adjust based on lines committed
		return {
			x,
			y,
			radius,
			defaultRadius: radius,
			repo,
			hovered: false,
		};
	});
}

generateCircles();

// Draw circles on the canvas
function drawCircles() {
	ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas

	circles.forEach((circle) => {
		// Calculate distance to cursor for interactivity
		const dx = mouse.x - circle.x;
		const dy = mouse.y - circle.y;
		const distance = Math.sqrt(dx * dx + dy * dy);

		// Grow circle as cursor approaches
		const maxDistance = 150; // Distance at which circle starts growing
		if (distance < maxDistance) {
			const scaleFactor = 1 + (1 - distance / maxDistance) * 1.5; // Smooth growth
			circle.radius = circle.defaultRadius * scaleFactor;
		} else {
			circle.radius = circle.defaultRadius;
		}

		// Draw the circle
		ctx.beginPath();
		ctx.arc(circle.x, circle.y, circle.radius, 0, Math.PI * 2);
		ctx.fillStyle = "#e0ba74"; // Orange color
		ctx.fill();

		// If hovered, draw halo
		if (circle.hovered) {
			ctx.beginPath();
			ctx.arc(circle.x, circle.y, circle.radius + 5, 0, Math.PI * 2);
			ctx.strokeStyle = "#fff"; // Halo color
			ctx.lineWidth = 2;
			ctx.stroke();
		}
	});
}


canvas.addEventListener("mousemove", (event) => {
	const rect = canvas.getBoundingClientRect();
	mouse.x = event.clientX - rect.left;
	mouse.y = event.clientY - rect.top;

	// Check for hover over circles
	circles.forEach((circle) => {
		const dx = mouse.x - circle.x;
		const dy = mouse.y - circle.y;
		const distance = Math.sqrt(dx * dx + dy * dy);
		if (distance < circle.radius) {
			circle.hovered = true;
			showTooltip(circle); // Show the tooltip
		} else {
			circle.hovered = false;
			hideTooltip(); // Hide the tooltip when not hovered
		}
	});

	drawCircles(); // Re-render the canvas with updated hover state
});

// Show tooltip function
const tooltip = document.createElement("div");
tooltip.className = "tooltip";
document.body.appendChild(tooltip);

function showTooltip(circle) {
	tooltip.style.display = "block";
	tooltip.style.left = `${circle.x + 20}px`; // Offset to the right of the circle
	tooltip.style.top = `${circle.y}px`;
	tooltip.innerHTML = `
        <h3>${circle.repo.title}</h3>
        <p>${circle.repo.description}</p>
        <p><small>Lines committed: ${circle.repo.lines_committed}</small></p>
        <p><small>Date: ${new Date(
			circle.repo.date
		).toLocaleDateString()}</small></p>
    `;
}

function hideTooltip() {
	tooltip.style.display = "none";
}

// Handle click events
canvas.addEventListener("click", (event) => {
	circles.forEach((circle) => {
		if (circle.hovered) {
			window.open(circle.repo.url, "_blank");
		}
	});
});

// Initial draw
drawCircles();
