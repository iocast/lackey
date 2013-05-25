
var TableViewer = Class.extend({
                               visual : null,
                               construct : function(visual) {
                               this.visual = visual;
                               },
                               refresh : function() {
                               this.visual.options.callbacks.search(this.visual.searchBox.currentQuery, this.visual.searchQuery);
                               }
                               });

$(function(){
  
  /* Twitter Boostrap Tabular activation */
  $('.nav-tabs a').click(function (e) {
                         e.preventDefault();
                         $(this).tab('show');
                         })
  
  /* datetime picker */
  $('div .datetime').datetimepicker({
                                    format: 'MM/dd/yyyy HH:mm:ss PP',
                                    maskInput: false,
                                    language: 'en',
                                    pick12HourFormat: true
                                    });
  
  /* Twitter Bootstrap Tooltip */
  $('[rel=tooltip]').tooltip();
  
  });
