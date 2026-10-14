// Live estimate on the lifestyle form. The final numbers are calculated by app.py;
// these factors are kept in sync with it so the preview matches the results page.
(function () {
    var EF = { walking: 0, train: 0.041, bus: 0.089, motorcycle: 0.103, car: 0.171 }; // kg CO2e per passenger-km
    var GRID = 0.82; // kg CO2e per kWh
    var DIET = { plant: 2.9, vegetarian: 3.8, mixed: 5.6, meat: 7.2 }; // kg CO2e per day

    var $ = function (id) { return document.getElementById(id); };
    var form = document.querySelector(".lifestyle-form");

    function choice(name) {
        var r = form.querySelector('input[name="' + name + '"]:checked');
        return r ? r.value : "";
    }
    function num(id, fallback) {
        var v = parseFloat($(id).value);
        return isFinite(v) ? v : fallback;
    }
    function fmt(n, d) { return n.toFixed(d === undefined ? 1 : d); }

    function update() {
        var transport = choice("transport") || "bus";
        var diet = choice("diet") || "mixed";
        var distance = Math.min(150, Math.max(0, num("distance", 0)));
        var passengers = Math.min(8, Math.max(1, Math.round(num("passengers", 1))));
        var electricity = Math.min(50, Math.max(0, num("electricity", 0)));
        var household = Math.min(10, Math.max(1, Math.round(num("household_size", 1))));

        $("passengerGroup").hidden = transport !== "car";

        var t = EF[transport] * distance / (transport === "car" ? passengers : 1);
        var e = electricity / household * GRID;
        var f = DIET[diet];
        var day = t + e + f;

        $("liveDay").textContent = fmt(day);
        $("liveYear").textContent = fmt(day * 365 / 1000, 2);
        $("lT").textContent = fmt(t) + " kg";
        $("lE").textContent = fmt(e) + " kg";
        $("lF").textContent = fmt(f) + " kg";
        var total = day || 1;
        $("sT").style.width = (t / total * 100) + "%";
        $("sE").style.width = (e / total * 100) + "%";
        $("sF").style.width = (f / total * 100) + "%";
    }

    function link(range, input) {
        range.addEventListener("input", function () { input.value = range.value; update(); });
        input.addEventListener("input", function () {
            var v = parseFloat(input.value);
            if (isFinite(v)) range.value = v;
            update();
        });
    }

    link($("distanceRange"), $("distance"));
    link($("electricityRange"), $("electricity"));
    $("passengers").addEventListener("input", update);
    $("household_size").addEventListener("input", update);
    form.addEventListener("change", update);
    update();
})();
