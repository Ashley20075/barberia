/*
 * Mejoras de usabilidad compartidas por todo el sitio.
 *
 * 1) Los mensajes de éxito / información (los banners verdes/azules que
 *    aparecen arriba de cada página, ej. "Cita agendada exitosamente")
 *    se cierran solos después de unos segundos, para que no se queden
 *    estorbando en pantalla si el usuario no les da clic.
 *
 * 2) Los mensajes de ERROR se dejan como están: el usuario debe cerrarlos
 *    manualmente, porque es importante que los lea con calma.
 *
 * 3) Los modales de formulario (agregar/editar cita, producto, etc.) NO
 *    se cierran solos a propósito: forzar el cierre de un formulario a
 *    medio llenar sería peor usabilidad, no mejor.
 */

document.addEventListener('DOMContentLoaded', function () {
    var SEGUNDOS_ANTES_DE_CERRAR = 5000;

    document
        .querySelectorAll('.alert-success, .alert-info')
        .forEach(function (alerta) {
            setTimeout(function () {
                if (window.bootstrap && window.bootstrap.Alert) {
                    var instancia = window.bootstrap.Alert.getOrCreateInstance(alerta);
                    instancia.close();
                } else {
                    alerta.remove();
                }
            }, SEGUNDOS_ANTES_DE_CERRAR);
        });
});

/* =====================================================
   TEMA
   Se ejecuta inmediatamente para evitar parpadeos.
===================================================== */

(function () {

    var temaGuardado = localStorage.getItem('tema');

    if (temaGuardado === 'light') {
        document.documentElement.setAttribute(
            'data-theme',
            'light'
        );
    } else {
        document.documentElement.removeAttribute(
            'data-theme'
        );
    }

})();

/* =====================================================
   FUNCIONES CUANDO CARGA LA PÁGINA
===================================================== */

document.addEventListener('DOMContentLoaded', function () {

    /* =================================================
       MENSAJES AUTOMÁTICOS
    ================================================= */

    var SEGUNDOS_ANTES_DE_CERRAR = 5000;

    document
        .querySelectorAll('.alert-success, .alert-info')
        .forEach(function (alerta) {

            setTimeout(function () {

                if (
                    window.bootstrap &&
                    window.bootstrap.Alert
                ) {

                    var instancia =
                        window.bootstrap.Alert
                            .getOrCreateInstance(alerta);

                    instancia.close();

                } else {

                    alerta.remove();

                }

            }, SEGUNDOS_ANTES_DE_CERRAR);

        });

    /* =================================================
       BOTÓN DE TEMA
    ================================================= */

    var botonTema =
        document.getElementById('themeToggle');

    if (!botonTema) {
        return;
    }

    var icono =
        botonTema.querySelector('i');

    /* Actualizar icono */
    function actualizarIcono() {

        var temaActual =
            document.documentElement
                .getAttribute('data-theme');

        if (!icono) {
            return;
        }

        if (temaActual === 'light') {

            icono.className =
                'bi bi-sun-fill';

            botonTema.setAttribute(
                'title',
                'Cambiar a tema oscuro'
            );

            botonTema.setAttribute(
                'aria-label',
                'Cambiar a tema oscuro'
            );

        } else {

            icono.className =
                'bi bi-moon-fill';

            botonTema.setAttribute(
                'title',
                'Cambiar a tema claro'
            );

            botonTema.setAttribute(
                'aria-label',
                'Cambiar a tema claro'
            );
        }

    }

    actualizarIcono();

    /* Cambiar tema */
    botonTema.addEventListener(
        'click',
        function () {

            var temaActual =
                document.documentElement
                    .getAttribute('data-theme');

            if (temaActual === 'light') {

                /* CLARO → OSCURO */

                document.documentElement
                    .removeAttribute('data-theme');

                localStorage.setItem(
                    'tema',
                    'dark'
                );

            } else {

                /* OSCURO → CLARO */

                document.documentElement
                    .setAttribute(
                        'data-theme',
                        'light'
                    );

                localStorage.setItem(
                    'tema',
                    'light'
                );

            }

            actualizarIcono();

        }
    );

});

