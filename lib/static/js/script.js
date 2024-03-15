function getDuration(horaInicio, horaFin) {
  var timeStart = new Date("01/01/2007 " + dateString(horaInicio));
  var timeEnd = new Date("01/01/2007 " + dateString(horaFin));
  
  // Verificar si la hora de fin es menor que la hora de inicio
  // Esto indicaría que el vuelo se extiende hasta el día siguiente
  if (timeEnd < timeStart) {
      // Agregar 24 horas a la hora de fin
      timeEnd.setHours(timeEnd.getHours() + 24);
  }

  var duration = (timeEnd - timeStart);

  return formatDuration(duration);
}

function dateString(dateString) {
  const [time, period] = dateString.split(' '); 
  const [hour, minute] = time.split(':'); 
  let formattedHour = parseInt(hour); 

  // Convertir las horas a formato de 24 horas
  if (period === 'p.m.' && formattedHour < 12) { 
      formattedHour += 12; 
  } else if (period === 'a.m.' && formattedHour == 12) {
      formattedHour = 0; // Si es 12 a.m., convertir a 0 (medianoche)
  }

  return `${formattedHour.toString().padStart(2, '0')}:${minute}`;
}

function formatDuration(milliseconds) {
  const seconds = Math.floor((milliseconds / 1000) % 60);
  const minutes = Math.floor((milliseconds / 1000 / 60) % 60);
  const hours = Math.floor((milliseconds / 1000 / 60 / 60));
  const formattedTime = hours.toString() + 'hrs ' + minutes.toString() + 'mins.';
  console.log(formattedTime);

  return formattedTime;
}