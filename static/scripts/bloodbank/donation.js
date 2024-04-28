document.querySelectorAll('input[type="radio"]').forEach(
    function(radio) {
        radio.addEventListener('click',
            function() {
                document.getElementById('donation').submit();
            }
        )
    }
)


var params = new URLSearchParams(window.location.search);
var status_param = params.get('status');

if (status_param === '1'){
    document.getElementById('statusvalid').checked = true;
}
else if (status_param === '2'){
    document.getElementById('statusinvalid').checked = true;
}
else {
    document.getElementById('statusall').checked = true;
}

