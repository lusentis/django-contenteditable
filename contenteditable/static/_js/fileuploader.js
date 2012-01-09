/* XMLHttpRequest2 file upload handler */

var Uploader = {};

Uploader._options = {
	'url': 'http://www.example.com/upload/',
	'droparea': undefined,
	'uploaderlist': undefined,
	'imagepreview': undefined,
	'multiple': true,
	'errorMessage': 'Si è verificato un errore durante il caricamento di uno o più files. Ricarica la pagina e riprova.',
	'progressHandler': function(evt) {
		//if (evt.lengthComputable) {
			$('#progress'+this._id).html(""+(evt.loaded / evt.total * 100));
		//}
	},
	'loadHandler': function(evt) {
		if (this.response.trim() != 'ok') {
			alert(Uploader._options.errorMessage);
			document.location.reload();
			return false;
		}

		$('#progress'+this._id).html(""+(evt.loaded / evt.total * 100));		
		//$('#progress'+that._id).parent().remove();
	},
	'dropHandler': function(file, id) {
		$(Uploader._options.uploaderlist+' > ul').append('<li>Caricamento '+file.name+': <span id="progress'+id+'">0</span>% </li>');
		reader = new FileReader();
		reader.onload = Uploader._options.fileHandler;
		reader.readAsDataURL(file);
	},
	'fileHandler': function(e) {
		$(Uploader._options.imagepreview).attr('src', e.target.result);
	}
};

Uploader.noopHandler = function(evt) {
	evt.stopPropagation();
	evt.preventDefault();
};

Uploader.init = function(options) {
	jQuery.extend(Uploader._options, options);

	$(Uploader._options.uploaderlist).append('<ul></ul>');

	$(function(){
		droparea = document.getElementById(Uploader._options.droparea);
		droparea.addEventListener("mouseover", function(evt) {
			Uploader.noopHandler(evt);		
		}, false);
		droparea.addEventListener("dragenter", function(evt) {
			$(droparea).css({'opacity': '.5'});
			Uploader.noopHandler(evt);
		}, false);
		droparea.addEventListener("dragexit", function(evt) {
			$(droparea).css({'opacity': '1'});
			Uploader.noopHandler(evt);
		}, false);
		droparea.addEventListener("dragover", function(evt) {
			Uploader.noopHandler(evt);
		}, false);
		droparea.addEventListener("drop", function(evt) {
			$(droparea).css({'opacity': '1'});
			Uploader.noopHandler(evt);

			var files = evt.dataTransfer.files;
			var count = files.length;
 			if (count == 0) return false;

			for (i=0; i<files.length; i++) {
				formData = new FormData()
				formData.append('uploaderVersion', '0.1');
				formData.append('postfile', files[i]);

				xhr = new XMLHttpRequest();
				xhr._id = i+0;
				xhr.open('POST', Uploader._options.url, true);
				xhr.onprogress = Uploader._options.progressHandler
				xhr.onload = Uploader._options.loadHandler
				xhr.send(formData);

				Uploader._options.dropHandler(files[i], i);

				if (Uploader._options.multiple == false) return false;
			}
		}, false);
	});
};
