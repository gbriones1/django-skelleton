$('form#multi-delete').submit(function () {
	var providerList = [];
	$('input.checkthis').each(function () {
		if (this.checked){
			providerList.push($(this).val())
		}
	})
	$('form#multi-delete input[name="provider_id"]').val(JSON.stringify(providerList));
});