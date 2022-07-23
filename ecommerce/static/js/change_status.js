$(document).ready(function () {
    $('.sopt').change(function (e) {
        var optionSelected = $("option:selected", this)
        var text = optionSelected.text()
        this_li = $(this).parent().parent()
        if (text != 'تغییر وضعیت') {
            $(this_li).children().eq(1).text('وضعیت: ' + text)
            index_li = $("ol").children().index($(this_li))

            $.ajax({
                type: 'POST',
                url: URL,
                data: {
                    'csrfmiddlewaretoken': CSRF_TOKEN,
                    'cart_index': index_li,
                    'value': optionSelected.val()
                },
                success: function () {
                    console.log('Success!')
                }
            })
        }
    });
})