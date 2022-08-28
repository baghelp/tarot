

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
    value: 'Type your code here',

});


let first_console_text = console1.getValue();

console2.on("changes", function(changes) {
    compare_consoles(first_console_text, changes);
    /*
    // code to color based on output
    var other = changes.getValue();

    var diff = Diff.diffWordsWithSpace(first_console_text, other);

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
    */
});

function compare_consoles(console1_text, console2_text) {
    var text2 = console2.getValue();

    var diff = Diff.diffWordsWithSpace(console1_text, text2);

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
}


function trigger_selection(element) {
    console.log('hi');
    let text = element.innerText;
    difficulty = text.split(':')[0];
    example_name = text.split(': ')[1];
    document.getElementById('lesson').innerText = example_name;
    $.getJSON('../static/code_immersion/lessons.json', function(data) {
        text_selection = data['levels'][difficulty][example_name];
        console1.setValue(text_selection);
        first_console_text = text_selection;
    });
}


$(document).ready(function(){
    $.getJSON('../static/code_immersion/lessons.json', function(data) {
        for( var root in data){
            for( var level in data[root]){
                for( var filename in data[root][level]){
                    $('#ddm').append('<li class="dropdown-item" id="option"><a href="#">' + level + ': ' + filename + '</a></li>');
                }
            }
        }
        let links = document.getElementsByClassName('dropdown-item');
        for (let i=0; i<links.length; i++) {
            links[i].addEventListener("click",
                function() {
                    trigger_selection(links[i]);
                }
            );
        };
    });
});

