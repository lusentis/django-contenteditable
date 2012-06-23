// Content editable support

$(function(){
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

  $('.editablebox').each(function(_, el) {
    var $box = $(el);
    var app = $box.attr('data-editapp');
    var model = $box.attr('data-editmodel');
    var pk = $box.attr('data-editpk');
    $box.find('[data-editfield]:not(.locked)').each(function (_, el) {
      var $editable = $(el);
      $editable.attr('contenteditable', 'true');
    }).on('blur', function() {
      save_data = {};
      $box.find('[data-editfield]').each(function (_, el2) {
        var name = $(el2).attr('data-editfield');
        if (name) {
          save_data[name] = el2.innerHTML;
        }
      });
      $contentEditable.save(model, pk, save_data, function(data) {
        if (pk == "-1") {
          pk = data;
          $box.attr('data-editpk', pk);
        }
      });
    });
  });

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


$contentEditable = {
  options: {'url': '/contenteditable/update/',
        'deleteurl': '/contenteditable/delete/'},
  init: function (options) {
    jQuery.extend($contentEditable.options, options);
  },
  save: function(model, id, data, success_callback) {
    console.log("Saving to "+$contentEditable.options['url']);
    console.log(data);

    $.post($contentEditable.options['url'], jQuery.extend(data, {
      'model': model,
      'id': id
    }))
    .success(function(response) {
      console.log("Saved: "+response);
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
