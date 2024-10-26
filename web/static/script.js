const socket = io();
const terminal = document.getElementById('terminal');

document.addEventListener('keydown', (event) => {
    let key = event.key;
    let modifiers = '';

    if (event.ctrlKey) {
        modifiers += 'C-';
    }
    if (event.altKey) {
        modifiers += 'M-';
    }
    if (event.shiftKey) {
        modifiers += 'S-';
    }

    if (event.key === 'Escape') {
        key = '<Esc>';
    } else if (event.key === 'Enter') {
        key = '<CR>';
    } else if (event.key === 'Backspace') {
        key = '<BS>';
    } else if (event.key === 'Tab') {
        key = '<Tab>';
    } else if (event.key === ' ') {
        key = '<Space>';
    } else if (event.key.startsWith('Arrow')) {
        key = `<${event.key.slice(5)}>`;
    } else if (event.key.startsWith('F') && event.key.length > 1) {
        key = `<${event.key}>`;
    } else if (event.key === 'Home') {
        key = '<Home>';
    } else if (event.key === 'End') {
        key = '<End>';
    } else if (event.key === 'Insert') {
        key = '<Insert>';
    } else if (event.key === 'Delete') {
        key = '<Del>';
    } else if (event.key === 'PageUp') {
        key = '<PageUp>';
    } else if (event.key === 'PageDown') {
        key = '<PageDown>';
    }

    socket.emit('command', modifiers + key);
    event.preventDefault();
});

socket.on('update', (data) => {
    terminal.innerHTML = data.output;
});
