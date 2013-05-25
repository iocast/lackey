
$(function(){
  
  /* tablesorter plugin */
  
  var searchRequest = null;
  var facetValues = [{value: 'project_id', label: 'project'}, {value: 'application_id', label: 'application'}];
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
  
  valueMatches['application_id'] = [];
  $.ajax({
         type: 'GET',
         url: base_path + 'api/application/list',
         dataType: 'json',
         async: false,
         success: function(data) {
         $.each(data, function(key, val) {
                valueMatches.application_id.push({ value: "" + val.id, label: val.name});
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
                                           'project',
                                           'application'
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
                                                    url: base_path + 'api/run/search',
                                                    dataType: 'json',
                                                    data: {q:searchCollection.serialize()},
                                                    success: function(data) {
                                                    
                                                    var tblBody = $('#search-result-table tbody').empty();
                                                    var tmpl = '<tr><td>{project_name}</td><td>{application_name}</td><td>{schedule}</td><td>{start}</td><td>{end}</td><td>{duration}</td><td>{directory}</td><td><span rel="tooltip" data-placement="top" data-original-title="{command}">{command_short}</span></td>' +
                                                    '<td><a href="api/run/{id}.raw" target="_blank" rel="tooltip" data-placement="top" data-original-title="opens the shell log in a seperate window">raw log</a></td>' +
                                                    '</tr>';
                                                    
                                                    for(var i = 0; i < data.length; i++) {
                                                    data[i]['command_short'] = data[i].command.trunc(50, true);
                                                    data[i].command = _.escape(data[i].command);

                                                    tblBody.append($(tmpl).nano(data[i]));
                                                    }
                                                    /* reinitialize twitter bootsrap tooltip */
                                                    $('[rel=tooltip]').tooltip();
                                                    
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
