/*--------------------------------------------------------------------------------------------- Answer */
function Init(answer) {
    var obj = new Object();
    switch (answer) {
        case 1:
            {
                obj.Second = 40;
                obj.Minute = 1;
                obj.Step = 1;
            }; break;
        case 2:
            {
                obj.Second = 20;
                obj.Minute = 1;
                obj.Step = 2;
            }; break;
        case 3:
            {
                obj.Second = 60;
                obj.Minute = 0;
                obj.Step = 3;
            }; break;
        case 4:
            {
                obj.Second = 40;
                obj.Minute = 0;
                obj.Step = 4;
            }; break;
        case 5:
            {
                obj.Second = 20;
                obj.Minute = 0;
                obj.Step = 5;
            }; break;
    };
    return obj;
}

/* Paint Progress Bar */

function paintProgressBar(progress, step, second, max, postBack) {
    var hndl = setInterval(function () {
        var w = $(progress).width();
        if (w == max) { clearInterval(hndl); return; }
        w += step;
        $(progress).width(w);
        postBack();
    }, second);
}


function computePixel(size, second) {
    var oneSecond = size / second;
    return (oneSecond * 100) / 1000;
}