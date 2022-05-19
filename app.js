function runFfmpeg(filename) {
    var proc = process.spawn('ffmpeg', ['-i', 'pathname', filename]);
    proc.stdout.on('data', function(data) { console.log("stdout: " + data); });
    proc.stderr.on('data', function(data) { console.log("stderr: " + data); });
    proc.on('exit', function(code) { console.log("exit: " + code); });
  }
  
  var filenames = ['foo.mp4', 'bar.mp4', 'gah.mp4'];
  filenames.forEach(function(filename) { runFfmpeg(filename); });