// Initialize Selection JS

const selection = new SelectionArea({
    document: window.document,
    class: 'selection-area',
    container: 'body',
    selectables: ['#media > li'],
    boundaries: ['#media'],
})

// Selection Logic

selection.on('start', ({ event, store }) => {
    let target = event.target.parentNode;
    if (target.classList.contains('selected')) {
        target.classList.remove('selected');
        store.changed.removed.push(target);
    }
}).on('move', ({ store }) => {
    for (const el of store.changed.added) {
        el.classList.add('selected');
    }
    for (const el of store.changed.removed) {
        el.classList.remove('selected');
    }
}).on('stop', ({ store }) => {
    selection.keepSelection();
    store.stored = store.stored.filter((item, index, self) =>
        index === self.findIndex((t) => (
            t.innerText === item.innerText
        ))
    )
});

// Capture object when it's logged

function clearEmpties(o) {
    for (var k in o) {
        if (!o[k] || typeof o[k] !== "object") {
            continue // If null or not an object, skip to the next iteration
        }
        // The property is an object
        clearEmpties(o[k]); // <-- Make a recursive call on the nested object
        if (Object.keys(o[k]).length === 0) {
            delete o[k]; // The object had no properties, so delete that property
        }
    }
}

function capture(object) {
    let whitelist = ['stored', 'selected', 'changed', 'added', 'removed', 'tagName', 'classList', 'innerText'];
    let parsed = JSON.parse(JSON.stringify(object, whitelist, 2));
    clearEmpties(parsed);
    return JSON.stringify(parsed, null, 2);
}

// Helper function to copy file list to clipboard.

let lastCopied = [];

function textToClipboard(text) {
    const dummy = document.createElement("textarea");
    document.body.appendChild(dummy);
    dummy.value = text;
    dummy.select();
    document.execCommand("copy");
    document.body.removeChild(dummy);
}

// Copy and Clear Selection buttons.

let notifTimer;

function showNotification(text) {
    clearTimeout(notifTimer);
    const notif = document.querySelector('.notification');
    notif.classList.add('visible');
    notif.innerText = text;
    notifTimer = setTimeout(() => {
        notif.innerText = '';
        notif.classList.remove('visible')
    }, 3000);
}

function copySelection() {
    const elements = selection.getSelection();
    const paths = elements.map(function (element) {
        return element.querySelector('div.info').innerText
    })
    lastCopied = paths;
    textToClipboard(paths.join("\r\n"));
    let notifText = 'Copied ' + paths.length + ' file names to the clipboard';
    showNotification(notifText);
}

function toggleSelection() {
    let elements = selection.getSelection();
    if (elements.length > 0) {
        for (const element of elements) {
            element.classList.remove('selected');
        }
        selection.clearSelection();
        showNotification('Deselected ' + elements.length + ' file names');
    } else {
        elements = document.querySelectorAll('#media > li');
        for (const element of elements) {
            element.classList.add('selected');
            selection.select(element);
        }
        selection.keepSelection();
        showNotification('Selected ' + elements.length + ' file names');
    }
}

// Alert if there are selected items which haven't been copied

window.onbeforeunload = function(){
    if (lastCopied.length != selection.getSelection().length) {
        return 'There are unselected elements left to be copied! Are you sure you want to leave?'
    }
    return undefined;
};
