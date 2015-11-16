 document.getElementById("myform").onsubmit = function(e) {

    e.preventDefault();


    var f = e.target,
        formData = new FormData(f),
        xhr = new XMLHttpRequest();

    xhr.open("POST", f.action);
    xhr.send(formData);
}