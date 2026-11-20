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
			el.setAttribute('role', 'status');
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
		if (!url && form.getAttribute('data-whatsapp')) {
			// No backend: hand the message over to WhatsApp (number set in site.json -> phone_wa).
			var data = new FormData(form), lines = ['Hola, quisiera más información sobre sus servicios.'];
			[['nombre', 'Nombre'], ['telefono', 'Teléfono'], ['correo', 'Correo'], ['servicio', 'Servicio'], ['mensaje', 'Mensaje']].forEach(function (f) {
				var v = (data.get(f[0]) || '').toString().trim();
				if (v) lines.push(f[1] + ': ' + v);
			});
			window.open('https://wa.me/' + form.getAttribute('data-whatsapp') + '?text=' + encodeURIComponent(lines.join('\n')), '_blank', 'noopener');
			notice(form, 'Te llevamos a WhatsApp para enviar tu mensaje.', true);
			return;
		}
		if (!url) {
			var mail = form.getAttribute('data-fallback-email') || 'comercial@corporacionyanayacu.com';
			notice(form, 'El formulario aún no está conectado. Escríbenos a ' + mail + '.', false);
			return;
		}
		fetch(url, {method: 'POST', body: new FormData(form), headers: {Accept: 'application/json'}})
			.then(function (r) { if (!r.ok) throw new Error(r.status); notice(form, 'Mensaje enviado. ¡Gracias!', true); form.reset(); })
			.catch(function () { notice(form, 'No se pudo enviar. Inténtalo nuevamente.', false); });
	});
})();
