/**
 * Static replacement for the WordPress form handlers (contact, newsletter, libro de reclamaciones).
 * There is no PHP backend: set an endpoint (e.g. a Formspree URL) in src/site.json -> forms.*.
 * While an endpoint is empty, submitting only shows a notice.
 */
(function () {
	'use strict';
	var cfg = window.SITE_FORMS || {};

	function endpointFor(form) {
		if (form.closest('.claim-wong')) return cfg.libro;
		if (form.closest('footer') || form.matches('.jkit-subscribe-form, [class*="subscribe"]')) return cfg.newsletter;
		return cfg.contact;
	}

	function notice(form, text, ok) {
		var el = form.querySelector('.static-form-notice');
		if (!el) {
			el = document.createElement('p');
			el.className = 'static-form-notice';
			form.appendChild(el);
		}
		el.textContent = text;
		el.style.color = ok ? '#006943' : '#b00020';
	}

	document.addEventListener('submit', function (e) {
		var form = e.target;
		if (!(form instanceof HTMLFormElement)) return;
		e.preventDefault();
		var url = endpointFor(form);
		if (!url) {
			notice(form, 'El formulario aún no está conectado. Escríbenos a comercial@corporacionyanayacu.com.', false);
			return;
		}
		fetch(url, {method: 'POST', body: new FormData(form), headers: {Accept: 'application/json'}})
			.then(function (r) { if (!r.ok) throw new Error(r.status); notice(form, 'Mensaje enviado. ¡Gracias!', true); form.reset(); })
			.catch(function () { notice(form, 'No se pudo enviar. Inténtalo nuevamente.', false); });
	});
})();
