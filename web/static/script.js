const socket = io();
const terminal = document.getElementById('terminal');

document.addEventListener('keydown', (event) => {
    event.preventDefault(); // Prevent default browser behavior
    
    let key = event.key;
    let modifiers = '';

    if (event.ctrlKey && key !== 'Control') modifiers += 'C-';
    if (event.altKey && key !== 'Alt') modifiers += 'M-';
    if (event.metaKey && key !== 'Meta') modifiers += 'D-'; // For Command key on Mac
    if (event.shiftKey && key.length > 1) modifiers += 'S-';

    // Handle special keys
    switch (key) {
        case 'Escape': key = '<Esc>'; break;
        case 'Enter': key = '<CR>'; break;
        case 'Backspace': key = '<BS>'; break;
        case 'Tab': key = '<Tab>'; break;
        case ' ': key = '<Space>'; break;
        case 'ArrowLeft': key = '<Left>'; break;
        case 'ArrowRight': key = '<Right>'; break;
        case 'ArrowUp': key = '<Up>'; break;
        case 'ArrowDown': key = '<Down>'; break;
        case 'Home': key = '<Home>'; break;
        case 'End': key = '<End>'; break;
        case 'PageUp': key = '<PageUp>'; break;
        case 'PageDown': key = '<PageDown>'; break;
        case 'Delete': key = '<Del>'; break;
        case 'Insert': key = '<Insert>'; break;
    }

    // Handle function keys
    if (key.startsWith('F') && key.length > 1) {
        key = `<${key}>`;
    }

    // Handle modifier keys when pressed alone
    if (['Control', 'Alt', 'Shift', 'Meta'].includes(key)) {
        return; // Don't send modifier keys when pressed alone
    }

    // Handle uppercase letters
    if (key.length === 1 && key.match(/[A-Z]/)) {
        modifiers += 'S-';
        key = key.toLowerCase();
    }

    const command = modifiers + key;
    socket.emit('command', command);
});

socket.on('update', (data) => {
    terminal.innerHTML = data.output;
});
