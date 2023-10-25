// Input Tag Number Only
function isNumberKey(event) {
  var charCode = (event.which) ? event.which : event.keyCode
  if (charCode > 31 && (charCode < 48 || charCode > 57))
    return false;
  return true;
}

// Input Tag Decimal Only
function isDecimalKey(event) {
  var charCode = (event.which) ? event.which : event.keyCode
  if (charCode > 31 && (charCode != 46 &&(charCode < 48 || charCode > 57)))
    return false;
  return true;
}

// Footer Year Copyright
const since = 2023;
const nowYear = new Date().getFullYear();
const footerYear = (since === nowYear) ? (since) : (`${since}-${nowYear}`);
document.getElementById('footer-year').innerHTML = footerYear;