/* =====================================================
   USABILIDAD: NO PERDER EL LUGAR NI LO ESCRITO
   -----------------------------------------------------
   Problema que resuelve:

   1) Cada accion de los paneles (confirmar cita, editar
      producto, registrar movimiento...) termina en un
      redirect al mismo panel. El navegador recarga la
      pagina y te deja arriba del todo, asi hubieras
      estado trabajando al final de la tabla.

   2) Si la accion falla, el formulario del modal se
      vuelve a dibujar vacio y hay que escribirlo todo
      otra vez.

   Aqui se guarda, antes de salir de la pagina, la
   posicion del scroll y lo que habia escrito en el
   formulario enviado. Al volver, se restauran.
===================================================== */

(function () {

    var CLAVE_SCROLL = 'barberia_scroll';
    var CLAVE_FORM = 'barberia_formulario';

    function rutaActual() {
        return window.location.pathname + window.location.search;
    }

    /* Para el scroll usamos solo el path, sin el "?...": paginar,
       filtrar o cambiar de pestaña dentro de la misma pantalla
       cambia el query string A PROPOSITO (?pagina=2, ?estado=...).
       Comparar con el query incluido hacia que esos casos NUNCA
       coincidieran con la pagina guardada, y el scroll se perdia
       cada vez que se usaba la paginacion. */
    function rutaBaseActual() {
        return window.location.pathname;
    }

    function guardar(clave, valor) {
        try {
            sessionStorage.setItem(clave, JSON.stringify(valor));
        } catch (e) { /* modo privado: se ignora */ }
    }

    function leerYBorrar(clave) {
        try {
            var crudo = sessionStorage.getItem(clave);
            sessionStorage.removeItem(clave);
            return crudo ? JSON.parse(crudo) : null;
        } catch (e) {
            return null;
        }
    }

    /* Identifica un formulario de forma estable entre recargas:
       primero por id, si no por action, y si no por su posicion. */
    function claveDelFormulario(formulario) {
        if (formulario.id) {
            return 'id:' + formulario.id;
        }
        var accion = formulario.getAttribute('action');
        if (accion) {
            return 'accion:' + accion;
        }
        var todos = Array.prototype.slice.call(
            document.querySelectorAll('form')
        );
        return 'indice:' + todos.indexOf(formulario);
    }

    function buscarFormulario(clave) {
        var partes = clave.split(':');
        var tipo = partes.shift();
        var valor = partes.join(':');

        if (tipo === 'id') {
            return document.getElementById(valor);
        }
        if (tipo === 'accion') {
            return document.querySelector(
                'form[action="' + valor + '"]'
            );
        }
        if (tipo === 'indice') {
            return document.querySelectorAll('form')[Number(valor)] || null;
        }
        return null;
    }

    /* =================================================
       1. GUARDAR SCROLL ANTES DE CAMBIAR DE PAGINA
       -------------------------------------------------
       "beforeunload" no es confiable en varios navegadores
       de celular (Safari de iOS, algunos de Android): a
       veces no se dispara para una navegacion comun, asi
       que el scroll nunca quedaba guardado ahi. Se guarda
       por TRES caminos distintos para que alguno funcione
       siempre:
         a) cada vez que el usuario scrollea (con un
            pequeno retraso, para no saturar);
         b) en "pagehide" y "beforeunload", los dos, por si
            alguno no aplica en el navegador de turno;
         c) justo antes de que el modal de confirmacion
            dispare la navegacion (ver mas abajo), que es
            el momento exacto en que sabemos que se va a
            cambiar de pagina.
    ================================================= */

    function guardarScrollActual() {
        var y = window.scrollY ||
                document.documentElement.scrollTop ||
                0;
        guardar(CLAVE_SCROLL, { ruta: rutaBaseActual(), y: y });
    }

    var guardadoPendiente = null;
    window.addEventListener('scroll', function () {
        if (guardadoPendiente) { clearTimeout(guardadoPendiente); }
        guardadoPendiente = setTimeout(guardarScrollActual, 150);
    }, { passive: true });

    window.addEventListener('beforeunload', guardarScrollActual);
    window.addEventListener('pagehide', guardarScrollActual);

    /* Se expone para que el modal de confirmacion (mas abajo en este
       mismo archivo) pueda llamarlo justo antes de navegar. */
    window._guardarScrollBarberia = guardarScrollActual;

    /* =================================================
       2. GUARDAR LO ESCRITO AL ENVIAR UN FORMULARIO
    ================================================= */

    document.addEventListener('submit', function (evento) {

        var formulario = evento.target;

        if (!formulario || formulario.tagName !== 'FORM') {
            return;
        }

        // Mismo momento seguro que en el modal de confirmacion: se
        // guarda el scroll apenas se sabe que la pagina va a cambiar.
        guardarScrollActual();

        var metodo = (formulario.getAttribute('method') || 'get')
            .toLowerCase();

        if (metodo !== 'post') {
            return;
        }

        var datos = {};

        Array.prototype.forEach.call(
            formulario.elements,
            function (campo) {

                if (!campo.name) { return; }
                if (campo.name === 'csrfmiddlewaretoken') { return; }

                /* Las contrasenas NUNCA se guardan. */
                if (campo.type === 'password') { return; }
                if (campo.type === 'file') { return; }

                if (campo.type === 'checkbox' || campo.type === 'radio') {
                    if (campo.checked) {
                        if (!datos[campo.name]) {
                            datos[campo.name] = [];
                        }
                        datos[campo.name].push(campo.value);
                    }
                    return;
                }

                if (campo.multiple && campo.tagName === 'SELECT') {
                    datos[campo.name] = Array.prototype.filter
                        .call(campo.options, function (o) { return o.selected; })
                        .map(function (o) { return o.value; });
                    return;
                }

                datos[campo.name] = campo.value;
            }
        );

        var modal = formulario.closest ?
            formulario.closest('.modal') : null;

        guardar(CLAVE_FORM, {
            ruta: rutaActual(),
            clave: claveDelFormulario(formulario),
            accion: formulario.getAttribute('action') || '',
            modal: modal ? modal.id : '',
            datos: datos
        });
    }, true);

    /* =================================================
       3. AL CARGAR: RESTAURAR
    ================================================= */

    document.addEventListener('DOMContentLoaded', function () {

        var scrollGuardado = leerYBorrar(CLAVE_SCROLL);
        var formGuardado = leerYBorrar(CLAVE_FORM);

        var hayError = document.querySelector(
            '.alert-danger, .alert-error, .alert-warning'
        );

        /* --- 3a. Si hubo error, se repuebla el formulario --- */

        var formularioRestaurado = null;

        if (hayError && formGuardado &&
            formGuardado.ruta === rutaActual()) {

            formularioRestaurado = buscarFormulario(formGuardado.clave);

            if (formularioRestaurado) {

                /* Algunos modales fijan el action por JS al abrirse;
                   se vuelve a poner el que se habia usado. */
                if (formGuardado.accion) {
                    formularioRestaurado.setAttribute(
                        'action',
                        formGuardado.accion
                    );
                }

                Array.prototype.forEach.call(
                    formularioRestaurado.elements,
                    function (campo) {

                        if (!campo.name) { return; }
                        if (campo.type === 'password') { return; }
                        if (campo.type === 'file') { return; }
                        if (!(campo.name in formGuardado.datos)) { return; }

                        var valor = formGuardado.datos[campo.name];

                        if (campo.type === 'checkbox' ||
                            campo.type === 'radio') {
                            campo.checked =
                                Array.isArray(valor) &&
                                valor.indexOf(campo.value) !== -1;
                            return;
                        }

                        if (campo.multiple && campo.tagName === 'SELECT') {
                            Array.prototype.forEach.call(
                                campo.options,
                                function (o) {
                                    o.selected =
                                        Array.isArray(valor) &&
                                        valor.indexOf(o.value) !== -1;
                                }
                            );
                            return;
                        }

                        campo.value = valor;
                    }
                );

                /* Si el formulario vivia en un modal, se reabre para
                   que el usuario vea sus datos intactos. */
                var modal = formGuardado.modal ?
                    document.getElementById(formGuardado.modal) : null;

                if (modal && window.bootstrap && window.bootstrap.Modal) {
                    window.bootstrap.Modal
                        .getOrCreateInstance(modal)
                        .show();
                }
            }
        }

        /* --- 3b. Volver donde estaba el usuario --- */

        function restaurarPosicion() {

            /* Si hay un error visible, tiene prioridad: se muestra
               el mensaje en vez de la posicion anterior. */
            if (hayError) {
                hayError.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center'
                });
                return;
            }

            if (scrollGuardado &&
                scrollGuardado.ruta === rutaBaseActual() &&
                scrollGuardado.y) {
                window.scrollTo(0, scrollGuardado.y);
            }
        }

        /* Se reintenta un par de veces porque tablas, iconos y
           fuentes cambian la altura de la pagina despues del load. */
        restaurarPosicion();
        setTimeout(restaurarPosicion, 60);
        window.addEventListener('load', function () {
            setTimeout(restaurarPosicion, 60);
        });
    });

})();

