
let timer = setInterval(function () {
  var now = new Date();
  var today = new Date(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), now.getUTCHours() - 12, now.getUTCMinutes(), now.getUTCSeconds(), now.getUTCMilliseconds());
  today = today.getTime()

  let diff;
  var endDate = new Date(Date.UTC(2023, 11, 25, 0, 0, 0));
  endDate = endDate.getTime() + (endDate.getTimezoneOffset() * 60000);

  diff = endDate - today;

  const days = Math.floor(diff / (1000 * 60 * 60 * 24));
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((diff % (1000 * 60)) / 1000);

  document.getElementById("timer").innerHTML =
    `<div class="days"><div class="numbers">${days}</div>days</div>
     <div class="hours"><div class="numbers">${hours}</div>hours</div>
     <div class="minutes"><div class="numbers">${minutes}</div>minutes</div>
     <div class="seconds"><div class="numbers">${seconds}</div>seconds</div>`;
}, 1000);
