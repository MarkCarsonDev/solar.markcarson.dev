document.addEventListener("DOMContentLoaded", function () {
	// The theme itself was applied in <head> before first paint; here we only
	// sync the icon and wire up interactions.
	showThemeIcon(currentTheme());
	initializeLightDarkSwitch();
	initializeKeypressNavigator();

	// Re-enable transitions now that the initial state is fully settled.
	requestAnimationFrame(function () {
		var s = document.getElementById("__no-trans");
		if (s) s.parentNode.removeChild(s);
	});
});

const THEME_COOKIE_DAYS = 7;
const TOGGLE_COOLDOWN_MS = 500;

const SUN_SVG = `
	<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
		<circle cx="12" cy="12" r="5" stroke="var(--icon-color)" stroke-width="1.5"></circle>
		<path d="M12 2V4" stroke="var(--icon-color)" stroke-width="1.5" stroke-linecap="round"></path>
		<path d="M12 20V22" stroke="var(--icon-color)" stroke-width="1.5" stroke-linecap="round"></path>
		<path d="M4 12L2 12" stroke="var(--icon-color)" stroke-width="1.5" stroke-linecap="round"></path>
		<path d="M22 12L20 12" stroke="var(--icon-color)" stroke-width="1.5" stroke-linecap="round"></path>
		<path d="M19.7778 4.22266L17.5558 6.25424" stroke="var(--icon-color)" stroke-width="1.5" stroke-linecap="round"></path>
		<path d="M4.22217 4.22266L6.44418 6.25424" stroke="var(--icon-color)" stroke-width="1.5" stroke-linecap="round"></path>
		<path d="M6.44434 17.5557L4.22211 19.7779" stroke="var(--icon-color)" stroke-width="1.5" stroke-linecap="round"></path>
		<path d="M19.7778 19.7773L17.5558 17.5551" stroke="var(--icon-color)" stroke-width="1.5" stroke-linecap="round"></path>
	</svg>`;

const MOON_SVG = `
	<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
		<path fill-rule="evenodd" clip-rule="evenodd" d="M11.203 6.02337C7.59276 6.99074 5.45107 10.6948 6.41557 14.2943C7.38006 17.8938 11.0868 20.0307 14.6971 19.0634C16.1096 18.6849 17.2975 17.8877 18.1626 16.8409C15.1968 17.3646 12.2709 15.546 11.4775 12.585C10.7644 9.92365 12.0047 7.20008 14.3182 5.92871C13.3186 5.72294 12.2569 5.74098 11.203 6.02337ZM4.96668 14.6825C3.78704 10.2801 6.40707 5.75553 10.8148 4.57448C12.968 3.99752 15.1519 4.3254 16.9581 5.32413L16.6781 6.72587C16.4602 6.75011 16.241 6.79108 16.0218 6.8498C13.6871 7.47537 12.303 9.8703 12.9264 12.1968C13.5497 14.5233 15.9459 15.9053 18.2806 15.2797C18.7257 15.1604 19.1351 14.9774 19.5024 14.7435L20.5991 15.6609C19.6542 17.9633 17.6796 19.8171 15.0853 20.5123C10.6776 21.6933 6.14631 19.085 4.96668 14.6825Z" fill="var(--icon-color)"></path>
	</svg>`;

const ARROW_KEYCAPS = { arrowleft: "←", arrowright: "→", arrowup: "↑", arrowdown: "↓" };

function currentTheme() {
	return document.documentElement.getAttribute("data-theme");
}

function initializeLightDarkSwitch() {
	const themeToggle = document.getElementsByClassName("theme-switch")[0];
	let coolingDown = false;

	themeToggle.addEventListener("click", function () {
		if (coolingDown) return;
		coolingDown = true;
		themeToggle.classList.add("debounce-active");
		setTimeout(() => {
			coolingDown = false;
			themeToggle.classList.remove("debounce-active");
		}, TOGGLE_COOLDOWN_MS);

		toggleTheme();
	});
}

function toggleTheme() {
	const newTheme = currentTheme() === "light" ? "dark" : "light";
	document.documentElement.setAttribute("data-theme", newTheme);
	showThemeIcon(newTheme);
	setCookie("theme", newTheme, THEME_COOKIE_DAYS);
}

/** Shows the current theme's icon; the button reads "Dark mode, pressed" in the dark theme. */
function showThemeIcon(theme) {
	document.getElementById("theme-icon").innerHTML = theme === "light" ? SUN_SVG : MOON_SVG;
	document.getElementById("kpD").setAttribute("aria-pressed", String(theme === "dark"));
}

// --- Cookie helper ---

function setCookie(name, value, days) {
	const expires = new Date(Date.now() + days * 24 * 60 * 60 * 1000).toUTCString();
	document.cookie = name + "=" + (value || "") + "; expires=" + expires + "; path=/";
}

// --- Keyboard shortcuts ---

/**
 * Every .keypress element with an id like "kpB" is activated by that key
 * ("b"); ids like "kpARROWLEFT" map to arrow keys. A keycap label is added
 * when the markup doesn't already have one.
 */
function initializeKeypressNavigator() {
	document.querySelectorAll(".keypress").forEach(function (item) {
		if (!item.id || !item.id.startsWith("kp")) return;
		const key = item.id.slice(2).toLowerCase();

		if (!item.querySelector(".keycap")) addKeycap(item, key);

		document.addEventListener("keydown", function (event) {
			if (!isShortcutFor(event, key)) return;
			setPressed(item, true);
			item.click();
		});
		document.addEventListener("keyup", function (event) {
			if (event.key.toLowerCase() === key) setPressed(item, false);
		});
	});
}

function addKeycap(item, key) {
	const keycap = document.createElement("span");
	keycap.className = "keycap";
	keycap.textContent = ARROW_KEYCAPS[key] || key.toUpperCase();
	if (item.classList.contains("keypress-reverse")) {
		item.insertBefore(keycap, item.firstChild);
	} else {
		item.appendChild(keycap);
	}
}

/** A bare key press, not a browser shortcut (Ctrl+D, Cmd+1, ...) or typing into a field. */
function isShortcutFor(event, key) {
	if (event.ctrlKey || event.metaKey || event.altKey) return false;
	if (event.target.closest && event.target.closest("input, textarea, select, [contenteditable]")) return false;
	return event.key.toLowerCase() === key;
}

/** Show the press on the visible keycap, or on the item itself when its keycap is hidden. */
function setPressed(item, pressed) {
	const keycap = item.querySelector(".keycap");
	const target = keycap && keycap.offsetParent !== null ? keycap : item;
	target.classList.toggle("depressed", pressed);
}
