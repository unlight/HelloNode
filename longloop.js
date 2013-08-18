var start = new Date();
var c = function() {

	var end = new Date();
	process.stdout.write("longloop.js: " + ((end - start)/1000));
}

setTimeout(c, 1500)