$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})
$(document).ready(function () {
    $("h1,h2,h3,h4").each(function (i) {
        var heading = $(this);
        var headingId = heading.text().trim().toLowerCase().replace(/\s/g, '_')
        heading.attr("id", headingId);
        heading.append("<a class='heading-link' href='#" + headingId + "'><div id='anchor-icon'>&#160;&#35;</div></a>");
    });
    var url = window.location.href
    var id_in_url = url.substring(url.lastIndexOf('#') + 1);
    if (id_in_url) {
        document.getElementById(id_in_url).scrollIntoView({
            behavior: 'smooth'
        });
    }
})