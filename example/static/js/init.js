var body = document.getElementsByTagName('body')[0];
body.insertBefore(document.createTextNode('This text was created by Javascript.'));

if (window.console && console.log) console.log('Successfully loaded init.js');
