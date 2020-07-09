$(document).ready(function() {
  let customId = $('#idagt').val();
  let options = {
    parentNode: document.querySelector('#meet'),
    roomName: `oml_videocall/${customId}`
  };

  let api, 
  domain = "marcelo";//aca especificar el dominio de jitsi meet
  let videoCallTrigger = $('#initMeeting');
  let videoCallContainer = $('#modalVideoCall');

  videoCallTrigger.click(function() {
    api = new JitsiMeetExternalAPI(domain, options);
    videoCallContainer.modal('show');
  });

  videoCallContainer.on('hidden.bs.modal', function() {
    api = null;
    $('#meet').empty();
  });
});