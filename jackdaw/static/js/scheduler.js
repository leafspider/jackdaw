   
        function removeEvents(date_st) {
            calendar.getEvents().forEach(event => {
                event_date = event.startStr.slice(0, 10);
                if (event_date === date_st) {
                    event.remove();
                }
            });            
        }

        function eventsByDateName(date_st, name) {
            var events = [];
            calendar.getEvents().forEach(event => {
                event_date = event.startStr.slice(0, 10);
                // console.log(event_date, date_st);
                if (event_date === date_st && event.title == name) {
                    events.push(event);
                }
            });            
            return events;
        }

        async function getAllBookedSlots(date_st, includeAddress=false) {

            the_date = new Date(date_st + 'T00:00:00').getTime();
            today = new Date().setHours(0,0,0,0);

            if ( the_date < today ) { return; }   // Forget the past

            var url = "/scheduler-all-booked-slots?date=" + date_st;
            axios.get(url)
            .then( function (response) {
                var data = response.data;
                // console.dir(data);
                for(slot of data.slots) {
                    
                    slot_start = new Date(slot.start_time).getTime();
                    if ( slot_start < today ) { continue; } // Forget the past
                    
                    if (includeAddress) {
                        the_title = slot.name + " : " + slot.address;
                    } 
                    else {
                        the_title = slot.name;
                    }
                    the_event = {
                        title: the_title,
                        start: slot.start_time,
                        end: slot.end_time,
                        allDay: false
                    }
                    weekCalendar.addEvent(the_event);
                };

                window.allSlots = data.slots;

                showDay(date_st);
                for(slot of data.slots) {
                    the_event = {
                        title: slot.name + " : " + slot.address,
                        start: slot.start_time,
                        end: slot.end_time,
                        allDay: false
                    }
                    dayCalendar.addEvent(the_event);
                }
            });
        }

        function getBookedSlots(date_st, the_name) {

            removeEvents(date_st);

            the_date = new Date(date_st + 'T00:00:00').getTime();
            today = new Date().setHours(0,0,0,0);

            if ( the_date < today ) { 
                // console.log("Forget the past." );
                return; 
            }

            var url = "/scheduler-booked-slots?date=" + date_st + "&name=" + the_name;
            axios.get(url)
            .then( function (response) {
                var data = response.data;
                // console.dir(data);
                for(slot of data.slots) {
                    calendar.addEvent({
                        title: slot.name,
                        start: slot.start_time,
                        end: slot.end_time,
                        allDay: false
                    });
                };

                me_today = eventsByDateName(date_st, nameInput.value)

                if ( me_today.length > 0 ) {
                    document.getElementById('response').innerHTML = 'You have an appointment on ' + date_st;              
                    // msgPopup.close();          
                }
                else {
                    getAvailableSlots(date_st);
                }
            });
        }

        function getAvailableSlots(date_st) {

            document.getElementById('popup-text').innerHTML = 'Checking appointments...';   
            msgPopup.showModal();

            the_date = new Date(date_st + 'T00:00:00').getTime();
            today = new Date().setHours(0,0,0,0);

            if ( the_date < today ) { 
                console.log("Nothing available in the past." );
                return; 
            }

            var url = "/scheduler-available-slots?date=" + date_st + "&duration=" + durationInput.value + "&name=" + nameInput.value + "&address=" + addressInput.value;
            axios.get(url)
            .then( function (response) {
                var data = response.data;
                for(slot of data.slots) {
                    calendar.addEvent({
                        title: slot.name,
                        start: slot.start_time,
                        end: slot.end_time,
                        allDay: false
                    });
                };
                document.getElementById('response').innerHTML = (data.status == 'ok') ? '' : data.status;
                msgPopup.close();                  
            });
        }

