let chatBox = $('#chatbox');
let userInput = $('#usermsg');
let userMsg = $('<div></div>').addClass('chat-msg right-msg').attr('dir', 'auto');
let serverMsg = $('<div></div>').addClass('chat-msg left-msg').attr('dir', 'auto');
let chatWaiting = $('<div><span></span><span></span><span></span></div>').addClass('chat-waiting');
const focusedElem = $('<a href="#" style="display: block; clear: both; padding-top: 20px; cursor: default;"></a>').attr('id', 'focused_elem');

$('#text_form').submit(function (e) {
    e.preventDefault();  // stop submit the form

    const InputValue = userInput.val();
    const newUserMsg = userMsg.clone();
    const newServerMsg = serverMsg.clone();

    chatBox.append(newUserMsg.text(InputValue));
    // newUserMsg.scrollTop(newUserMsg[0].scrollHeight);
    userInput.val('');  // .removeAttr('value');

    chatBox.append(newServerMsg.append(chatWaiting));
    chatBox.append(focusedElem);
    $('#focused_elem').focus();

    $.ajax({
        type: 'POST',
        url: '/text',
        contentType: 'text/plain; charset: UTF-8',
        data: InputValue,
        dataType: 'text'
    }).done(function (res) {
        // chatWaiting.remove();
        newServerMsg.empty();
        newServerMsg.text(res);
        // userInput.focus();
        console.log(res);

    }).fail(function (err) {
        newServerMsg.remove();
        console.log(err);
    });

    userInput.focus();

});
