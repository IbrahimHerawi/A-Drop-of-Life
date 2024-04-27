document.querySelectorAll('input[type="radio"]').forEach(
    function(radio) {
        radio.addEventListener('click',
            function() {
                document.getElementById('bloodgroups').submit();
                sessionStorage.setItem('checked', radio.id);
            }
        )
    }
)


let btn_checked = sessionStorage.getItem('checked');
document.getElementById(btn_checked).checked = true;

