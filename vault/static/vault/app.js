// COPY UTILS: intenta usar el portapapeles moderno y cae a un fallback si hace falta.
async function copySnippetText(text) {
    if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
        return true;
    }

    // FALLBACK DE COMPATIBILIDAD: usa un textarea temporal para navegadores o contextos restringidos.
    const helper = document.createElement('textarea');
    helper.value = text;
    helper.setAttribute('readonly', '');
    helper.style.position = 'fixed';
    helper.style.opacity = '0';
    helper.style.pointerEvents = 'none';
    document.body.appendChild(helper);
    helper.select();

    const copied = document.execCommand('copy');
    document.body.removeChild(helper);
    return copied;
}

document.addEventListener('DOMContentLoaded', () => {
    // UI COPY: conecta todos los botones marcados para copiar código desde listado y detalle.
    document.querySelectorAll('[data-copy-button]').forEach((button) => {
        const label = button.querySelector('[data-copy-label]');
        const defaultLabel = label ? label.textContent.trim() : 'Copiar';
        let feedbackTimer;
        // ESTADOS VISUALES: clases base, éxito y error para dar feedback inmediato al usuario.
        const baseClasses = [
            'border-white/10',
            'bg-white/5',
            'text-slate-200',
        ];
        const successClasses = [
            'border-emerald-400/30',
            'bg-emerald-400/15',
            'text-emerald-100',
        ];
        const errorClasses = [
            'border-rose-400/30',
            'bg-rose-400/15',
            'text-rose-100',
        ];

        // RESETEO DE ESTADO: devuelve el botón a su estilo original antes de aplicar un nuevo feedback.
        const resetState = () => {
            button.classList.remove(...successClasses, ...errorClasses);
            button.classList.add(...baseClasses);
        };

        button.addEventListener('click', async () => {
            // ORIGEN DEL TEXTO: toma el contenido desde el selector indicado en data-copy-source.
            const sourceSelector = button.dataset.copySource;
            const source = sourceSelector ? document.querySelector(sourceSelector) : null;
            const text = source
                ? ('value' in source ? source.value : source.textContent)
                : '';

            // GUARD CLAUSE: evita ejecutar el flujo de copia si no hay contenido útil.
            if (!text.trim()) {
                return;
            }

            window.clearTimeout(feedbackTimer);

            try {
                // ÉXITO: copia el texto y actualiza el botón temporalmente.
                const copied = await copySnippetText(text);
                if (!copied) {
                    throw new Error('Copy failed');
                }
                resetState();
                button.classList.remove(...baseClasses);
                button.classList.add(...successClasses);
                if (label) {
                    label.textContent = 'Copiado';
                }
            } catch (error) {
                // ERROR: informa fallo de copia manteniendo el botón operativo para otro intento.
                resetState();
                button.classList.remove(...baseClasses);
                button.classList.add(...errorClasses);
                if (label) {
                    label.textContent = 'Error';
                }
            }

            // RESTAURACIÓN: tras un breve intervalo, recupera el estilo y texto originales.
            feedbackTimer = window.setTimeout(() => {
                resetState();
                if (label) {
                    label.textContent = defaultLabel;
                }
            }, 1800);
        });
    });
});
