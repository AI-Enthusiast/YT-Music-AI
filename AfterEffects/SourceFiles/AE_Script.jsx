// AE_Script.js started on 7/25/2018
// Authors: Cormac Dacker, Marilyn Groppe
// Version # 0.0.01

path = require('path');
fs   = require('fs');
/*
STEPS:
1. Grab and store the song and image from IN directory DONE!
1.1 Match the corresponding song and image
2. Plug them into the template
    a. Remove the old song/background?
3. Ensure the render time matches the song length
4. Render at the proper bitrate and store in the OUT directory
 */
PATH = 'C:/Users/corma/Documents/GitHub/YT-Music-AI/AfterEffects/In/';

//Thanks to Nicolas S.Xu on StackOverflow for this method!
function findFilesInDir(startPath,filter){

    var results = [];

    if (!fs.existsSync(startPath)){
        console.log("no dir ",startPath);
        return;
    }

    var files=fs.readdirSync(startPath);
    for(var i=0;i<files.length;i++){
        var filename=path.join(startPath, files[i]);
        var stat = fs.lstatSync(filename);
        if (stat.isDirectory()) {
            results = results.concat(findFilesInDir(filename,filter)); //recurse
        }
        else if (filename.indexOf(filter) >= 0) {
            console.log('-- found: ',filename);
            results.push(filename);
        }
    }
    return results;
}


function buildVideo(song, name, image) {
    var video = app.newProject();
}


function main() {
    var imgs = findFilesInDir(PATH, '.jpg');
    var songs = findFilesInDir(PATH, '.mp3');
    for(var i = 0; i < songs.length && i < imgs.length; i++) {
        console.log("Rendering... (" + (i+1) + "/" + songs.length + ")");
        var desired = songs[i].length - (PATH.length + 16);
        var img = {
            imageUrl: imgs[i],
            name: 'IMAGE'
        };
        var sng = {
            songUrl: songs[i],
            name: 'SONG'
        };
        var name = {
            songName: songs[i].substr(PATH.length, desired),
            name: 'NAME'
        };



    }


}

main();