/**************************************************************
"Learning with Texts" (LWT) is free and unencumbered software 
released into the PUBLIC DOMAIN.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a
compiled binary, for any purpose, commercial or non-commercial,
and by any means.

In jurisdictions that recognize copyright laws, the author or
authors of this software dedicate any and all copyright
interest in the software to the public domain. We make this
dedication for the benefit of the public at large and to the 
detriment of our heirs and successors. We intend this 
dedication to be an overt act of relinquishment in perpetuity
of all present and future rights to this software under
copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE 
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
THE SOFTWARE.

For more information, please refer to [http://unlicense.org/].
***************************************************************/

/**************************************************************
Check for unsaved changes when unloading window
***************************************************************/

var DIRTY = 0;

function askConfirmIfDirty(){  
	if (DIRTY) { 
		return '** You have unsaved changes! **'; 
	}
}

function makeDirty() {
	DIRTY = 1; 
}

function resetDirty() {
	DIRTY = 0; 
}

function tagChanged(event, ui) {
	if (! ui.duringInitialization) DIRTY = 1;
	return true;
}

$(document).ready( function() {
	$('#termtags').tagit({afterTagAdded: tagChanged, afterTagRemoved: tagChanged});
	$('#texttags').tagit({afterTagAdded: tagChanged, afterTagRemoved: tagChanged}); 
	$('input,checkbox,textarea,radio,select').bind('change',makeDirty);
	$(':reset,:submit').bind('click',resetDirty);
	$(window).bind('beforeunload', askConfirmIfDirty);
} ); 
