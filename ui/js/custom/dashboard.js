$(function () {
    // Function to escape HTML special characters
    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // API call for order table
    $.get(orderListApiUrl)
        .done(function (response) {
            if (response) {
                var table = '';
                var totalCost = 0;
                $.each(response, function (index, order) {
                    totalCost += parseFloat(order.total);
                    table += '<tr>' +
                        '<td>' + escapeHtml(order.datetime) + '</td>' +
                        '<td>' + escapeHtml(order.order_id) + '</td>' +
                        '<td>' + escapeHtml(order.customer_name) + '</td>' +
                        '<td>' + parseFloat(order.total).toFixed(2) + ' Rs</td></tr>';
                });
                table += '<tr><td colspan="3" style="text-align: end"><b>Total</b></td><td><b>' + totalCost.toFixed(2) + ' Rs</b></td></tr>';
                $("table").find('tbody').empty().html(table);
            }
        })
        .fail(function () {
            alert("An error occurred while fetching order data.");
        });
});