/* =====================================================
   MODAL DE CONFIRMACION PROPIO
   -----------------------------------------------------
   Antes cada accion destructiva (eliminar cita, barbero,
   producto, servicio, cancelar turno...) usaba confirm()
   del navegador: un cuadro gris del sistema operativo,
   con tipografia y botones que no tienen nada que ver
   con el resto del sitio, y que ademas no se puede
   traducir ni acomodar al tema claro/oscuro.

   Ahora cualquier enlace o boton con el atributo
   data-confirmar="pregunta" abre este modal, que sí usa
   los colores del panel. Con data-confirmar-peligro se
   pinta en rojo (acciones que borran algo).
===================================================== */

(function () {

    var PLANTILLA =
        '<div class="modal fade" id="modalConfirmar" tabindex="-1"' +
        '     aria-hidden="true" aria-labelledby="modalConfirmarTitulo">' +
        '  <div class="modal-dialog modal-dialog-centered">' +
        '    <div class="modal-content">' +
        '      <div class="modal-header">' +
        '        <h5 class="modal-title" id="modalConfirmarTitulo">Confirmar</h5>' +
        '        <button type="button" class="btn-close btn-close-white"' +
        '                data-bs-dismiss="modal" aria-label="Cerrar"></button>' +
        '      </div>' +
        '      <div class="modal-body text-center py-4">' +
        '        <i class="confirmar-icono bi bi-question-circle-fill"></i>' +
        '        <p class="fs-5 mb-0" id="modalConfirmarTexto"></p>' +
        '      </div>' +
        '      <div class="modal-footer">' +
        '        <button type="button" class="btn btn-secondary"' +
        '                data-bs-dismiss="modal">Cancelar</button>' +
        '        <button type="button" class="btn btn-danger"' +
        '                id="modalConfirmarAceptar">Confirmar</button>' +
        '      </div>' +
        '    </div>' +
        '  </div>' +
        '</div>';

    var modalEl = null;
    var instancia = null;
    var alAceptar = null;

    function asegurarModal() {
        if (modalEl) { return modalEl; }

        var contenedor = document.createElement('div');
        contenedor.innerHTML = PLANTILLA;
        modalEl = contenedor.firstChild;
        document.body.appendChild(modalEl);

        modalEl.querySelector('#modalConfirmarAceptar')
            .addEventListener('click', function () {
                var accion = alAceptar;
                alAceptar = null;
                if (instancia) { instancia.hide(); }
                if (typeof accion === 'function') { accion(); }
            });

        return modalEl;
    }

    function confirmar(opciones) {

        /* Si por lo que sea Bootstrap no cargo, se recurre al
           confirm() clasico para no dejar la accion muerta. */
        if (!window.bootstrap || !window.bootstrap.Modal) {
            if (window.confirm(opciones.texto)) {
                opciones.aceptar();
            }
            return;
        }

        var el = asegurarModal();

        el.classList.toggle('confirmar-peligro', !!opciones.peligro);

        el.querySelector('#modalConfirmarTitulo').textContent =
            opciones.titulo || (opciones.peligro ? 'Eliminar' : 'Confirmar');

        el.querySelector('#modalConfirmarTexto').textContent = opciones.texto;

        el.querySelector('.confirmar-icono').className =
            'confirmar-icono bi ' +
            (opciones.peligro ?
                'bi-exclamation-triangle-fill' :
                'bi-question-circle-fill');

        var botonAceptar = el.querySelector('#modalConfirmarAceptar');
        botonAceptar.className = opciones.peligro ?
            'btn btn-danger' : 'btn btn-modern';
        botonAceptar.textContent = opciones.etiqueta ||
            (opciones.peligro ? 'Sí, eliminar' : 'Confirmar');

        alAceptar = opciones.aceptar;

        instancia = window.bootstrap.Modal.getOrCreateInstance(el);
        instancia.show();
    }

    /* Se expone por si alguna pantalla necesita llamarlo a mano. */
    window.confirmarAccion = confirmar;

    /* Intercepta clics en cualquier elemento con data-confirmar. */
    document.addEventListener('click', function (evento) {

        var disparador = evento.target.closest ?
            evento.target.closest('[data-confirmar]') : null;

        if (!disparador) { return; }
        if (disparador.dataset.confirmado === '1') { return; }

        evento.preventDefault();
        evento.stopPropagation();

        confirmar({
            texto: disparador.getAttribute('data-confirmar'),
            titulo: disparador.getAttribute('data-confirmar-titulo') || '',
            etiqueta: disparador.getAttribute('data-confirmar-boton') || '',
            peligro: disparador.hasAttribute('data-confirmar-peligro'),
            aceptar: function () {
                /* Se marca como ya confirmado y se repite la accion
                   original (seguir el enlace o enviar el formulario). */
                disparador.dataset.confirmado = '1';

                // Guarda el scroll ANTES de navegar: es el momento mas
                // seguro posible, no depende de que el navegador
                // dispare beforeunload/pagehide a tiempo.
                if (window._guardarScrollBarberia) {
                    window._guardarScrollBarberia();
                }

                if (disparador.tagName === 'A' && disparador.href) {
                    window.location.href = disparador.href;
                    return;
                }

                if (disparador.form) {
                    disparador.form.submit();
                    return;
                }

                disparador.click();
                disparador.dataset.confirmado = '';
            }
        });

    }, true);

})();
/* =====================================================
   FONDOS DINÁMICOS — HOME Y LOGIN
   Cambia la fotografía suavemente sin recargar la página.
===================================================== */

