
function populate(counter,machid,against) {
    $('input[name=machid]').val(machid);
    $('#machname').text($('#'+counter+'mach').text());
    $('#odds').text($('#'+counter+'odds').text());
    $('#rodds').text($('#'+counter+'rodds').text());
    $('#odds').show();
    $('#rodds').hide();
    $('#against').hide();
    if (against && $('#position').is(":checked")) {
        $('#position').trigger('click');
    }
    if (!against && !$('#position').is(":checked")) {
        $('#position').trigger('click');
    }
    if ($('#position').is(":checked")) {
        $('#odds').show();
        $('#rodds').hide();
        $('#against').hide();
    } else {
        $('#odds').hide();
        $('#rodds').show();
        $('#against').show();
    }
}
function calcpayout() {
    if ($("#position").is(':checked')) {
        $('#payoutval').text($('#odds').text() * $("#pinbucks").val());
    } else {
        $('#payoutval').text($('#rodds').text() * $("#pinbucks").val());
    }
}


function processBet(data,i){
    var idx=i+1;
    $("#"+idx+"time").text(data.at_time);
    $("#"+idx+"comment").text(data.comment);
    if (data.position) {
        $("#"+idx+"machine").text(data.machine + " at " + data.at_odds + ":1");
    } else {
        $("#"+idx+"machine").text("Against " + data.machine + " at " + data.at_odds + ":1");
    }
    $("#"+idx+"user").text(data.user);
}

function process(data) {
    for (var idx=0; idx<data.bets.length; ++idx) {
        processBet(data.bets[idx],idx);
    }
}

