async function copySnippetText(text) {
    if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
        return true;
    }

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
    document.querySelectorAll('[data-copy-button]').forEach((button) => {
        const label = button.querySelector('[data-copy-label]');
        const defaultLabel = label ? label.textContent.trim() : 'Copiar';
        let feedbackTimer;
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

        const resetState = () => {
            button.classList.remove(...successClasses, ...errorClasses);
            button.classList.add(...baseClasses);
        };

        button.addEventListener('click', async () => {
            const sourceSelector = button.dataset.copySource;
            const source = sourceSelector ? document.querySelector(sourceSelector) : null;
            const text = source
                ? ('value' in source ? source.value : source.textContent)
                : '';

            if (!text.trim()) {
                return;
            }

            window.clearTimeout(feedbackTimer);

            try {
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
                resetState();
                button.classList.remove(...baseClasses);
                button.classList.add(...errorClasses);
                if (label) {
                    label.textContent = 'Error';
                }
            }

            feedbackTimer = window.setTimeout(() => {
                resetState();
                if (label) {
                    label.textContent = defaultLabel;
                }
            }, 1800);
        });
    });
});
