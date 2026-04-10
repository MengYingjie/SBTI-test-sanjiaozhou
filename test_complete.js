document.querySelectorAll('input[type="radio"]').forEach((el, index) => {
    if (index % 3 === 0) el.click();
});
document.getElementById('submitBtn').disabled = false;
document.getElementById('submitBtn').click();
