/* Adapted from https://stackoverflow.com/a/63097563/1937033 
   3 following functions: How to get the range from the selection, even when the selection extends on
   several differents elements (like differents <p>) */
function walkRange(range) {
    let ranges = [];
    
    let el = range.startContainer;
    let elsToVisit = true;
    while (elsToVisit) {
        let startOffset = el == range.startContainer ? range.startOffset : 0;
        let endOffset = el == range.endContainer ? range.endOffset : el.textContent.length;
        let r = document.createRange();
        r.setStart(el, startOffset);
        r.setEnd(el, endOffset);
        ranges.push(r);
        
        /// Move to the next text container in the tree order
        elsToVisit = false;
        while (!elsToVisit && el != range.endContainer) {
            let nextEl = getFirstTextNode(el.nextSibling);
            if (nextEl) {
                el = nextEl;
                elsToVisit = true;
            }
            else {
                if (el.nextSibling)      el = el.nextSibling;
                else if (el.parentNode)  el = el.parentNode;
                else                     break;
            }
        }
    }
    
    return ranges;
}

/* helper function for 'walkRange' */
/* Looping inside the selected node until we find the ultimate child containing text */
function getFirstTextNode(el) {
    /// Degenerate cases: either el is null, or el is already a text node
    if (!el)               return null;
	if (el.parentNode.className == 'webpage_done')	return null;
    if (el.nodeType == 3)  return el;
    
    for (let child of el.childNodes) {
        if (child.nodeType == 3) {
            return child;
        }
        else {
            let textNode = getFirstTextNode(child);
            if (textNode !== null) return textNode;
        }
    }
    
    return null;
}

function highlight(selObj, className) {
    range = selObj.getRangeAt ? selObj.getRangeAt(0) : selObj;
	// Check that the selected text contains at least 10 characters:
	range_text = range.toString();
	if (range_text.length > 10){
		for (let r of walkRange(range)) {
			let mark = document.createElement('span');
			mark.className = className;
			r.surroundContents(mark);
		}
		return true;
	} else 
	{ return false;}
}

/* Putting the split words inside the frame */
$(document).ready(function(e) {

	var iframe= document.getElementById('thewebpage');

	// Wait that the iframe has loaded completely the srcdoc inside
	iframe.addEventListener('load', function (e) { 
	
		// find the location where we'll put the split words
		var idoc= iframe.contentDocument || iframe.contentWindow.document;	
		var iframe_spans = $(idoc).find('.webpage_done');
		
		// moving each split words inside the correct location in the frame
		var words_inthistext = $('.words_inthistext');
		$.each(iframe_spans, function(indx, iframe_span){
			iframe_span = $(iframe_span);
			var section_nb= iframe_span.data('webpagesection');
			var words_inthistext_webpagesection = words_inthistext.find('.words_inthistext_webpagesection_'+section_nb.toString());

			// Copy the split words inside the webpage sections:
			iframe_span.html(words_inthistext_webpagesection.html());

			// display the hovering tooltip 
			var span_woids = iframe_span.find('span[woid]');
			$.each(span_woids, function() { 
				update_title($(this), $(this).attr('iscompoundword'), $(this).attr('wowordtext'), 
					$(this).attr('wotranslation'), $(this).attr('woromanization'), $(this).attr('wostatus'), 
					$(this).attr('cowordtext'), $(this).attr('cowotranslation'), $(this).attr('coworomanization'), 
					$(this).attr('cowostatus'), $(this).attr('show_compoundword'));

				$(this).bind('click', clickword);
			});
		});
		
		// Reading a webpage: trying to get the selected word inside the iframe:
		var DOCUMENT = $(iframe.contentWindow.document);	
		window.DOCUMENT = DOCUMENT;
		var sel_word = $(idoc).find('span[wostatus="0"]:not([show_compoundword="True"][cowostatus!="0"])').first(); 
		initialize_to_selectedword(sel_word, e);

		// Bind the key events to the frame
		key_binding(e);
		
		update_workcount(); 
		
		// bind the mouse release to fetching the highlighted text
		$("iframe#thewebpage").contents().mouseup(function() {
			var selObj = idoc.getSelection();
			var is_big_enough = highlight(selObj, 'webpage_seltext');
			if (is_big_enough){
			var iframe_html = idoc.documentElement.outerHTML;
			$('<div></div>').appendTo('body')
			.html(gettext('"LingLibrify" this text of the webpage?'))
			.dialog({
				modal: true,
				title: gettext('LingLibrify'), zIndex: 10000, autoOpen: true,
				width: 'auto', resizable: false,
				buttons: [{text: gettext("Yes"),
							click: function() {
								$.ajax({
									  type: "POST",
									  url: '/webpage_read/',
									  data: {'iframe_html':iframe_html, 'csrfmiddlewaretoken': window.CSRF_TOKEN,
											'text_id':TID},
									  success: function(){
											document.location='/webpage_read/'+TID;	
										}
									});
								}
							},
							{text: gettext("Cancel"),
							click: function() {
								  $( this ).dialog( "close" );}
							}
				],
				close: function (event, ui) {
					$(this).remove();
				},
			   // position: {my: "center",  at: "center", of: $("body"),within: $("body") }
			}); // end of '.dialog'
			} // end of if(is_big_enough)
		});// end of 'mouseup'
		
	});
						
 


}) // end of 'document.ready'

	
