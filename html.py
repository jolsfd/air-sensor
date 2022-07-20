html = """<!DOCTYPE html>
<html>
  <style>
    body {
      font-family: Courier New, Courier, Lucida Sans Typewriter,
        Lucida Typewriter, monospace;
      color: #222;
      margin: 0;
    }
    h1,
    h2,
    h3 {
      margin: 0 0 0.35em;
    }

    h1 {
      font-size: 40px;
    }

    h2 {
      font-size: 28px;
      text-align: center;
    }
    p {
      margin: 0 0 1.15em;
      text-align: center;
    }
    .container {
      max-width: 800px;
      margin-left: auto;
      margin-right: auto;
      padding: 24px;
    }

    header {
      background-color: rgb(89, 47, 145);
      color: #ffffff;
      text-align: center;
    }
  </style>
  <body>
    <header id="title">
      <div class="container">
        <h1>BMP280 Sensor</h1>
      </div>
    </header>
    <div class="container">
      <h2>Temperature: <span id="tempValue">None</span> &ordm;C</h2>
    </div>
    <div class="container">
      <h2>Pressure: <span id="pressureValue">None</span> pa</h2>
    </div>
    <div class="container">
      <p>Source: <a href="https://github.com/jolsfd/bmp280-sensor">GitHub</a></p>
    </div>

    <script>
      setInterval(function () {
        // Call a function repetatively with 2 Second interval
        getData();
      }, 2000); //2000mSeconds update rate

      function getData() {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
          if (this.readyState == 4 && this.status == 200) {
            values = this.responseText.split(" ");
            document.getElementById("tempValue").innerHTML = values[0];
            document.getElementById("pressureValue").innerHTML = values[1];
            changeColor(values[0]);
          }
        };
        xhttp.open("GET", "data", true);
        xhttp.send();
      }

      function changeColor(value) {
        color = "";

        if (value <= 0) {
          color = "#0034a8";
        } else if (0 <= value && value <= 15) {
          color = "#2c9aba";
        } else if (16 <= value && value <= 20) {
          color = "#22912d";
        } else if (21 <= value && value <= 23) {
          color = "#008000";
        } else if (24 <= value && value <= 30) {
          color = "#FFA500";
        } else if (31 <= value) {
          color = "#FF0000";
        }

        document.getElementById("title").style.backgroundColor = color;
      }
    </script>
  </body>
</html>
"""