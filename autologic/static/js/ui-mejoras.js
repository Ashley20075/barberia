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