(function () {
    function iniciarSlideshow(selector, intervalo) {
        var slides = Array.prototype.slice.call(
            document.querySelectorAll(selector)
        );

        if (slides.length <= 1) {
            return;
        }

        var indice = 0;

        setInterval(function () {
            slides[indice].classList.remove('active');
            indice = (indice + 1) % slides.length;
            slides[indice].classList.add('active');
        }, intervalo);
    }

    document.addEventListener('DOMContentLoaded', function () {
        iniciarSlideshow('.hero-bg-slide', 6500);
        iniciarSlideshow('.login-bg-slide', 6500);
    });
})();

/* Menú compacto para las barras de navegación. */
(function () {

    function armarNavbar(nav) {
        var fila = nav.querySelector('.d-flex.align-items-center.justify-content-between');
        if (!fila) { return; }

        var marca = fila.querySelector('.navbar-brand-custom');
        var acciones = fila.querySelector(':scope > div.d-flex.align-items-center');
        if (!marca || !acciones || acciones === marca) { return; }

        acciones.classList.add('nav-acciones');

        var boton = document.createElement('button');
        boton.type = 'button';
        boton.className = 'nav-hamburguesa';
        boton.setAttribute('aria-label', 'Abrir menú');
        boton.setAttribute('aria-expanded', 'false');
        boton.innerHTML = '<i class="bi bi-list"></i>';

        boton.addEventListener('click', function () {
            var abierto = acciones.classList.toggle('nav-acciones-abierto');
            boton.setAttribute('aria-expanded', abierto ? 'true' : 'false');
            boton.innerHTML = abierto ?
                '<i class="bi bi-x-lg"></i>' :
                '<i class="bi bi-list"></i>';
        });

        marca.insertAdjacentElement('afterend', boton);
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('nav.navbar-custom').forEach(armarNavbar);
    });

})();

