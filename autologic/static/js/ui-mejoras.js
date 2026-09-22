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


/* =====================================================
   MENU HAMBURGUESA PARA LAS NAVBARS DE LOS PANELES
   -----------------------------------------------------
   .navbar-custom (barbero, cliente, admin, inventario,
   cierre de caja, agendar cita...) nunca tuvo colapso
   para pantallas chicas: todos los botones (campana,
   usuario, enlaces, tema, cerrar sesion) iban en una
   sola fila que en el celular se amontonaba, se cortaba
   o directamente tapaba otros botones al cargar.

   Esto NO toca el HTML de cada plantilla: busca el
   patron que ya usan todas (marca + fila de botones) y
   le inyecta un boton de hamburguesa por JS, asi la
   correccion aplica en todos los paneles a la vez.
===================================================== */
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
