let cabeceraAlicuota = { // cabecera de la alicuota
  vivienda: 0,
  tasaInteres: 0,
  tasaEntrada: 0,
  fechaInicial: '',
  saldoAPagar: 0,
  fechaCreacion: '',
  periodo: 0,
  monto: 0,
  saldoPendiente: 0,
}

let id_vivienda = 0
let monto = 0


let detalleAlicuota = []; // detalles de las alicuotas

const viviendas = [];

document.addEventListener('DOMContentLoaded', function () {
  fetch(`http://localhost:8000/api/buscar_vivienda/`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
  })
    .then(response => response.ok ? response.json() : Promise.reject("Error en la red"))
    .then((data) => {
      if (Array.isArray(data)) {
        viviendas.push(...data);
      } else {
        viviendas.push(data);
      }
    })
    .catch(error => console.error("Error al crear el objeto:", error));
  console.log('Las viviendas se cargaron correctamente.');
  console.log('Viviendas: ', viviendas);
});


function mostrarSugerencias(texto) {
  const sugerencias = document.getElementById('sugerencias');
  sugerencias.innerHTML = '';

  if (texto.length === 0) return; // no mostramos sugerencias si no hay texto

  // filtramos las viviendas que coincidan con lo que ingresamos
  const coincidencias = viviendas.filter(vivienda =>
    vivienda.descripcion.toLowerCase().includes(texto.toLowerCase())
  );

  // creamos un elemento <li> para cada coincidencia que encontremos
  coincidencias.forEach(vivienda => {
    const item = document.createElement('li');
    item.textContent = vivienda.descripcion;
    item.classList.add('p-2', 'cursor-pointer', 'hover:bg-gray-100'); // Estilo para el <li>

    // llenamos la informacion cuando hacemos click en una sugerencia
    item.onclick = () => seleccionarVivienda(vivienda);

    sugerencias.appendChild(item);
  });
}

// llenamos los campos cuando hayamos seleccionado una vivienda
function seleccionarVivienda(vivienda) {
  document.getElementById('villa').value = vivienda.descripcion;
  document.getElementById('nombre').value = vivienda.nombre;
  document.getElementById('cedula').value = vivienda.cedula;
  document.getElementById('correo').value = vivienda.email;
  document.getElementById('costoVivienda').value = vivienda.valor;

  id_vivienda = vivienda.id
  monto = vivienda.valor


  // limpiamos las sugerencias despues de seleccionar la vivienda
  document.getElementById('sugerencias').innerHTML = '';
}




function GenerarAlicuota() {
  detalleAlicuota = [];

  let costoVivienda = parseFloat(document.getElementById("costoVivienda").value.replace(',', '.'));
  let periodo = Number(document.getElementById("periodo").value);
  let entrada = parseFloat(document.getElementById("entrada").value.replace('%', '').trim()) / 100;
  let interes = parseFloat(document.getElementById("interes").value.replace('%', '').trim()) / 100;
  if (costoVivienda && periodo) {
    // Calcular el pago inicial
    let pagoInicial = costoVivienda * entrada;
    let saldoPendiente = costoVivienda - pagoInicial;

    // Obtener la fecha inicial
    let fechaInicial = moment().format('YYYY-MM-DD')
    let fechaPago = moment(fechaInicial);  // Usando moment.js para manejar las fechas
    fechaPago.add(1, 'months');

    // Limpiar la tabla de pagos antes de agregar nuevos datos
    let tablaPagos = document.getElementById("tablaPagos").getElementsByTagName('tbody')[0];
    tablaPagos.innerHTML = "";  // Limpiar la tabla

    let totalSaldoAPagar = saldoPendiente + (saldoPendiente * interes);
    let totalSaldoPendiente = saldoPendiente + (saldoPendiente * interes);
    let fechas = []; // Para almacenar las fechas

    for (let i = 1; i <= periodo; i++) {
      let totalperiodo = totalSaldoAPagar / periodo;  // Total del pago de cada periodo

      let diaPago = document.getElementById("fechaInicial").value;

      fechaPago.date(diaPago);
      fechas[i] = fechaPago.format('DD-MM-YYYY');
      let fechaVencimiento = fechaPago.clone().add(4, 'days').format('DD-MM-YYYY');

      let recargo = 0;  // Por ahora, no hay recargos

      // Agregar la fila a la tabla
      tablaPagos.innerHTML += `
        <tr>
            <td class="border border-gray-300 px-4 py-2 text-center">${i}</td>
            <td class="border border-gray-300 px-4 py-2 text-center">${fechas[i]}</td>
            <td class="border border-gray-300 px-4 py-2 text-center">${fechaVencimiento}</td>
            <td class="border border-gray-300 px-4 py-2 text-center">${recargo}</td>
            <td class="border border-gray-300 px-4 py-2 text-center">${totalperiodo.toFixed(2)}</td>
            <td class="border border-gray-300 px-4 py-2 text-center">${totalperiodo.toFixed(2)}</td>
            <td class="border border-gray-300 px-4 py-2 text-center">Pendiente</td>
        </tr>
    `;
      const alicuota = {
        secuencia: i,
        fechaPago: fechas[i],
        fechaVencimiento: fechaVencimiento,
        recargo: recargo,
        totalPagar: totalperiodo.toFixed(2),
        saldoPendiente: totalperiodo.toFixed(2),
        estado: "Pendiente"
      }


      detalleAlicuota.push(alicuota); // Agregar la alicuota al array

      // Mover la fecha de pago al siguiente mes para la próxima iteración
      fechaPago.add(1, 'month');
    }
    cabeceraAlicuota = {
      vivienda: id_vivienda,
      tasaInteres: 1,
      tasaEntrada: 1,
      fechaInicial: fechaInicial,
      saldoAPagar: totalSaldoAPagar,
      fechaCreacion: fechaInicial,
      periodo: periodo,
      monto: monto,
      saldoPendiente: totalSaldoAPagar,
    }
    // Mostrar el pago inicial en la interfaz si es necesario
    document.getElementById("pagoInicial").value = `$${pagoInicial.toFixed(2)}`;
    document.getElementById("saldoPendiente").value = `$${totalSaldoPendiente.toFixed(2)}`;
    document.getElementById("saldoPagar").value = `$${totalSaldoAPagar.toFixed(2)}`;
    document.getElementById("interesTotal").value = `$${(saldoPendiente * interes).toFixed(2)}`;
    document.getElementById("monto").value = `$${saldoPendiente.toFixed(2)}`;
    document.getElementById("totalPagos").textContent = `$${totalSaldoAPagar.toFixed(2)}`;
    document.getElementById("totalaPagar").textContent = `$${totalSaldoAPagar.toFixed(2)}`;
    document.getElementById("fechaAlicuota").value = `${fechaInicial}`;

    console.log('Cabecera');
    console.log(cabeceraAlicuota);
    console.log('Detalle');
    console.log(detalleAlicuota);
  } else {
    alert("Debe seleccionar una vivienda y el periodo.");
  }
}
