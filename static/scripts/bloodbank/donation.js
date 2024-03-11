document.querySelectorAll('input[type="radio"]').forEach(
    function(radio) {
        radio.addEventListener('click',
            function() {
                document.getElementById('donation').submit();
                sessionStorage.setItem('checked', radio.id);
            }
        )
    }
)


let btn_checked = sessionStorage.getItem('checked');
document.getElementById(btn_checked).checked = true;

