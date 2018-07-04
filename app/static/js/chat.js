let chatBox = $('#chatbox');
let userInput = $('#usermsg');
let userMsg = $('<div></div>').addClass('chat-msg left-msg');

$('#text_form').submit(function (e) {
    e.preventDefault();  // stop submit the form
    // userMsg.empty();

    const InputValue = userInput.val();
    chatBox.append(userMsg.clone().text(InputValue));
    userInput.val('');  // .removeAttr('value');

    $.ajax({
        type: 'POST',
        url: '/text',
        contentType: 'text/plain; charset: UTF-8',
        data: InputValue,
        dataType: 'text'
    }).done(function (res) {
        console.log(res);
    }).fail(function (err) {
        console.log(err);
    });


});