var myCodeMirror1 = CodeMirror(document.querySelector('#first_console'), {
    lineNumbers: true,
    tabSize: 2,
    value: 'console.log("Hello, World");'
});

var myCodeMirror2 = CodeMirror(document.querySelector('#second_console'), {
    lineNumbers: true,
    tabSize: 2,
    value: 'console.log("Hello, World");'
});
