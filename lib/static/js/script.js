div.flush-collapseOne.rendered = function() {
document.getElementById("id_rango_precio").oninput = function() { formatPrice() };
}

function formatPrice() {

  var val = document.getElementById("id_rango_precio").value //gets the oninput value
  const formatter = new Intl.NumberFormat('en-US', {style: 'currency',currency: 'USD',});                       
  let valFormatted = formatter.format(val);
  document.getElementById('output').innerHTML = valFormatted //displays this value to the html page

}

function getDuration(horaInicio, horaFin) {
  
  var timeStart = new Date("01/01/2007 " + dateString(horaInicio));
  var timeEnd = new Date("01/01/2007 " + dateString(horaFin));
    
  duration = (timeEnd - timeStart);

  return formatDuration(duration);
}

function dateString(dateString) {
  
  const [time, period] = dateString.split(' '); 
  const [hour, minute] = time.split(':'); 
  let formattedHour = parseInt(hour); 

  if (period === 'p.m.') { 
      formattedHour += 12; 
  }
  return `${formattedHour}:${minute}`;
}

function formatDuration(milliseconds) {

  const seconds = Math.floor((milliseconds / 1000) % 60);
  const minutes = Math.floor((milliseconds / 1000 / 60) % 60);
  const hours = Math.floor((milliseconds / 1000 / 60 / 60) % 24);
  const formattedTime = hours.toString() + 'hrs ' + minutes.toString() + 'mins.';
  console.log(formattedTime);

  return formattedTime

}