/* Ajustes para los modales en móvil. */
document.addEventListener('DOMContentLoaded', function () {
    if (!window.bootstrap || !window.bootstrap.Modal) return;

    document.querySelectorAll('.modal').forEach(function (modal) {
        modal.addEventListener('shown.bs.modal', function () {
            var primerControl = modal.querySelector(
                'input:not([type="hidden"]):not([disabled]), select:not([disabled]), textarea:not([disabled]), button:not([disabled]), [tabindex="0"]'
            );
            if (primerControl && window.matchMedia('(max-width: 767.98px)').matches) {
                modal.setAttribute('data-modal-mobile-ready', 'true');
            }
        });
        modal.addEventListener('hidden.bs.modal', function () {
            if (!document.querySelector('.modal.show')) {
                document.body.classList.remove('modal-open');
                document.querySelectorAll('.modal-backdrop').forEach(function (backdrop) {
                    backdrop.remove();
                });
                document.body.style.removeProperty('padding-right');
                document.body.style.removeProperty('overflow');
            }
        });
    });
});

/* ===== Toasts: convierte los banners de messages de Django en toasts flotantes ===== */
(function () {
    function crearStack() {
        let s = document.getElementById('toastStack');
        if (!s) {
            s = document.createElement('div');
            s.id = 'toastStack'; s.className = 'toast-stack';
            s.setAttribute('aria-live', 'polite'); s.setAttribute('aria-atomic', 'false');
            document.body.appendChild(s);
        }
        return s;
    }
    function mostrarToast(texto, tipo) {
        const stack = crearStack();
        const t = document.createElement('div');
        t.className = 'app-toast ' + (tipo || 'info');
        t.setAttribute('role', (tipo === 'danger' || tipo === 'error') ? 'alert' : 'status');
        const body = document.createElement('div'); body.className = 'app-toast-body'; body.textContent = texto;
        const x = document.createElement('button'); x.type = 'button'; x.className = 'app-toast-close';
        x.setAttribute('aria-label', 'Cerrar'); x.innerHTML = '&times;';
        t.appendChild(body); t.appendChild(x); stack.appendChild(t);
        requestAnimationFrame(function () { t.classList.add('show'); });
        const dur = (tipo === 'danger' || tipo === 'error') ? 7000 : 4500;
        let resto = dur, inicio = Date.now(), timer;
        function cerrar() { clearTimeout(timer); t.classList.remove('show'); setTimeout(function () { t.remove(); }, 400); }
        function arrancar() { inicio = Date.now(); timer = setTimeout(cerrar, resto); }
        t.addEventListener('mouseenter', function () { clearTimeout(timer); resto -= Date.now() - inicio; });
        t.addEventListener('mouseleave', arrancar);
        x.addEventListener('click', cerrar);
        arrancar();
    }
    window.mostrarToast = mostrarToast;
    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.alert.alert-dismissible').forEach(function (a) {
            if (a.closest('.modal')) { return; }
            const m = a.className.match(/alert-(success|danger|warning|info|error)/);
            const copia = a.cloneNode(true);
            copia.querySelectorAll('.btn-close').forEach(function (b) { b.remove(); });
            const texto = copia.textContent.replace(/\s+/g, ' ').trim();
            if (texto) { mostrarToast(texto, m ? m[1] : 'info'); }
            a.remove();
        });
    });
})();

