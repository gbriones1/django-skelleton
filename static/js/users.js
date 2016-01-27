$('form#multi-delete').submit(function () {
	var userList = [];
	$('input.checkthis').each(function () {
		if (this.checked){
			userList.push($(this).val())
		}
	})
	$('form#multi-delete input[name="user_id"]').val(JSON.stringify(userList));
});