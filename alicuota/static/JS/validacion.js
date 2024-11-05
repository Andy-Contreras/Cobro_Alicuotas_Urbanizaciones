function validarNumero(input) {
    // Reemplazar cualquier carácter que no sea un dígito
    input.value = input.value.replace(/[^0-9]/g, '');
}