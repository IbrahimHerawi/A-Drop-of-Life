var selectElement = document.getElementById("bg");
selectElement.addEventListener("change", function() {
  document.getElementById("patient").submit();
});


var params = new URLSearchParams(window.location.search);
var bg_param = params.get('bg');

if (bg_param && bg_param !== 'all'){
    document.getElementById('bg').value = bg_param;
}
else {
    document.getElementById('bg').value = 'all';
}

