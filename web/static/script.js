const socket = io();
const terminal = document.getElementById('terminal');

document.addEventListener('keydown', (event) => {
    event.preventDefault();

    let key = event.key;
    let modifiers = '';

    // Handle special keys
    const specialKeys = {
        'Escape': '<Esc>',
        'Enter': '<CR>',
        'Backspace': '<BS>',
        'Tab': '\t',
        'ArrowUp': '<Up>',
        'ArrowDown': '<Down>',
        'ArrowLeft': '<Left>',
        'ArrowRight': '<Right>',
        'Home': '<Home>',
        'End': '<End>',
        'PageUp': '<PageUp>',
        'PageDown': '<PageDown>',
        'Delete': '<Del>',
        'Insert': '<Insert>'
    };

    if (key in specialKeys) {
        key = specialKeys[key];
    } else if (key.startsWith('F') && key.length > 1) {
        // Function keys
        key = `<${key}>`;
    } else if (event.ctrlKey && key.length === 1) {
        // Control key combinations
        key = `<C-${key.toUpperCase()}>`;
    } else if (event.altKey && key.length === 1) {
        // Alt key combinations
        key = `<M-${key}>`;
    } else if (key.length === 1) {
        // Single characters (including shifted characters)
        key = key;
    } else {
        // Ignore other keys
        return;
    }

    socket.emit('command', key);
});

socket.on('update', (data) => {
    terminal.innerHTML = data.output;
});
