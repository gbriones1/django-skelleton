var backupAction = $('#backupform input[name="action"]');
var backupForm = $('#backupform');
var backupSelect = $('select[name="backups"]');

$(document).on('click', '#backupform button', function (e) {
	if ($(e.target).attr("id") == "backup"){
		backupAction.val("CREATE");
		backupForm.submit();
	}
	else if($(e.target).attr("id") == "send"){
		backupAction.val("SEND");
		backupForm.submit();
	}
	else if($(e.target).attr("id") == "restore-btn"){
		$('#restore form input[name="backup"]').val(backupSelect.val());
		$('#restore .modal-title').text(backupSelect.find(":selected").text());
	}
	else if($(e.target).attr("id") == "delete-btn"){
		$('#delete form input[name="backup"]').val(backupSelect.val());
		$('#delete .modal-title').text(backupSelect.find(":selected").text());
	}
	else{
		console.log("Unknown command");
	}
});