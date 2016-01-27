$('form#multi-delete').submit(function () {
	var appliancesList = [];
	$('input.checkthis').each(function () {
		if (this.checked){
			appliancesList.push($(this).val())
		}
	})
	$('form#multi-delete input[name="appliance_id"]').val(JSON.stringify(appliancesList));
});