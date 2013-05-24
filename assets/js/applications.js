
$(function(){
  
  /* tablesorter plugin */
  
  var searchRequest = null;
  var facetValues = [{value:'name', label:'name'}, {value:'command', label: 'command'}, {value: 'project_id', label: 'project'}];
  var valueMatches = {};
  
  valueMatches['project_id'] = [];
  $.ajax({
         type: 'GET',
         url: base_path + 'api/project/list',
         dataType: 'json',
         async: false,
         success: function(data) {
         $.each(data, function(key, val) {
                valueMatches.project_id.push({ value: "" + val.id, label: val.name});
                });
         }
         });
  
  
  $(".tablesorter").tablesorter({
                                headers: { 6: { sorter: false} }
                                });
  
  var visualSearch = VS.init({
                             container  : $('#search-box-container'),
                             query      : '',
                             minLength  : 0,
                             showFacets : true,
                             unquotable : [
                                           'project'
                                           ],
                             placeholder : "Search for ...",
                             callbacks  : {
                             search : function(query, searchCollection) {
                             if(searchRequest != null) { searchRequest.abort(); }
                             
                             if (query.length <= 0) {
                             $('#search-result-table tbody').empty();
                             $('#search-result-table').trigger("update");
                             } else {
                             
                             searchRequest = $.ajax({
                                                    type: 'GET',
                                                    url: base_path + 'api/application/search',
                                                    dataType: 'json',
                                                    data: {q:searchCollection.serialize()},
                                                    success: function(data) {
                                                    
                                                    var tblBody = $('#search-result-table tbody').empty();
                                                    var tmpl = '<tr><td>{project_name}</td><td>{name}</td><td>{description}</td><td>{project_directory}<b>{directory}</b></td><td>{command}</td>' +
                                                    '<td>' +
                                                    '<a href="#" name="application-lst-run-btn"data-id="{id}"><span class="icon-tasks">&nbsp;</span></a>' +
                                                    '<a href="#" name="application-lst-edit-btn" data-toggle="modal" data-id="{id}"><span class="icon-edit">&nbsp;</span></a>' +
                                                    '<a href="#" name="application-lst-delete-btn" data-id="{id}"><span class="icon-remove">&nbsp;</span></a>' +
                                                    '<a href="#" name="application-lst-schedule-btn" data-id="{id}"><span class="icon-play">&nbsp;</span></a>' +
                                                    '</td></tr>';
                                                    
                                                    for(var i = 0; i < data.length; i++) {
                                                    tblBody.append($(tmpl).nano(data[i]));
                                                    }
                                                    
                                                    $('a[name="application-lst-delete-btn"]').click(function(event) {
                                                                                                    $.ajax({
                                                                                                           type: 'DELETE',
                                                                                                           url: base_path + 'api/application/' + $(this).attr("data-id"),
                                                                                                           success: function(data, status, xhr) {
                                                                                                           search.refresh();
                                                                                                           },
                                                                                                           error: function(xhr, status, error) { }
                                                                                                           });
                                                                                                    return false;
                                                                                                    });
                                                    
                                                    $('a[name="application-lst-edit-btn"]').click(function(event) {
                                                                                                  $($('#application-edit form span[name="id"]')[0]).text($(this).attr("data-id"));
                                                                                                  $('#application-edit').modal('show');
                                                                                                  });
                                                    
                                                    $('a[name="application-lst-run-btn"]').click(function(event) {
                                                                                                 window.location = "/runs?q=" + encodeURIComponent('application_id: "' + $(this).attr("data-id") + '"');
                                                                                                 return false;
                                                                                                 });
                                                    $('a[name="application-lst-schedule-btn"]').click(function(event) {
                                                                                                      $($('#application-schedule form span[name="id"]')[0]).text($(this).attr("data-id"));
                                                                                                      $('#application-schedule').modal('show');
                                                                                                      });
                                                    $('#search-result-table').trigger("update");
                                                    
                                                    }
                                                    });
                             }
                             },
                             valueMatches : function(category, searchTerm, callback) {
                             callback(valueMatches[category]);
                             },
                             facetMatches : function(callback) {
                             callback(facetValues, {preserveOrders: true});
                             
                             }
                             }
                             });
  
  
  
  
  search = new TableViewer(visualSearch);
  
  });
