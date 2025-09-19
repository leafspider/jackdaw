
async function getData( task ) {
    console.log(task);
    addEllipsis(); 
    await newSocket( task );
    console.log("Done");
}

socket = null;

function createWebSocketConnection(url) {
    return new Promise((resolve, reject) => {
        socket = new WebSocket(url);
        
        socket.onopen = function(event) { 
            console.log('Connected to WebSocket');
        };

        socket.onmessage = function(response) {

            removeEllipsis();

            var data = response.data;
            console.log(data);

            var res = extractJson(data);

            var json = res[0];
            if ( json != null ) {
                var jid = 'chart' + Math.random();
                var jdiv = document.createElement('div');
                jdiv.id = jid;
                jdiv.classList.add('agent_chart');
                document.getElementById('history').appendChild(jdiv);
                Highcharts.chart(jid, json);
            }

            var text = res[1];
            if ( text != null ) {
                var id = 'speech' + Math.random();
                var div = document.createElement('div');
                div.id = id;
                div.classList.add('agent_speech');
                div.innerHTML = text;
                document.getElementById('history').appendChild(div);
            }

            addEllipsis();                

            window.scrollTo(0, document.body.scrollHeight);
        };

        socket.onclose = function(event) { 
            removeEllipsis();
            console.log('Disconnected from WebSocket'); 
        };

        socket.onerror = function(event) { 
            removeEllipsis();
            console.log('Error in WebSocket'); 
        };

        // socket.onopen = () => {
        //     console.log("WebSocket connected");
        //     resolve(socket);
        // };
        
        // socket.onerror = (error) => {
        //     console.error("WebSocket error:", error);
        //     reject(error);
        // };
    });
}

async function connectToWebSocket() {
    try {
        return await createWebSocketConnection('ws://localhost:8765');
        //socket.send("Hello, server!");
    } catch (error) {
        console.error("Failed to connect:", error);
    }
}

async function newSocket(task) {
    
    if (socket && socket.readyState !== WebSocket.CLOSED) {
        socket.close();
    }

    // socket = new WebSocket('ws://localhost:8765');    
    // socket = connectToWebSocket();
    socket = await createWebSocketConnection('ws://localhost:8765');

    // num = 0;
    // while( socket.readyState == WebSocket.CONNECTING ) { 
    //     console.log('Connecting');
    //     num++
    //     if ( num > 10 ) { break; }
    // }

    socket.send( task );
}


