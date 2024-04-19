console.log("Hello world!")

const ws = new WebSocket("ws://localhost:8080") // Виконуємо з'єднання до веб-сокету:

formChat.addEventListener("submit", (e) => {
    e.preventDefault()
    ws.send(textField.value)
    textField.value = null
})

ws.open = (e) => {
    console.log("Hello Websocket!")
}

ws.onmessage = (e) => {
    console.log(e.data)
    text = e.data

    //var subscribe = document.getElementById('subscribe')

    const elMsg = document.createElement("div")
    elMsg.textContent = text
    subscribe.appendChild(elMsg)
}

