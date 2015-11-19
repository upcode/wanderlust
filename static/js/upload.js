dropbox.filedrop({
    paramname: 'file',
    maxfiles: 10,
    maxfilesize: 5,
    url: '/upload',
    uploadFinished:function(i,file,response){
        $.data(file).addClass('done');
    }