

$(function() {
 
    //Variables to configure Plot.ly charts        
    var trace1 = {
        x: [[]], 
        y: [], 
        name: '', 
        type: ''
    };
    var data = [trace1];
    var layout = {
      showlegend: false,
      xaxis: {
        tickson: "boundaries",
        ticklen: 15,
        showdividers: true,
        dividercolor: 'grey',
        dividerwidth: 2
      }
    };
    var divID=0;
    //END Variables to configure Plot.ly charts 

    //Variables to configure speech synthesizer        
    var synth = window.speechSynthesis;
    var msg = new SpeechSynthesisUtterance();
    var voices = synth.getVoices();
    msg.voice = voices[0];
    msg.rate = 1;
    msg.pitch = 1;

    var onAnythingSaid = function (text) {
        //console.log('Interim text: ', text);
    };
    var onFinalised = function (text) {
        //console.log('Finalised text: ', text);
    $('#messageText').val(text);
    };
    var onFinishedListening = function () {
        // $('#chatbot-form-btn').click();
    };
    //END Variables to configure speech synthesizer

    $('#chatbot-form-btn').click(function(e) {
        e.preventDefault();
    $('#chatbot-form').submit();
    });
    $('#chatbot-form-btn-clear').click(function(e) {
        e.preventDefault();
    $('#chatPanel').find('.media-list').html('');
    });
    $('#chatbot-form-btn-voice').click(function(e) {
    e.preventDefault();
    try {
        var listener = new SpeechToText(onAnythingSaid, onFinalised, onFinishedListening);
        listener.startListening();

        setTimeout(function () {
            listener.stopListening();
            if ($('#messageText').val()) {
                $('#chatbot-form-btn').click();
            }
        }, 5000);
    } catch (error) {
        console.log(error);
        }
    });

    $('#chatbot-form').submit(function(e) {
        e.preventDefault();
        var message = $('#messageText').val();
        $(".media-list").append('<li class="media"><div class="media-body"><div class="media"><div style = "text-align:right; color : #2EFE2E" class="media-body">' + message + '<hr/></div></div></div></li>');
        //POST the chat message to the chatbot, get a response
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5001/ask",
            data: $(this).serialize(),
            success: function(response) {
            //Add a new div where Plot.ly can draw a plot
            divID=divID+1;
            result="";
            result+=response.answer;
            var result_json= JSON.parse(result);
            var result_key= Object.keys(result_json)[0];
            var json=Object.values(result_json)[0];
            console.log(Object.keys(result_json)[0]);
            console.log(Object.values(result_json)[0]);
            var help="";
            if(result_key=="help"){
                //Loop over all the various help passed in as JSON object
                //console.log("in help");
                for (var key in json) {
                   if (json.hasOwnProperty(key)) {
                        //Modify plot.ly parameters according to returned values
                        //console.log("hasownprop loop");
                        help+=json[key]+ ",";

                   }
                }
                console.log(help);
                result=help;
                
           }

            if(result_key=="stats"){
                //Loop over all the various stats passed in as JSON object
                trace1.name='Stats';
                trace1.type='bar';
                trace_item=0;
                for (var key in json) {
                   if (json.hasOwnProperty(key)) {
                        //Modify plot.ly parameters according to returned values
                        trace1.x[trace_item]=key;
                        trace1.y[trace_item]=json[key];
                        console.log(key);
                        console.log(json[key]);
                        trace_item+=1;
                   }
                }
                
                $(".media-list").append('<div id="myDiv'+divID+'"'+'> </div>');
                Plotly.newPlot('myDiv'+divID, data, layout, {showSendToCloud: true});
            }
            $('#messageText').val('');
            var answer = result;
            const chatPanel = document.getElementById("chatPanel");
            $(".media-list").append('<li class="media"><div class="media-body"><div class="media"><div style = "color : white" class="media-body">' + answer + '<hr/></div></div></div></li>');
            $(".fixed-panel").stop().animate({ scrollTop: $(".fixed-panel")[0].scrollHeight}, 1000);
            //Crop the message, so that speech doesnt go on too long
            msg.text = answer;
            var msg_short=msg.text.slice(0,50);
            msg.text = msg_short;
            //Synthesize message to speech
            speechSynthesis.speak(msg);
            },
            error: function(error) {
            //console.log(error);
            }
        });
    });
});
