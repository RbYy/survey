$(document).ready(function(){
    $('.dicty-table > tr.add-row > td > a').hide()
    m2mWidget = $('.related-widget-wrapper')
    m2mWidget.addClass('hidden')
    showm2m = m2mWidget.after('<a class="show-groups">Show groups</a>')
    $('.field-groups').on('click', '.show-groups', function() {
        console.log('sss')
        $(this).prev().removeClass('hidden')
        $(this).replaceWith('<a class="hide-groups">Hide groups</a>')
    });
    $('.field-groups').on('click', '.hide-groups', function() {
        console.log('ddd')
        $(this).prev().addClass('hidden')
        $(this).replaceWith('<a class="show-groups">Show groups</a>')
    })
})