/* ===== Panel admin: secciones desplegables + menú de anclas fijo ===== */
(function () {
    document.addEventListener('DOMContentLoaded', function () {
        if (!document.body.classList.contains('tema-admin')) { return; }
        var CLAVE = 'admin_secciones_v1';
        var estado = {};
        try { estado = JSON.parse(localStorage.getItem(CLAVE) || '{}'); } catch (e) { estado = {}; }
        function guardar() { try { localStorage.setItem(CLAVE, JSON.stringify(estado)); } catch (e) {} }

        var tarjetas = Array.prototype.slice.call(document.querySelectorAll('.card-custom'))
            .filter(function (c) { return c.querySelector('.card-header-custom') && !c.closest('.modal'); });
        if (tarjetas.length < 2) { return; }

        var barra = document.createElement('nav');
        barra.className = 'admin-anclas'; barra.setAttribute('aria-label', 'Secciones del panel');
        var contenedor = document.querySelector('.container') || document.body;
        var primera = tarjetas[0];
        primera.parentNode.insertBefore(barra, primera);

        tarjetas.forEach(function (card, i) {
            var header = card.querySelector('.card-header-custom');
            var titulo = (header.querySelector('span') || header).textContent.replace(/\s+/g, ' ').trim().replace(/\d+$/, '').trim() || ('Sección ' + (i + 1));
            var clave = titulo;
            var id = card.id || ('seccion-' + (i + 1));
            card.id = id; card.style.scrollMarginTop = '130px';

            var envoltorio = header;
            while (envoltorio.parentElement && envoltorio.parentElement !== card) { envoltorio = envoltorio.parentElement; }
            var cuerpo = [];
            for (var n = envoltorio.nextElementSibling; n; n = n.nextElementSibling) { cuerpo.push(n); }

            var pill = document.createElement('span');
            pill.className = 'seccion-toggle';
            pill.innerHTML = '<span class="seccion-toggle-txt"></span><i class="bi bi-chevron-down"></i>';
            header.appendChild(pill);
            var pillTxt = pill.querySelector('.seccion-toggle-txt');
            header.style.cursor = 'pointer';
            header.setAttribute('role', 'button'); header.setAttribute('tabindex', '0');

            function aplicar(abierta) {
                cuerpo.forEach(function (el) { el.style.display = abierta ? '' : 'none'; });
                card.classList.toggle('seccion-cerrada', !abierta);
                header.setAttribute('aria-expanded', abierta ? 'true' : 'false');
                pillTxt.textContent = abierta ? 'Ocultar' : 'Mostrar';
                estado[clave] = abierta; guardar();
            }
            var abierta = (clave in estado) ? estado[clave] : (i === 0);
            aplicar(abierta);
            function alternar(ev) {
                if (ev.target.closest('a, button, input, select, form, .btn')) { return; }
                aplicar(card.classList.contains('seccion-cerrada'));
            }
            header.addEventListener('click', alternar);
            header.addEventListener('keydown', function (ev) { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); alternar(ev); } });

            var a = document.createElement('a');
            a.href = '#' + id; a.textContent = titulo;
            a.addEventListener('click', function () { aplicar(true); });
            barra.appendChild(a);
        });
    });
})();

