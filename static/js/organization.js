$('form#multi-delete').submit(function () {
	var organizationList = [];
	$('input.checkthis').each(function () {
		if (this.checked){
			organizationList.push($(this).val())
		}
	})
	$('form#multi-delete input[name="organization_id"]').val(JSON.stringify(organizationList));
});