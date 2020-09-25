$(document).ready(function() {

    searchBtn = $('#search-btn')
    resultsContainer = $('#available-rooms')
    resultsList = $('#available-rooms-list')
    checkIn = $('#checkin-input')
    checkOut = $('#checkout-input')
    guests = $('#guest-input')
    bookingFormModal = $('#booking-form-modal')
    bookingBtn = $('#booking-btn')

    validCheckIn = false
    validCheckOut = false

    msgEmptyDates = "Introduzca fecha de entrada y salida"
    msgErrorDates = "La fecha de entrada debe ser anterior a la fecha de salida"
    msgErrorEmptyInput = "El campo no puede estar vacío"
    msgErrorInvalidEmail = "El email introducido no es válido"

    searchBtn.popover({
        trigger: 'focus',
        content: msgEmptyDates
    })

    // Check and handle the checkin input to show possible error messages
    checkIn.change(function() {
        changePopoverContent(msgEmptyDates)
        searchBtn.popover('enable')
        validCheckIn = false

        if ($(this).val() != '') {
            validCheckIn = true
            if (checkOut.val() != '') {
                if (validDates()) {
                    searchBtn.popover('disable')
                    validCheckIn = true
                } else {
                    changePopoverContent(msgErrorDates)
                    validCheckOut = false
                }
            }
        }
    })

    // Check and handle the checkout input to show possible error messages
    checkOut.change(function() {
        changePopoverContent(msgEmptyDates)
        searchBtn.popover('enable')
        validCheckOut = false

        if ($(this).val() != '') {
            validCheckOut = true
            if (checkIn.val() != '') {
                if (validDates()) {
                    searchBtn.popover('disable')
                    validCheckOut = true
                } else {
                    changePopoverContent(msgErrorDates)
                    validCheckIn = false
                }
            }
        }
    })

    // Search available rooms
    searchBtn.click(function() {
        resultsList.css('display', 'block')
        $('#no-available-rooms-alarms').css('display', 'none')

        if (validCheckIn && validCheckOut) {
            $(this).addClass('disabled')
            $('#loading-btn').css('display', 'inline-block')

            // Clean the result list. 1 item list is left to use it as template
            resultsList.children('li:not(:first-child)').remove()

            $.ajax({
                type: 'POST',
                dataType: 'json',
                async: false,
                url: '/hotelBooking/search/',
                data: {
                    'checkin': checkIn.val(),
                    'checkout': checkOut.val(),
                    'guests': guests.val(),
                    'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
                },
                success: function(results) {
                    console.log(results)
                    if (results.data.length == 0 || results.data.rooms.length == 0) {
                        resultsList.css('display', 'none')
                        $('#no-available-rooms-alarms').css('display', 'block')
                    }

                    // Render results
                    if (results.data.length != 0) {
                        results.data.rooms.forEach(function(item, index) {
                            itemList = resultsList.children('li')
                            if (index != 0) {
                                // The rest of results will be appended
                                itemList = resultsList.children('li:first').clone()
                            }

                            itemList.children('div').children('.type-room-result').
                            children('span').text(item.type_room)
                            itemList.children('div').children('.available-rooms-result').
                            children('span').text(item.available_rooms)
                            itemList.children('div').children('.total-price-result').
                            children('span').text(item.total_price_view)

                            itemList.children('div').children('.select-room-btn').children('button').
                            attr('chosen-type-room', item.id_type_room)
                            itemList.children('div').children('.select-room-btn').children('button').
                            attr('chosen-total-price', item.total_price)

                            // First result is already shown
                            if (index != 0) {
                                itemList.appendTo(resultsList)
                            }
                        })
                    }

                    // load data into modal form
                    $('#checkin-booking').val(results.data.checkin)
                    $('#checkout-booking').val(results.data.checkout)
                    $('#guests-booking').val(results.data.guests)

                    $('#checkin-modal').val(results.data.checkin_view)
                    $('#checkout-modal').val(results.data.checkout_view)
                    $('#guests-modal').val(results.data.guests)
                    $('#duration-modal').text(results.data.duration)

                    resultsContainer.collapse('show')
                    searchBtn.removeClass('disabled')
                    $('#loading-btn').css('display', 'none')
                },
                error: function(request, status, error) {
                    console.log(status)
                    console.log(error)
                }
            })
        }
    })

    // Select a room for booking 
    resultsList.on('click', 'button', function() {
        dataContent = $(this).parent().parent()

        // End of loading data in modal form
        typeRoom = dataContent.children('.type-room-result').text().toLowerCase()
        totalPriceCurrency = dataContent.children('.total-price-result').text()

        $('#type-room-modal').text(typeRoom)
        $('#total-price-modal').text(totalPriceCurrency)

        idTypeRoom = dataContent.children('.select-room-btn').
        children('button').attr('chosen-type-room')
        totalPrice = dataContent.children('.select-room-btn').
        children('button').attr('chosen-total-price')

        $('#type-room-booking').val(idTypeRoom)
        $('#total-price-booking').val(totalPrice)

        bookingFormModal.modal()
    })

    // Booking process
    $('#booking-btn').click(function(e) {
        e.preventDefault()

        validName = true
        validEmail = true
        validPhone = true

        // Validate data input 
        if ($('#name-booking').val().trim() == '') {
            $('#name-error').text(msgErrorEmptyInput)
            $('#name-error').css('display', 'block')
            validName = false
        }
        if ($('#email-booking').val().trim() == '') {
            $('#email-error').text(msgErrorEmptyInput)
            $('#email-error').css('display', 'block')
            validEmail = false
        }
        if ($('#phone-booking').val().trim() == '') {
            $('#phone-error').text(msgErrorEmptyInput)
            $('#phone-error').css('display', 'block')
            validPhone = false
        }
        if (!validateEmail($('#email-booking').val().trim())) {
            $('#email-error').text(msgErrorInvalidEmail)
            $('#email-error').css('display', 'block')
            validEmail = false
        }

        // Create data to save the booking
        if (validName && validEmail && validPhone) {
            data = {
                'checkin': $('#checkin-booking').val(),
                'checkout': $('#checkout-booking').val(),
                'type_room': $('#type-room-booking').val(),
                'guests': $('#guests-booking').val(),
                'name': $('#name-booking').val(),
                'email': $('#email-booking').val(),
                'phone': $('#phone-booking').val(),
                'price': $('#total-price-booking').val(),
                'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
            }

            $.ajax({
                type: 'POST',
                dataType: 'json',
                async: false,
                url: '/hotelBooking/create_booking/',
                data: data,
                success: function(results) {
                    $('#booking-code').text(results.data)
                    $('#success-booking-alert').css('display', 'block')
                },
                error: function(request, status, error) {
                    console.log(status)
                    console.log(error)
                }
            })
        }

    })

    // Clean error message after insert something in the input
    $('#name-booking, #email-booking, #phone-booking').keydown(function() {
        $(this).parent().children('small').text('')
    })

    // Handle closing modal
    bookingFormModal.on('hidden.bs.modal', function(e) {
        // Do redirect if there is a booking code on modal
        if ($('#booking-code').text() != '') {
            window.location.replace("/hotelBooking/bookings")
        }
    })

    // Change the popover content used to show error messages (validation)
    function changePopoverContent(content) {
        searchBtn.attr('data-content', content)
        var popover = searchBtn.data('bs.popover')
        popover.setContent()
    }

    // Check if dates input have good values (checkin < checkout)
    function validDates() {
        if (checkIn.val() != '' && checkOut.val() != '') {
            inDate = new Date(checkIn.val())
            outDate = new Date(checkOut.val())
            if (inDate < outDate) {
                return true
            }
        }
        return false
    }

    // Check if email is valid
    function validateEmail(email) {
        const re = /^(([^<>()\[\]\\.,:\s@"]+(\.[^<>()\[\]\\.,:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        return re.test(String(email).toLowerCase())
    }

})