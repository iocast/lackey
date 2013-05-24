
$(function(){
  
  /* tablesorter plugin */
  
  var searchRequest = null;
  var facetValues = [{value:'name', label:'name'}, {value:'title', label: 'title'}];
  var valueMatches = {};
  
  
  
  $(".tablesorter").tablesorter({
                                headers: { 6: { sorter: false} }
                                });
  
  var visualSearch = VS.init({
                             container  : $('#search-box-container'),
                             query      : '',
                             minLength  : 0,
                             showFacets : true,
                             unquotable : [
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
                                                    url: base_path + 'api/project/search',
                                                    dataType: 'json',
                                                    data: {q:searchCollection.serialize()},
                                                    success: function(data) {
                                                    
                                                    var tblBody = $('#search-result-table tbody').empty();
                                                    var tmpl = '<tr><td>{name}</td><td>{title}</td><td>{directory}</td><td>{description}</td>' +
                                                    '<td>' +
                                                    '<a href="#" name="project-lst-show-btn" data-id="{id}"><span class="icon-leaf">&nbsp;</span></a>' +
                                                    '<a href="#" name="project-lst-edit-btn" data-toggle="modal" data-id="{id}"><span class="icon-edit">&nbsp;</span></a>' +
                                                    '<a href="#" name="project-lst-delete-btn" data-id="{id}"><span class="icon-remove">&nbsp;</span></a>' +
                                                    '</td></tr>';
                                                    
                                                    for(var i = 0; i < data.length; i++) {
                                                    tblBody.append($(tmpl).nano(data[i]));
                                                    }
                                                    
                                                    $('a[name="project-lst-delete-btn"]').click(function(event) {
                                                                                                $.ajax({
                                                                                                       type: 'DELETE',
                                                                                                       url: base_path + 'api/project/' + $(this).attr("data-id"),
                                                                                                       success: function(data, status, xhr) {
                                                                                                       search.refresh();
                                                                                                       },
                                                                                                       error: function(xhr, status, error) { }
                                                                                                       });
                                                                                                return false;
                                                                                                });
                                                    
                                                    $('a[name="project-lst-edit-btn"]').click(function(event) {
                                                                                              $($('#project-edit form span[name="id"]')[0]).text($(this).attr("data-id"));
                                                                                              $('#project-edit').modal('show');
                                                                                              });
                                                    
                                                    $('a[name="project-lst-show-btn"]').click(function(event) {
                                                                                              window.location = "/applications?q=" + encodeURIComponent('project_id: "' + $(this).attr("data-id") + '"');
                                                                                              return false;
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
