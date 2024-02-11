function read_entry(option) {
    window.location.href="/" + option.id;
}
function delete_entry(id) {
    window.location.href="/delete/" + id;
}
function searchMonth() {
	document.getElementById("select-month-form").submit();
}