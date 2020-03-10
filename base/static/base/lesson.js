let lessonSocket = new WebSocket(`ws://${window.location.host}/ws/lesson/${lesson.id}/`);

lessonSocket.onopen = e => {
    lessonSocket.send(JSON.stringify({
        type: "READY",
    }));
}

lessonSocket.onmessage = e => {
    const json_data = JSON.parse(e.data);
    const data_type = json_data['type'];

    if (data_type === 'RUN_CODE') {
        terminalSocket = new WebSocket(`${json_data['terminal_url']}/containers/${json_data['container_id']}/attach/ws?logs=1&stream=1&stdin=1&stdout=1&stderr=1`);
        terminalSocket.onopen = terminalSocketOpen;
        $("#terminalMessageBlock").addClass("d-none");
        $("#runCode").removeClass('disabled');
        $("#runCode").addClass('d-none');
        $("#stopCode").removeClass('d-none');
    } else if(data_type === 'STOP_CODE') {
        $("#terminalLoading").addClass('d-none');
        $("#terminalMessage").removeClass('d-none');
        $("#terminalMessageBlock").removeClass('d-none');
        $("#stopCode").removeClass("disabled");
        $("#runCode").removeClass('d-none');
        $("#stopCode").addClass('d-none');
    } else if(data_type === 'FINISH_CODE') {
        $("#stopCode").removeClass("disabled");
        $("#runCode").removeClass('d-none');
        $("#stopCode").addClass('d-none');
    } else if (data_type === 'CHECK_CODE') {
        $("#resultLoading").addClass('d-none');
        if(json_data['result'] === true) {
            $("#resultSuccess").removeClass('d-none');
            $("#resultCloseButton").removeClass('d-none');
            $("#resultNextButton").removeClass('d-none');
        } else {
            $("#resultFail").removeClass("d-none");
            $("#resultCloseButton").removeClass('d-none');
            $("#failHelpText").html(json_data['help_text']);
        }
    }
}

lessonSocket.onclose = e => {
    console.error("lessonSocket closed unexpectedly");
}

$(".code-editor").each((index, element) => {
    CodeMirror.fromTextArea(element, {
        lineNumbers: true
    })
});

const editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
    lineNumbers: true
});

$("#runCode").click(() => {
    const code = editor.getValue();

    $("#terminalMessage").addClass("d-none");
    $("#terminalLoading").removeClass("d-none");
    $("#runCode").addClass('disabled');

    lessonSocket.send(JSON.stringify({
        type: "RUN_CODE",
        code: code
    }))
});

$("#stopCode").click(() => {
    $("#stopCode").addClass('disabled');

    lessonSocket.send(JSON.stringify({
        type: "STOP_CODE",
    }))
})

$("#checkCode").click(() => {
    const code = editor.getValue();
    $("#codeResultWindow").modal();
    lessonSocket.send(JSON.stringify({
        type: "CHECK_CODE",
        code: code
    }))
});

$("#helpCollapseButton").click(() => {
    $("#helpCollapse").collapse('toggle');
})

let terminal = new Terminal();
const fitAddon = new FitAddon.FitAddon();
let attachAddon = null;

let terminalSocket = null;

terminal.open(document.getElementById("terminal"))
terminal.loadAddon(fitAddon);

const terminalSocketOpen = e =>  {
    attachAddon = new AttachAddon.AttachAddon(terminalSocket);
    terminal.dispose();
    terminal = new Terminal();
    terminal.open(document.getElementById("terminal"));
    terminal.loadAddon(fitAddon);
    terminal.loadAddon(attachAddon);
    terminal.paste('\n');
}

window.onresize = event => {
    fitAddon.fit();
}

$("#codeResultWindow").on('show.bs.modal', function (e) {
    $("#resultLoading").removeClass('d-none');
    $("#resultSuccess").addClass('d-none');
    $("#resultFail").addClass('d-none');
    $("#resultCloseButton").addClass('d-none');
    $("#resultNextButton").addClass('d-none');
})