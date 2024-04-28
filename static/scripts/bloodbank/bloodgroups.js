document.querySelectorAll('input[type="radio"]').forEach(
    function(radio) {
        radio.addEventListener('click',
            function() {
                document.getElementById('bloodgroups').submit();
            }
        )
    }
)



var params = new URLSearchParams(window.location.search);
var gender_param = params.get('gender');

if (gender_param === 'Male'){
    document.getElementById('Male').checked = true;
}
else if (gender_param === 'Female'){
    document.getElementById('Female').checked = true;
}
else {
    document.getElementById('genderall').checked = true;
}

