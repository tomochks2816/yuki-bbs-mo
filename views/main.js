// オートリンク
function autoLink(str) {
  var regexp_url = /(https?:\/\/[a-zA-Z0-9.\-_@:/~?%&;=+#',()*!]+)/g;
  var regexp_makeLink = function(all, url, h, href) {
    return '<a href="h' + href + '">' + url + '</a>';
  }
  return str.replace(regexp_url, regexp_makeLink);
}

function sendMessage(name, seed, channel, message) {
  if (name=='' || seed=='' || channel=='' || message=='') {
    console.warn('Invalid argument(s).')
  } else {
    $.ajax({
      type: 'POST',
      url: `${localStorage.getItem('instance')}/bbs/result`,
      data: {
        'name': name,
        'seed': seed,
        'message': message,
        'channel': channel
      }
    });
  }
}

// メッセージ送信
function sendMessageByUser() {
  var name = $('#name').val();
  var seed = $('#seed').val();
  var message = $('#message').val();
  var channel = $('#channel').val();
  sendMessage(name, seed, channel, message);
  $('#message').val("");
}

// メッセージ読み込み
var xhr;
function loadMessage() {
  if (xhr && xhr.readyState !== 4) {
    xhr.abort();
  }
  
  var channel = $('#channel').val();
  var filter = $('#verify').prop('checked');

  if (localStorage.getItem('instance') === null) {
    return
  }
  xhr = $.ajax({
    type: 'GET',
    url: '/bbs/api',
    headers: { 'Accept': null },
    xhrFields: {
      withCredentials: true
    },
    data: {
      'channel': channel,
      'verify': filter,
      't': 0
    },
    success: function(data) {
      $('#result').html(data);
      $('table tr').each(function() {
        var firstTd = $(this).find('td:first');
        var content = firstTd.text();
        firstTd.html(`<button class="anchor">${content}</button>`);
      });
      $('.anchor').click(function() {
        var currentMsg = $('#message').val();
        $('#message').val(currentMsg + '>>' + $(this).text() + ' ');
      });
    }
  });
}

// ネットワークコネクション検知
function updateConnectionStatus() {
  var status = $('#status');
  if (navigator.onLine) {
    status.removeClass('offline').addClass('online');
    status.text('online');
  } else {
    status.removeClass('online').addClass('offline');
    status.text('offline');
  }
}

$(document).ready(function() {
  updateConnectionStatus();
  window.addEventListener('online', updateConnectionStatus);
  window.addEventListener('offline', updateConnectionStatus);

  loadMessage();
  
  var selectedChannel = localStorage.getItem('channel');
  if (selectedChannel) {
    $('#channel').val(selectedChannel);
  }
  
  $('#channel').change(function() {
    var newSelectedChannel = $(this).val();
    localStorage.setItem('channel', newSelectedChannel);
    loadMessage();
  });

  var isVerified = localStorage.getItem('verify') === 'true';
  $('#verify').prop('checked', isVerified);

  $('#verify').change(function() {
    var isVerified = $(this).prop('checked');
    localStorage.setItem('verify', isVerified.toString());
    loadMessage();
  });

  var storedName = localStorage.getItem('name');
  var storedSeed = localStorage.getItem('seed');

  if (storedName) {
    $('#name').val(storedName);
  }
  if (storedSeed) {
    $('#seed').val(storedSeed);
  }
  
  $('#name').on('input', function() {
    var newName = $(this).val();
    localStorage.setItem('name', newName);
  });
  $('#seed').on('input', function() {
    var newSeed = $(this).val();
    localStorage.setItem('seed', newSeed);
  });

  loadMessage();
  setInterval(function() {
    loadMessage();
  }, 5000);
});
