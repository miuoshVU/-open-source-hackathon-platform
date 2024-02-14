$('#id_phone').on('input', function () {
    var currentValue = $(this).val();
    if (!/^\d*$/.test(currentValue)) {
        $(this).val(currentValue.replace(/[^\d]/g, ''));
    }
});

$('#id_first_name, #id_last_name').on('input', function () {
    var currentValue = $(this).val();
    if (!/^[A-Za-z]*$/.test(currentValue)) {
        $(this).val(currentValue.replace(/[^A-Za-z]/g, ''));
    }
});
