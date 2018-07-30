// AE_Script.js started on 7/25/2018
// Authors: Marilyn Groppe, Cormac Dacker
// Version # 0.0.01
'use strict';

const path = require('path');
const fs   = require('fs');
const Project = require('nexrender').Project;
const renderer = require('nexrender').renderer;
const api = require('nexrender').api;

/*
STEPS:
1. Grab and store the song and image from IN directory DONE!
1.1 Match the corresponding song and image
2. Plug them into the template
    a. Remove the old song/background?
3. Ensure the render time matches the song length
4. Render at the proper bitrate and store in the OUT directory
 */
var PATH = 'C:/Users/corma/Documents/GitHub/YT-Music-AI/AfterEffects/In/';
var OUT = 'C:/Users/corma/Documents/GitHub/YT-Music-AI/AfterEffects/Out/';





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
    api.config({
        host: 'localhost',
        port: 9988
    });
    let ff = name.file;
    let s = "";
    for(let i = 0; i < ff.length; i++) {
        if(ff[i] === ' ') {
            s += '%20';
        } else {
            s += ff[i];
        }
        console.log(s);
    }
    let assets = [
        {
            type: 'project',
            src: 'C:/Users/corma/Documents/GitHub/YT-Music-AI/AfterEffects/AscentTemplate.aep',
            name: name.songName
        },
        {
            type: 'image',
            src: image.imageUrl,
            name: 'wallhaven-3020.jpg'
        },
        {
            type: 'audio',
            src: song.songUrl,
            name: s
        }
    ];

    let model = {
        template: 'C:/Users/corma/Documents/GitHub/YT-Music-AI/AfterEffects/AscentTemplate.aep',
        composition: 'Render Me!!',
        settings: {
            outputModule: 'h264',
            outputExt: 'mp4'
        },
        assets: assets
    };

    api.create(model).then(
        (project) => {
            console.log('project saved');
            project.on('uncaughtException', function (err) {
                console.log(err);
            });
            project.on('rendering', function(err, project) {
                console.log('project rendering started');
            });
            project.on('finished', function(err, project) {
                console.log('project rendered');
                //move project to Out folder
            });
            project.on('failure', function(err, project) {
                console.log('project failed.');
            });

    });
}


function main() {
    let imgs = findFilesInDir(PATH, '.jpg');
    let songs = findFilesInDir(PATH, '.mp3');
    for(let i = 0; i < songs.length && i < imgs.length; i++) {
        console.log("Rendering... (" + (i+1) + "/" + songs.length + ")");
        const desired = songs[i].length - (PATH.length + 16);
        const img = {
            imageUrl: imgs[i],
            name: 'IMAGE'
        };
        const sng = {
            songUrl: songs[i],
            name: 'SONG'
        };
        const name = {
            songName: songs[i].substr(PATH.length, desired),
            name: 'NAME',
            file: songs[i].substr(PATH.length)
        };
        buildVideo(sng, name, img);
    }


}

main();