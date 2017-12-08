$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
      // do not show message anymore
    }

    // Updates the flash message area
    function flash_message(message) {
      $("#flash_message").empty();
      $("#flash_message").append(message);
    }

    // Updates the flash message area
    function clear_message(panel_id) {
      $(panel_id).hide();
    }

    // Updates the result message area
    function show_result(panel_id, table_id, res) {
      //alert(res.toSource())
      $(table_id).empty();
      $(panel_id).show();
      $(table_id).append('<table class="table-striped">');
      var header = '<tr>'
      header += '<th style="width:25%">ID</th>'
      header += '<th style="width:25%">First Name</th>'
      header += '<th style="width:25%">Last Name</th>'
      header += '<th style="width:25%">Credit Level</th>'
      header += '<th style="width:20%">Valid</th>'
      $(table_id).append(header);
      for(var i = 0; i < res.length; i++) {
          customer = res[i];
          var row = "<tr><td>"+customer.id+"</td><td>"+
                customer.firstname+"</td><td>"+customer.lastname+"</td><td>"+
                customer.credit_level+"</td><td>"+customer.valid+"</td><tr>";
          $(table_id).append(row);
      }

      $(table_id).append('</table>');

      flash_message("Success")
    }

    // ****************************************
    // Create a Customer
    // ****************************************

    $("#create-btn").click(function () {

        var first_name = $("#first_name_to_create").val();
        var category = $("#first_name_to_create").val();

        var data = {
            "firstname": first_name,
            "lastname": category,
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/customers",
            contentType:"application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            show_result("#create_panel","#create_results",[res])
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_message("#create_panel")
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Customer
    // ****************************************

    $("#update-btn").click(function () {

        var customer_id = $("#id_to_update").val();
        var firstname = $("#first_name_to_update").val();
        var lastname = $("#last_name_to_update").val();

        var data = {
            "firstname": firstname,
            "lastname": lastname,
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/customers/" + customer_id,
                contentType:"application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            show_result("#update_panel","#update_results",[res])
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_message("#update_panel")
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Customer
    // ****************************************

    $("#retrieve-btn").click(function () {

        var customer_id = $("#id_to_retrive").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/customers/" + customer_id,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            show_result("#retrieve_panel","#retrieve_results",[res])
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_message("#retrieve_panel")
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Customer
    // ****************************************

    $("#delete-btn").click(function () {

        var customer_id = $("#id_to_delete").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/customers/" + customer_id,
            contentType:"application/json",
            data: '',
        })

        ajax.done(function(res){
            flash_message("Customer with ID [" + res.id + "] has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Search for a Customer
    // ****************************************

    $("#search-btn").click(function () {

        var firstname = $("#first_name_to_search").val();
        var lastname = $("#last_name_to_search").val();

        var queryString = ""

        if (firstname) {
            queryString += 'firstname=' + firstname
        }

        if (lastname) {
            queryString += 'lastname=' + lastname
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/customers?" + queryString,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            show_result("#search_panel","#search_results",res);
        });

        ajax.fail(function(res){
            clear_message("#search_panel")
            flash_message(res.responseJSON.message)
        });

    });

})
