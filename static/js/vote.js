console.log("Here");

$('.js-vote').click(function(ev){
	ev.preventDefault();
	var $this = $(this),
		action = $this.data('action'),
		qid = $this.data('qid');
	$.ajax('/vote/',{
		method: 'POST',
		data: {
			action: action,
			qid: qid
		},
	}).done(function(data){
		var success = data['success'];
		if (success){
			elem = document.getElementById(qid);
			elem.value = data['response'];
		}


	});
});