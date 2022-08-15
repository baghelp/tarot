var console1 = CodeMirror(document.querySelector('#first_console'), {
    lineNumbers: true,
    tabSize: 2,
    mode: 'javascript',
    value: 'coconsole.log("Helconsole.log("Helconsole.lnsole.log("Hello, World");',
    readOnly: true,
});

var console2 = CodeMirror(document.querySelector('#second_console'), {
    lineNumbers: true,
    tabSize: 2,
    theme: 'ayu-mirage',
    mode: 'javascript',
    value: 'console.log("Hello, World");',
});


//console2.setOption('readOnly', true);
