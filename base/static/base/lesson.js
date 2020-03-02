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
    }
}

lessonSocket.onclose = e => {
    console.error("lessonSocket closed unexpectedly");
}

const editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
    lineNumbers: true
});

$("#runCode").click(() => {
    const code = editor.getValue();
    lessonSocket.send(JSON.stringify({
        type: "RUN_CODE",
        code: code
    }))
});

const terminal = new Terminal();
const fitAddon = new FitAddon.FitAddon();
let attachAddon = null;

let terminalSocket = null;

terminal.open(document.getElementById("terminal"))
terminal.loadAddon(fitAddon);

const terminalSocketOpen = e =>  {
    attachAddon = new AttachAddon.AttachAddon(terminalSocket);
    terminal.loadAddon(attachAddon);
    //terminal.paste("\n");
    console.log("TERMINAL COMPLETED");
}

window.onresize = event => {
    fitAddon.fit();
}
