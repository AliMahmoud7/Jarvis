$(function () {
    // Change active class
    $(".nav li").removeClass("active");
    $('#text_chat').addClass('active');

    var chatBox = $('#chatbox');
    var userInput = $('#usermsg');
    var userMsg = $('<div></div>').addClass('chat-msg right-msg').attr('dir', 'auto');
    var serverMsg = $('<div></div>').addClass('chat-msg left-msg').attr('dir', 'auto');
    var chatWaiting = $('<div><span></span><span></span><span></span></div>').addClass('chat-waiting');
    var focusedElem = $('<a href="#" style="display: block; clear: both; padding-top: 15px; cursor: default;"></a>').attr('id', 'focused_elem');

    $('#text_form').submit(function (e) {
        e.preventDefault();  // stop submit the form

        var InputValue = userInput.val();
        var newUserMsg = userMsg.clone();
        var newServerMsg = serverMsg.clone();

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

            $('#focused_elem').focus();
            console.log(res);

            userInput.focus();

        }).fail(function (err) {
            newServerMsg.remove();
            // newServerMsg.empty().text('An unexpected error has occurred on the server!');
            console.log(err);
        });

        userInput.focus();

    });
});
