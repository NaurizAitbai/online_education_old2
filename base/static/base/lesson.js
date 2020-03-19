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

// TODO: Рефакторинг
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

/*
    NEW CODE
*/

// Список интерактивных редакторов
const code_runners = {};

$(".code-runner").each((index, element) => {
    const code_name = element.dataset.code;

    const editor_element = $(element).children(".code-editor")[0];

    const editor = CodeMirror.fromTextArea(editor_element, {
        lineNumbers: true
    })

    code_runners[code_name] = {
        editor: editor,
        terminal: null
    }
});

// Показать/Скрыть интерактивную консоль
$(".toggle-terminal").click(event => {
    event.preventDefault();
    const toggle_element = event.target;
    const code_runner = $(toggle_element).parents('.code-runner')[0];
    const code_name = code_runner.dataset.code;

    const terminal_block = $(code_runner).children('.terminal-block')[0];

    if(terminal_block.dataset.hidden === "true") {
        terminal_block.dataset.hidden = false;
        $(terminal_block).removeClass("d-none");
        toggle_element.innerHTML = "Скрыть терминал";
    } else {
        terminal_block.dataset.hidden = true;
        $(terminal_block).addClass("d-none");
        toggle_element.innerHTML = "Показать терминал";
    }

    if (code_runners[code_name].terminal === null) {
        const terminal_element = $(terminal_block).children(".terminal-app")[0];
        const terminal = new Terminal();

        terminal.open(terminal_element);
        terminal.loadAddon(fitAddon);

        code_runners[code_name].terminal = {
            app: terminal,
            socket: null
        };
    }
});