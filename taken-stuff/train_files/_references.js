/// <reference path="jquery-1.7.1.js" />
/// <reference path="jquery-ui-1.8.20.js" />
/// <reference path="jquery.validate.js" />
/// <reference path="jquery.validate.unobtrusive.js" />
/// <reference path="knockout-2.1.0.debug.js" />
/// <reference path="modernizr-2.5.3.js" />


/* Для перехода в страницам */
var rederict = function (url) {
    window.location.href = url;
}

function postBack(url) {
    window.location = url;
}

/* Для перехода по */
function ShortInterval(page, item, sec, mm, action) {
    var second = sec;
    var minute = mm;

    var temp = setInterval(function () {
        if (second == 0) {
            action(page);
            clearInterval(temp);
        }

        $(item).text(minute + (second--));
    }, 1000);
}


/* Функция для отсчета времени 1:30 */
function LongInterval(page, item, sec, mm, state) {
    var second = sec;
    var minute = mm;
    var stateSecond = state;

    setInterval(function() {
        if (stateSecond == 60) {
            $(item).text(minute + ":00");
            minute = "00";
            second = stateSecond = 59;
            return;
        }

        // Rederict
        if (second == 0) {
            rederict(page);
        }

        if (second < 10)
            $(item).text(minute + ":0" + (second--));
        else
            $(item).text(minute + ":" + (second--));
        --stateSecond;
    }, 1000);
}


/* Функция для отсчета N секунд */

function TimeRederict(time, reference) {
    var second = 0;
    setInterval(function () {
        ++second;
        if (second == time)
            rederict(reference);
    }, 1000);
};

/*Toolpit*/
function Help(item) {
    $('.tooltip').tooltipster();
}

/*Скрыть*/
function Hide(item) {
    $(item).hide();
}

/**/
function Mouse(item, node) {
    $(item).mouseover(function () {
        $(node).show("slow");
    });

    $(item).mouseout(function () {
        $(node).hide("slow");
    });
}

/* Проверка элементов на совпадение*/

function Any(items, action) {
    for (var i = 0; i < items.length; i++) {
        if (action(items[i])) return true;
    }
    return false;
}


//Включаем и выключаем элементы
function DisableItem(item, flag) {
    if (flag)
        $(item).show();
    else
        $(item).hide();
}

/*Воспроизводит музыкальный файл */

// Play
function playerMusic(item) {
    if (item.played.length == 0) {
        item.play();
        return 0;
    }
    else {
        var temp = item.played.length;
        item.load();
        return 1;
    }
}



// Stop
function stopMusic(item) {
    if (item.played.length == 1) {
        item.load();
        return 1;
    }
    return 0;
}



/* Новый Таймер */

function SpeedTimer(minute, second, value, action, view) {
    var min = -1;
    if (second == -1) {
        second = 59;
        minute = 1;
    } else {
        if (value != -2) {
            if (second >= value) min = second - value;
            if (second < value) {
                min = 60 - value;
                second = 59;
            }
        }
    }

    return setInterval(function() {
        --second;
        if (second == min) action();
        if (second == -1) {
            if (minute == 0) {
                action();
                return;
            }

            $(view).text("0" + minute + ":" + "0" + second);

            --minute;
            second = 59;
        }

        if (minute < 0) action();
        if (second < 10) {
            if (minute == 0)
                $(view).text("00:" + "0" + second);
            else
                $(view).text("0" + minute + ":" + "0" + second);
        } else {
            if (minute == 0)
                $(view).text("00:" + second);
            else
                $(view).text("0" + minute + ":" + second);
        }
    }, 1000);
}



/* Для подсказок  */
function locationModal(item) {
    var w = window.screen.width;
    item.css('margin-left', (w / 2) - (item.width() / 2));
    
    $("#cancel").click(function () {
        $('#modal').animate({ opacity: 0, top: '45%' }, 200,  // плавно меняем прозрачность на 0 и одновременно двигаем окно вверх
				function () {
				    $(this).css('display', 'none'); // делаем ему display: none;
				    $('#overlay').fadeOut(400);
				});
    });
}
