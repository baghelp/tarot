// includes
require('colors');
const Diff = require('diff');

// codemirror consoles
const console1 = CodeMirror(document.querySelector('#first_console'), {
    lineNumbers: true,
    tabSize: 2,
    mode: 'javascript',
    value: 'Twas brillig, and the slithy toves\nDid gyre and gimble in the wabe:\nAll mimsy were the borogoves,\nAnd the mome raths outgrabe. \n\n“Beware the Jabberwock, my son!\nThe jaws that bite, the claws that catch!\nBeware the Jubjub bird, and shun\nThe frumious Bandersnatch!”',
    readOnly: true,
});

const console2 = CodeMirror(document.querySelector('#second_console'), {
    lineNumbers: true,
    tabSize: 2,
    theme: 'ayu-mirage',
    mode: 'javascript',
    value: 'coconsole.log("Helconsole.log("Helconsole.lnsole.log("Hello, World");',

});


// console2.on("change", function(cm, 
const one = console1.getValue();

console2.on("changes", function(changes) {
    // code to color based on output
    var other = changes.getValue();

    var diff = Diff.diffWordsWithSpace(one, other);

    var styling = [];
    var line_index = 0;
    var char_index = 0;

    diff.forEach((change) => {
        //console.log(change.value);
        // read through reproductions and removals, to get line numbers
        if( change.added ){
            return;
        }
        
        for(var i=0; i<change.value.length; i++) {
            ch = change.value[i];
            if( ch == '\n' ) {
                line_index++;
                char_index = 0;
            } else{
                char_index++;
            };
        };


        if( change.removed ){
            styling.push( {place: {line:line_index, ch:char_index}, style:{css:"color: black"}} );
            console.log({state:'removed', value: change.value})
        } else {
            styling.push( {place: {line:line_index, ch:char_index}, style:{css:"color: mediumblue"}} );
            console.log({state:'matched', value: change.value})
        };
 
    });

    last_pos = {line:0,ch:0};
    for (var i=0; i< (styling.length); i++) {
        console1.markText(last_pos, styling[i].place, styling[i].style);
        last_pos = styling[i].place;
    };

    console.log(diff);
    //console.log(styling);
});

