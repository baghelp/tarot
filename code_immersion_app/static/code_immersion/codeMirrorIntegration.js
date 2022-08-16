// includes
require('colors');
const Diff = require('diff');

// codemirror consoles
const console1 = CodeMirror(document.querySelector('#first_console'), {
    lineNumbers: true,
    tabSize: 2,
    mode: 'javascript',
    value: 'This is a pretty long sentence. others are longer but this is long.',
    readOnly: true,
});

const console2 = CodeMirror(document.querySelector('#second_console'), {
    lineNumbers: true,
    tabSize: 2,
    theme: 'ayu-mirage',
    mode: 'javascript',
    value: 'coconsole.log("Helconsole.log("Helconsole.lnsole.log("Hello, World");',
});

//console2.on("change", function(cm, 
const one = console1.getValue();

console2.on("changes", function(changes) {
    console.log(changes);
    console.log(console1);
    console.log(console2);
    // code to color based on output
    var other = changes.getValue();

    //var diff = Diff.diffWords(one, other);
    var diff = Diff.diffChars(one, other);

    /* 
    diff.forEach((part) => {
        //green for additions, red for deletions, grey for common parts
        const color = part.added ? 'green':
            part.removed ? 'red' : 'grey';
        //console.log(part.value[color]);
    });
    */
    

    //console1.markText({line:0,ch:1}, {line:2,ch:5}, {css:"color: green"});

    console.log(diff);
});

