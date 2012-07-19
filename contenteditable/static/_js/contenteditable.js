// Content editable support

$(function(){
  // function enableEditbox
  // turns design mode on for editable elements
  // this: the box element that contains all the editable elements
  function enableEditbox(){
    var self = this;
    $(self).addClass('ui-editbox-active')
    .find('[data-editfield]:not(.locked)')
    .attr('contenteditable', 'true')
    .off('.editbox');
    // FIXME remove hack once we get real ui for determining when we're done
    $(document).on('click.editbox', function(evt){
      if (!$(evt.target).closest('.ui-editbox-active').length) {
        try {
          saveEditbox.call(self, evt);
        } catch (e){
          disableEditbox.call(self);
          console.warn(e);
        }
        $(document).off('.editbox');
      }
    });
  }


  // function disableEditbox
  // turns design mode off for editable elements
  // this: the box element that contains all the editable elements
  function disableEditbox(){
    $(this).removeClass('ui-editbox-active')
    .find('[contentEditable]')
    .removeAttr('contenteditable');
  }


  // function saveEditbox
  // this: the box element that contains all the editable elements
  function saveEditbox(){
    var $box = $(this),
        data = $box.data(),
        pk = data.editpk,
        save_data = {};
    if (!data.editmodel){
      throw "missingModel";
    }
    if (pk){
      save_data.pk = pk;
    } else if (data.editslug) {
      save_data.slug = data.editslug;
      if (data.editslugfield){
        save_data.slugfield = data.editslugfield;
      }
    } else {
      throw "missingPK";
    }
    var editables = $box.find('[data-editfield]');
    if (editables.length) {
      editables.each(function (_, el) {
        var name = $(el).attr('data-editfield');
        if (name) {
          save_data[name] = el.innerHTML;
        }
      });
    } else if (data.editfield) {
      save_data[data.editfield] = $.trim($box.html());
    } else {
      throw "missingData";
    }
    if (pk !== -1) {
      $contentEditable.save(data.editmodel, save_data);
    } else {
      $contentEditable.insert(data.editmodel, save_data, function(data) {
        $box.attr('data-editpk', data.pk);
      });
    }
    disableEditbox.call(this);
  }

  $('.clearonclick').click(function() {
    if ($(this).html()==$(this).attr('data-placeholder')) {
      $(this).html('');
    }
  }).blur(function () {
    if ($(this).html() === '') {
      $(this).html($(this).attr('data-placeholder'));
    }
  }).each(function (_, el1){
    if ($(el1).html().trim() === '') {
      $(el1).html($(this).attr('data-placeholder'));
    }
  });

  // not an efficient selector but makes this easier to implement in the templates
  $('[data-editpk], [data-editslug]').addClass('ui-editbox').on('dblclick', enableEditbox);

  $('.returnsaves').each(function (_, el) {
    $(el).keypress(function(event) {
      var keycode = (event.keyCode ? event.keyCode : event.which);
      if (keycode=='13') {
        $(el).blur();
        return false;
      }
    });
  });

  $('.editableitem').each(function (_, el) {
    $(el).attr('contenteditable', 'true');
    $(el).css({'border':'1px dotted red'});
    $.setEventHandler('blur', el, function() { reloadPage($(el).attr('data-redirect')); });
  });

  $('.clickitem').each(function (_, el) {
    $.setEventHandler('click', el, function() { reloadPage(); });
  });

  $('.reloadbutton').each(function (_, el) {
    $(el).click(function() {
      reloadPage();
      return false;
    });
  });

  $('.deletebutton').each(function (_, el) {
    $(el).click(function() {
      if (confirm('Vuoi veramente eliminare questo elemento?')) {
        $contentEditable.delete($(el).attr('data-model'), $(el).attr('data-id'));
      }
      return false;
    });
  });

});

$.setEventHandler = function(ev, el, callback) {
  $(el).bind(ev, function() {
      save_data = {};
      if ($(this).attr('data-value') !== undefined) {
        console.log('Saving with data-value: '+$(this).attr('data-value'));
        save_data[$(this).attr('data-name')] = $(this).attr('data-value');
      } else {
        console.log('Saving with innerHTML: '+$(this).html());
        save_data[$(this).attr('data-name')] = $(this).html();
      }

      if (save_data[$(this).attr('data-name')]!=$(this).attr('data-placeholder')) {
        $contentEditable.save($(this).attr('data-model'), $(this).attr('data-id'), save_data, callback);
      } else {
        console.log('Aborted: not saving an empty album');
      }
      return false;
  });
};

// add csrf to ajax requests
// https://docs.djangoproject.com/en/1.3/ref/contrib/csrf/#upgrading-notesO
$(document).ajaxSend(function(event, xhr, settings) {
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  function sameOrigin(url) {
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
  }
  function safeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
  }
});

$contentEditable = {
  options: {'url': '/contenteditable/update/',
        'deleteurl': '/contenteditable/delete/'},
  init: function (options) {
    jQuery.extend($contentEditable.options, options);
  },
  save: function(model, data, success_callback) {
    console.log("Saving to "+$contentEditable.options['url']);
    console.log(data);

    $.post($contentEditable.options['url'], jQuery.extend(data, {
      'model': model
    }))
    .success(function(response) {
      console.log("Saved: "+response);
    })
    .success(success_callback)
    .error(function() {
      alert("Si è verificato un errore durante il salvataggio. Le modifiche potrebbero non essere state salvate.\nSe il problema persiste ricarica la pagina.");
    });
  },
  insert: function(model, data, success_callback){
    console.log("Inserting to " + $contentEditable.options['url']);
    console.log(data);
    $.ajax({
      type: 'PUT',
      url: $contentEditable.options.url,
      data: jQuery.extend(data, {
        'model': model
      }),
      dataType: 'json'
    })
    .success(function(response) {
      console.log("Saved: " + response);
    })
    .success(success_callback)
    .error(function() {
      alert("Si è verificato un errore durante il salvataggio. Le modifiche potrebbero non essere state salvate.\nSe il problema persiste ricarica la pagina.");
    });
  },
  'delete': function(model, id) {
    console.log("Deleting <"+model+">#"+id);
    $.post($contentEditable.options['deleteurl'], {
      'model': model,
      'id': id
    })
    .success(function(response) {
      console.log("Deleted: "+response);
      document.location.reload();
    })
    .error(function() {
      alert("Impossibile eliminare l'elemento richiesto. La pagina verrà ricaricata.");
    });
  }
};


reloadPage = function(url) {
  if (url) {
    document.location.href=url;
  } else {
    document.location.reload();
  }
};
