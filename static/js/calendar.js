        window.onload = function () {
            year();
            month();
            for (var j = 1; j <= 31; j++) {
                var optday = window.document.createElement("option");
                optday.value = j;
                optday.innerHTML = j;
                document.getElementById("SelectDay").appendChild(optday);
            }
        }
        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth() + 1;
		var yy = today.getFullYear();
		
        function year() {
            for (var i = yy; i <= (yy+4); i++) {
                var optyear = window.document.createElement("option");
                optyear.value = i;
                optyear.innerHTML = i;
                document.getElementById("SelectYear").appendChild(optyear);
            }
        }
            function month() {
                for (i = 1; i <= 12; i++) {    
                    var opt = window.document.createElement("option");
                    opt.value = i;
                    opt.innerHTML = i;
                    document.getElementById('SelectMonth').appendChild(opt);
                }
            }
            function day() {
                var k =31;
                switch (currentmonth) {
                    case "1":
                    case "3":
                    case "5":
                    case "7":
                    case "8":
                    case "10":
                    case "12":
                        k = 31;
                        break;
                    case "4":
                    case "6":
                    case "9":
                    case "11":
                        k = 30;
                        break;
                    case "2":
                        if (currentyear % 4 == 0) {
                            k = 29;
                        }
                        else {
                            k = 28;
                        }
                        break; 
                }
                for (var j = 1; j <= k; j++) {
                    var optday = window.document.createElement("option");
                    optday.value = j;
                    optday.innerHTML = j;
                    document.getElementById("SelectDay").appendChild(optday);
                }
            }
            function chooseYear() {
                currentyear = document.getElementById("SelectYear").value;
                display();
                delDay();
                day();
            }
            function chooseMonth() {
                currentmonth = document.getElementById("SelectMonth").value;
                display();
                delDay();
                day();
            }
            function delDay() {
                var del = document.getElementById("SelectDay");
                while(del.hasChildNodes()){                   
                    del.removeChild(del.firstChild);
                }
            }
            function chooseDay() {
                currentday = document.getElementById("SelectDay").value;
                display();
            }
            function display(){
                var year = document.getElementById("year").innerHTML = document.getElementById("SelectYear").value;
                var month = document.getElementById("month").innerHTML = document.getElementById("SelectMonth").value;
                var day = document.getElementById("day").innerHTML = document.getElementById("SelectDay").value;
            }