/**
 * Libro de Reclamaciones page behaviour (no backend, vanilla JS).
 * - Fills "Fecha de reclamación / queja" with today's date.
 * - Provincia / Distrito were filled through WordPress admin-ajax. Without a backend the selects are empty,
 *   so they are swapped for text inputs (same id / name / required).
 * - Shows the guardian block only when "¿Eres menor de edad?" is "Sí" and makes its fields required.
 * - Flags invalid fields visually after the first failed submit.
 * Submission itself is handled by forms.js (src/site.json -> forms.libro).
 */
(function () {
	'use strict';
	var form = document.getElementById('rt_form_libro');
	if (!form) return;

	function pad(n) { return (n < 10 ? '0' : '') + n; }
	function setToday() {
		var el = document.getElementById('fch_reclamo');
		if (!el) return;
		var d = new Date();
		el.value = pad(d.getDate()) + '/' + pad(d.getMonth() + 1) + '/' + d.getFullYear();
	}
	setToday();
	form.addEventListener('reset', function () { setTimeout(function () { setToday(); sync(); }, 0); });

	[['prov', 'Provincia'], ['dist', 'Distrito']].forEach(function (pair) {
		var sel = document.getElementById(pair[0]);
		if (!sel || sel.tagName !== 'SELECT' || sel.options.length > 1) return;
		var input = document.createElement('input');
		input.type = 'text';
		input.id = sel.id;
		input.name = sel.name;
		input.className = sel.className;
		input.required = sel.required;
		input.placeholder = pair[1];
		sel.parentNode.replaceChild(input, sel);
	});

	var tutor = document.getElementById('tutor_block');
	function sync() {
		if (!tutor) return;
		var checked = form.querySelector('input[name="flag_menor"]:checked');
		var minor = !!checked && checked.value === '1';
		tutor.hidden = !minor;
		tutor.querySelectorAll('[data-tutor-required]').forEach(function (el) { el.required = minor; });
	}
	form.querySelectorAll('input[name="flag_menor"]').forEach(function (r) { r.addEventListener('change', sync); });
	sync();

	// "invalid" does not bubble, so listen in the capture phase.
	form.addEventListener('invalid', function () { form.classList.add('was-validated'); }, true);
})();