/* ===== Asistente de citas por pasos (cliente) ===== */
(function () {
    document.addEventListener('DOMContentLoaded', function () {
        var cont = document.getElementById('formularioTurno');
        if (!cont) { return; }
        var form = cont.querySelector('form');
        if (!form) { return; }
        var bloques = Array.prototype.slice.call(form.querySelectorAll(':scope > .nc-bloque'));
        var resumen = form.querySelector(':scope > .nc-resumen');
        if (bloques.length < 4 || !resumen) { return; }

        // Orden pedido: servicio -> barbero -> fecha y hora -> adicionales -> confirmar
        var pasos = [bloques[0], bloques[2], bloques[3], bloques[1], resumen];
        var nombres = ['Servicio', 'Barbero', 'Fecha y hora', 'Adicionales', 'Confirmar'];
        pasos.slice(0, 4).forEach(function (p) { form.insertBefore(p, resumen); });

        var progreso = document.createElement('div');
        progreso.className = 'wiz-progreso';
        progreso.innerHTML = '<div class="wiz-barra"><div class="wiz-barra-llena"></div></div><ol class="wiz-pasos"></ol>';
        var lista = progreso.querySelector('.wiz-pasos');
        nombres.forEach(function (n, i) {
            var li = document.createElement('li'); li.textContent = (i + 1) + '. ' + n; lista.appendChild(li);
        });
        form.insertBefore(progreso, form.firstChild);

        var nav = document.createElement('div');
        nav.className = 'wiz-nav';
        nav.innerHTML = '<button type="button" class="btn btn-cancelar btn-secondary wiz-cancelar">Cancelar</button>' +
            '<span class="wiz-total" aria-live="polite"></span>' +
            '<button type="button" class="btn btn-volver btn-secondary wiz-atras"><i class="bi bi-arrow-left"></i> Atrás</button>' +
            '<button type="button" class="btn btn-primary-custom wiz-siguiente">Siguiente <i class="bi bi-arrow-right"></i></button>';
        form.appendChild(nav);
        var bAtras = nav.querySelector('.wiz-atras'), bSig = nav.querySelector('.wiz-siguiente');
        var totalEl = nav.querySelector('.wiz-total');
        var actual = 0;

        function mostrar(i) {
            actual = Math.max(0, Math.min(pasos.length - 1, i));
            pasos.forEach(function (p, k) { p.style.display = (k === actual) ? '' : 'none'; });
            progreso.querySelector('.wiz-barra-llena').style.width = ((actual + 1) / pasos.length * 100) + '%';
            Array.prototype.forEach.call(lista.children, function (li, k) {
                li.classList.toggle('activo', k === actual); li.classList.toggle('hecho', k < actual);
            });
            bAtras.style.display = actual === 0 ? 'none' : '';
            bSig.style.display = actual === pasos.length - 1 ? 'none' : '';
            actualizarTotal();
            irAlFormulario();
        }
        function irAlFormulario() {
            var y = cont.getBoundingClientRect().top + window.pageYOffset - 84;
            window.scrollTo({ top: Math.max(0, y), behavior: 'smooth' });
        }
        function modoAgendando(on) {
            var fid = document.getElementById('fidelidad');
            var fila = fid && fid.closest('.row');
            if (fila) { fila.style.display = on ? 'none' : ''; }
            cont.style.minHeight = on ? '75vh' : '';
        }
        var inputCupon = document.getElementById('usarCupon');
        var avisoCupon = document.createElement('div');
        avisoCupon.className = 'wiz-cupon';
        avisoCupon.innerHTML = '<i class="bi bi-ticket-perforated-fill"></i> <span>Cupón de corte gratis aplicado: el servicio se cobra $0.</span> ' +
            '<button type="button" class="wiz-cupon-quitar">Quitar</button>';
        form.insertBefore(avisoCupon, progreso.nextSibling);
        function cuponActivo() { return inputCupon && inputCupon.value === '1'; }
        function actualizarTotal() {
            var t = document.getElementById('totalPagar');
            avisoCupon.style.display = cuponActivo() ? '' : 'none';
            if (!t) { totalEl.textContent = ''; return; }
            var texto = t.textContent;
            if (cuponActivo()) {
                var radio = form.querySelector('.servicio-radio:checked');
                var total = parseInt((t.textContent || '').replace(/[^0-9]/g, ''), 10) || 0;
                var precio = radio ? parseInt(radio.dataset.precio, 10) || 0 : 0;
                texto = '$' + Math.max(0, total - precio).toLocaleString('es-CO') + ' (cupón aplicado)';
            }
            totalEl.textContent = 'Total: ' + texto;
        }
        avisoCupon.querySelector('.wiz-cupon-quitar').addEventListener('click', function () {
            if (inputCupon) { inputCupon.value = '0'; }
            actualizarTotal();
        });
        function avisar(msg) { if (window.mostrarToast) { window.mostrarToast(msg, 'warning'); } else { alert(msg); } }

        function validar() {
            var paso = pasos[actual];
            var campos = paso.querySelectorAll('input:required, select:required, textarea:required');
            for (var i = 0; i < campos.length; i++) {
                var c = campos[i];
                if (c.type === 'hidden') {
                    if (!c.value) { avisar('Elige una hora disponible para continuar.'); return false; }
                } else if (!c.checkValidity()) { c.reportValidity(); return false; }
            }
            return true;
        }
        // Paso de adicionales: botón "Ninguno" para continuar sin extras
        var pasoExtras = pasos[3];
        var ninguno = document.createElement('button');
        ninguno.type = 'button';
        ninguno.className = 'btn btn-volver wiz-ninguno';
        ninguno.innerHTML = '<i class="bi bi-slash-circle"></i> Ninguno, continuar sin extras';
        ninguno.addEventListener('click', function () {
            pasoExtras.querySelectorAll('input[type="checkbox"]').forEach(function (c) {
                if (c.checked) { c.checked = false; c.dispatchEvent(new Event('change', { bubbles: true })); }
            });
            mostrar(4);
        });
        pasoExtras.appendChild(ninguno);

        bSig.addEventListener('click', function () { if (validar()) { mostrar(actual + 1); } });
        bAtras.addEventListener('click', function () { mostrar(actual - 1); });
        nav.querySelector('.wiz-cancelar').addEventListener('click', function () {
            if (inputCupon) { inputCupon.value = '0'; }
            modoAgendando(false);
            var b = document.getElementById('btnCancelarForm'); if (b) { b.click(); }
        });
        var bCupon = document.getElementById('btnUsarCupon');
        if (bCupon) {
            bCupon.addEventListener('click', function () {
                if (inputCupon) { inputCupon.value = '1'; }
                var ag = document.getElementById('btnAgendar'); if (ag) { ag.click(); }
            });
        }
        form.addEventListener('change', actualizarTotal);
        var obs = document.getElementById('totalPagar');
        if (obs) { new MutationObserver(actualizarTotal).observe(obs, { childList: true, characterData: true, subtree: true }); }
        document.getElementById('btnAgendar') && document.getElementById('btnAgendar').addEventListener('click', function () {
            // Si no viene del botón del cupón, la cita es normal
            if (inputCupon && !window.__cuponPendiente) { /* se mantiene el valor puesto por btnUsarCupon */ }
            modoAgendando(true);
            mostrar(0);
        });
        var bCancelOrig = document.getElementById('btnCancelarForm');
        if (bCancelOrig) { bCancelOrig.addEventListener('click', function () { if (inputCupon) { inputCupon.value = '0'; } modoAgendando(false); }); }
        // Enter no debe enviar el formulario antes del último paso
        form.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' && actual < pasos.length - 1 && e.target.tagName !== 'TEXTAREA') {
                e.preventDefault(); bSig.click();
            }
        });
        mostrar(0);
    });
})();

/* Si la página no trae el modal de cerrar sesión, el botón cierra sesión directamente */
document.addEventListener('DOMContentLoaded', function () {
    if (document.getElementById('modalCerrarSesion')) { return; }
    document.querySelectorAll('.btn-logout-custom[data-bs-target="#modalCerrarSesion"]').forEach(function (b) {
        b.removeAttribute('data-bs-toggle');
        b.addEventListener('click', function () { window.location.href = '/logout/'; });
    });
});

