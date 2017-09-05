/**
 * Resize function without multiple trigger
 *
 * Usage:
 * $(window).smartresize(function(){
 *     // code here
 * });
 */
(function($,sr){
    // debouncing function from John Hann
    // http://unscriptable.com/index.php/2009/03/20/debouncing-javascript-methods/
    var debounce = function (func, threshold, execAsap) {
      var timeout;

        return function debounced () {
            var obj = this, args = arguments;
            function delayed () {
                if (!execAsap)
                    func.apply(obj, args);
                timeout = null;
            }

            if (timeout)
                clearTimeout(timeout);
            else if (execAsap)
                func.apply(obj, args);

            timeout = setTimeout(delayed, threshold || 100);
        };
    };

    // smartresize
    jQuery.fn[sr] = function(fn){  return fn ? this.bind('resize', debounce(fn)) : this.trigger(sr); };

})(jQuery,'smartresize');
/**
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

var CURRENT_URL = window.location.href.split('#')[0].split('?')[0],
    $BODY = $('body'),
    $MENU_TOGGLE = $('#menu_toggle'),
    $SIDEBAR_MENU = $('#sidebar-menu'),
    $SIDEBAR_FOOTER = $('.sidebar-footer'),
    $LEFT_COL = $('.left_col'),
    $RIGHT_COL = $('.right_col'),
    $NAV_MENU = $('.nav_menu'),
    $FOOTER = $('footer');

// Sidebar
function init_sidebar() {
var setContentHeight = function () {
	// reset height
	$RIGHT_COL.css('min-height', $(window).height());

	var bodyHeight = $BODY.outerHeight(),
		footerHeight = $BODY.hasClass('footer_fixed') ? -10 : $FOOTER.height(),
		leftColHeight = $LEFT_COL.eq(1).height() + $SIDEBAR_FOOTER.height(),
		contentHeight = bodyHeight < leftColHeight ? leftColHeight : bodyHeight;

	// normalize content
	contentHeight -= $NAV_MENU.height() + footerHeight;

	$RIGHT_COL.css('min-height', contentHeight);
};

  $SIDEBAR_MENU.find('a').on('click', function(ev) {
	  //console.log('clicked - sidebar_menu');
        var $li = $(this).parent();

        if ($li.is('.active')) {
            $li.removeClass('active active-sm');
            $('ul:first', $li).slideUp(function() {
                setContentHeight();
            });
        } else {
            // prevent closing menu if we are on child menu
            if (!$li.parent().is('.child_menu')) {
                $SIDEBAR_MENU.find('li').removeClass('active active-sm');
                $SIDEBAR_MENU.find('li ul').slideUp();
            }else
            {
				if ( $BODY.is( ".nav-sm" ) )
				{
					$SIDEBAR_MENU.find( "li" ).removeClass( "active active-sm" );
					$SIDEBAR_MENU.find( "li ul" ).slideUp();
				}
			}
            $li.addClass('active');

            $('ul:first', $li).slideDown(function() {
                setContentHeight();
            });
        }
    });

// toggle small or large menu
$MENU_TOGGLE.on('click', function() {
		if ($BODY.hasClass('nav-md')) {
			$SIDEBAR_MENU.find('li.active ul').hide();
			$SIDEBAR_MENU.find('li.active').addClass('active-sm').removeClass('active');
		} else {
			$SIDEBAR_MENU.find('li.active-sm ul').show();
			$SIDEBAR_MENU.find('li.active-sm').addClass('active').removeClass('active-sm');
		}

	$BODY.toggleClass('nav-md nav-sm');

	setContentHeight();
});

	// check active menu
	$SIDEBAR_MENU.find('a[href="' + CURRENT_URL + '"]').parent('li').addClass('current-page');

	$SIDEBAR_MENU.find('a').filter(function () {
		return this.href == CURRENT_URL;
	}).parent('li').addClass('current-page').parents('ul').slideDown(function() {
		setContentHeight();
	}).parent().addClass('active');

	// recompute content when resizing
	$(window).smartresize(function(){
		setContentHeight();
	});

	setContentHeight();

	// fixed sidebar
	if ($.fn.mCustomScrollbar) {
		$('.menu_fixed').mCustomScrollbar({
			autoHideScrollbar: true,
			theme: 'minimal',
			mouseWheel:{ preventDefault: true }
		});
	}
};
// /Sidebar


// Panel toolbox
$(document).ready(function() {
    $('.collapse-link').on('click', function() {
        var $BOX_PANEL = $(this).closest('.x_panel'),
            $ICON = $(this).find('i'),
            $BOX_CONTENT = $BOX_PANEL.find('.x_content');

        // fix for some div with hardcoded fix class
        if ($BOX_PANEL.attr('style')) {
            $BOX_CONTENT.slideToggle(200, function(){
                $BOX_PANEL.removeAttr('style');
            });
        } else {
            $BOX_CONTENT.slideToggle(200);
            $BOX_PANEL.css('height', 'auto');
        }

        $ICON.toggleClass('fa-chevron-up fa-chevron-down');
    });

    $('.close-link').click(function () {
        var $BOX_PANEL = $(this).closest('.x_panel');

        $BOX_PANEL.remove();
    });
});
// /Panel toolbox

// Tooltip
$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip({
        container: 'body'
    });
});
// /Tooltip

// Progressbar
if ($(".progress .progress-bar")[0]) {
    $('.progress .progress-bar').progressbar();
}
// /Progressbar

// Switchery
$(document).ready(function() {
    if ($(".js-switch")[0]) {
        var elems = Array.prototype.slice.call(document.querySelectorAll('.js-switch'));
        elems.forEach(function (html) {
            var switchery = new Switchery(html, {
                color: '#26B99A'
            });
        });
    }
});
// /Switchery


// Table
$('table input').on('ifChecked', function () {
    checkState = '';
    $(this).parent().parent().parent().addClass('selected');
    countChecked();
});
$('table input').on('ifUnchecked', function () {
    checkState = '';
    $(this).parent().parent().parent().removeClass('selected');
    countChecked();
});

var checkState = '';

$('.bulk_action input').on('ifChecked', function () {
    checkState = '';
    $(this).parent().parent().parent().addClass('selected');
    countChecked();
});
$('.bulk_action input').on('ifUnchecked', function () {
    checkState = '';
    $(this).parent().parent().parent().removeClass('selected');
    countChecked();
});
$('.bulk_action input#check-all').on('ifChecked', function () {
    checkState = 'all';
    countChecked();
});
$('.bulk_action input#check-all').on('ifUnchecked', function () {
    checkState = 'none';
    countChecked();
});

function countChecked() {
    if (checkState === 'all') {
        $(".bulk_action input[name='table_records']").iCheck('check');
    }
    if (checkState === 'none') {
        $(".bulk_action input[name='table_records']").iCheck('uncheck');
    }

    var checkCount = $(".bulk_action input[name='table_records']:checked").length;

    if (checkCount) {
        $('.column-title').hide();
        $('.bulk-actions').show();
        $('.action-cnt').html(checkCount + ' Records Selected');
    } else {
        $('.column-title').show();
        $('.bulk-actions').hide();
    }
}

// Accordion
$(document).ready(function() {
    $(".expand").on("click", function () {
        $(this).next().slideToggle(200);
        $expand = $(this).find(">:first-child");

        if ($expand.text() == "+") {
            $expand.text("-");
        } else {
            $expand.text("+");
        }
    });
});

// NProgress
if (typeof NProgress != 'undefined') {
    $(document).ready(function () {
        NProgress.start();
    });

    $(window).load(function () {
        NProgress.done();
    });
}

	  //hover and retain popover when on popover content
        var originalLeave = $.fn.popover.Constructor.prototype.leave;
        $.fn.popover.Constructor.prototype.leave = function(obj) {
          var self = obj instanceof this.constructor ?
            obj : $(obj.currentTarget)[this.type](this.getDelegateOptions()).data('bs.' + this.type);
          var container, timeout;

          originalLeave.call(this, obj);

          if (obj.currentTarget) {
            container = $(obj.currentTarget).siblings('.popover');
            timeout = self.timeout;
            container.one('mouseenter', function() {
              //We entered the actual popover – call off the dogs
              clearTimeout(timeout);
              //Let's monitor popover content instead
              container.one('mouseleave', function() {
                $.fn.popover.Constructor.prototype.leave.call(self, self);
              });
            });
          }
        };

        $('body').popover({
          selector: '[data-popover]',
          trigger: 'click hover',
          delay: {
            show: 50,
            hide: 400
          }
        });

		/* DATA TABLES */
			function init_DataTables(response) {

				//console.log('run_datatables');

				if( typeof ($.fn.DataTable) === 'undefined'){ return; }
				//console.log('init_DataTables');

				var handleDataTableButtons = function() {
				  if ($("#datatable-buttons").length) {
					$("#datatable-buttons").DataTable({
					  dom: "Bfrtip",
					  buttons: [
						{
						  extend: "copy",
						  className: "btn-sm"
						},
						{
						  extend: "csv",
						  className: "btn-sm"
						},
						{
						  extend: "excel",
						  className: "btn-sm"
						},
						{
						  extend: "pdfHtml5",
						  className: "btn-sm"
						},
						{
						  extend: "print",
						  className: "btn-sm"
						},
					  ],
					  responsive: true
					});
				  }
				};

				TableManageButtons = function() {
				  "use strict";
				  return {
					init: function() {
					  handleDataTableButtons();
					}
				  };
				}();

				$('#datatable').dataTable();

				$('#datatable-keytable').DataTable({
				  keys: true
				});

				$('#datatable-responsive').DataTable();

				$('#datatable-scroller').DataTable({
          deferRender: true,
				  scrollY: 380,
				  scrollCollapse: true,
				  scroller: true
				});

        var dataRaw = JSON.stringify(response);
        dataSet = [
          ['1', 'script-src', response['script-src']],
          ['2', 'base-uri', response['base-uri']],
          ['3', 'default-src', response['default-src']],
          ['4', 'object-src', response['object-src']],
          ['5', 'style-src', response['style-src']],
          ['6', 'img-src', response['img-src']],
          ['7', 'media-src', response['media-src']],
          ['8', 'frame-src', response['frame-src']],
          ['9', 'child-src', response['child-src']],
          ['10', 'frame-ancestors', response['frame-ancestors']],
          ['11', 'font-src', response['font-src']],
          ['12', 'connect-src', response['connect-src']],
          ['13', 'manifest-src', response['manifest-src']],
          ['14', 'form-action', response['form-action']],
          ['15', 'sandbox', response['sandbox']],
          ['16', 'script-nonce', response['script-nonce']],
          ['17', 'plugin-type', response['plugin-types']],
          ['18', 'reflected-xss', response['reflected-xss']],
          ['19', 'block-all-mixed-content', response['block-all-mixed-content']],
          ['20', 'upgrade-insecure-requests', response['upgrade-insecure-requests']],
          ['21', 'referrer', response['referrer']],
          ['22', 'report-uri', response['report-uri']],
          ['23', 'report-to', response['report-to']]
        ]
        $('#example').DataTable({
          "data": dataSet
        });

				$('#datatable-fixed-header').DataTable({
				  fixedHeader: true
				});

				var $datatable = $('#datatable-checkbox');

				$datatable.dataTable({
				  'order': [[ 1, 'asc' ]],
				  'columnDefs': [
					{ orderable: false, targets: [0] }
				  ]
				});
				$datatable.on('draw.dt', function() {
				  $('checkbox input').iCheck({
					checkboxClass: 'icheckbox_flat-green'
				  });
				});

/*        $(document).ready(function() {
            $datatable.DataTable( {
                "iDisplayLength": 5,
                "autoWidth": true,
                "responsive": true,
                "info": false,
                "searching": false,
                "bLengthChange": false,
                "ajax": response
            } );
        } );*/

				TableManageButtons.init();

			};

		/* ECHRTS */
		function init_echarts() {

				if( typeof (echarts) === 'undefined'){ return; }
				  var theme = {
				  color: [
					  '#26B99A', '#34495E', '#BDC3C7', '#3498DB',
					  '#9B59B6', '#8abb6f', '#759c6a', '#bfd3b7'
				  ],

				  title: {
					  itemGap: 8,
					  textStyle: {
						  fontWeight: 'normal',
						  color: '#408829'
					  }
				  },

				  dataRange: {
					  color: ['#1f610a', '#97b58d']
				  },

				  toolbox: {
					  color: ['#408829', '#408829', '#408829', '#408829']
				  },

				  tooltip: {
					  backgroundColor: 'rgba(0,0,0,0.5)',
					  axisPointer: {
						  type: 'line',
						  lineStyle: {
							  color: '#408829',
							  type: 'dashed'
						  },
						  crossStyle: {
							  color: '#408829'
						  },
						  shadowStyle: {
							  color: 'rgba(200,200,200,0.3)'
						  }
					  }
				  },

				  dataZoom: {
					  dataBackgroundColor: '#eee',
					  fillerColor: 'rgba(64,136,41,0.2)',
					  handleColor: '#408829'
				  },
				  grid: {
					  borderWidth: 0
				  },

				  categoryAxis: {
					  axisLine: {
						  lineStyle: {
							  color: '#408829'
						  }
					  },
					  splitLine: {
						  lineStyle: {
							  color: ['#eee']
						  }
					  }
				  },

				  valueAxis: {
					  axisLine: {
						  lineStyle: {
							  color: '#408829'
						  }
					  },
					  splitArea: {
						  show: true,
						  areaStyle: {
							  color: ['rgba(250,250,250,0.1)', 'rgba(200,200,200,0.1)']
						  }
					  },
					  splitLine: {
						  lineStyle: {
							  color: ['#eee']
						  }
					  }
				  },
				  timeline: {
					  lineStyle: {
						  color: '#408829'
					  },
					  controlStyle: {
						  normal: {color: '#408829'},
						  emphasis: {color: '#408829'}
					  }
				  },

				  k: {
					  itemStyle: {
						  normal: {
							  color: '#68a54a',
							  color0: '#a9cba2',
							  lineStyle: {
								  width: 1,
								  color: '#408829',
								  color0: '#86b379'
							  }
						  }
					  }
				  },
				  map: {
					  itemStyle: {
						  normal: {
							  areaStyle: {
								  color: '#ddd'
							  },
							  label: {
								  textStyle: {
									  color: '#c12e34'
								  }
							  }
						  },
						  emphasis: {
							  areaStyle: {
								  color: '#99d2dd'
							  },
							  label: {
								  textStyle: {
									  color: '#c12e34'
								  }
							  }
						  }
					  }
				  },
				  force: {
					  itemStyle: {
						  normal: {
							  linkStyle: {
								  strokeColor: '#408829'
							  }
						  }
					  }
				  },
				  chord: {
					  padding: 4,
					  itemStyle: {
						  normal: {
							  lineStyle: {
								  width: 1,
								  color: 'rgba(128, 128, 128, 0.5)'
							  },
							  chordStyle: {
								  lineStyle: {
									  width: 1,
									  color: 'rgba(128, 128, 128, 0.5)'
								  }
							  }
						  },
						  emphasis: {
							  lineStyle: {
								  width: 1,
								  color: 'rgba(128, 128, 128, 0.5)'
							  },
							  chordStyle: {
								  lineStyle: {
									  width: 1,
									  color: 'rgba(128, 128, 128, 0.5)'
								  }
							  }
						  }
					  }
				  },
				  gauge: {
					  startAngle: 225,
					  endAngle: -45,
					  axisLine: {
						  show: true,
						  lineStyle: {
							  color: [[0.2, '#86b379'], [0.8, '#68a54a'], [1, '#408829']],
							  width: 8
						  }
					  },
					  axisTick: {
						  splitNumber: 10,
						  length: 12,
						  lineStyle: {
							  color: 'auto'
						  }
					  },
					  axisLabel: {
						  textStyle: {
							  color: 'auto'
						  }
					  },
					  splitLine: {
						  length: 18,
						  lineStyle: {
							  color: 'auto'
						  }
					  },
					  pointer: {
						  length: '90%',
						  color: 'auto'
					  },
					  title: {
						  textStyle: {
							  color: '#333'
						  }
					  },
					  detail: {
						  textStyle: {
							  color: 'auto'
						  }
					  }
				  },
				  textStyle: {
					  fontFamily: 'Arial, Verdana, sans-serif'
				  }
			  };

			  //echart Bar
			if ($('#mainb').length ){

          $.ajax({
            url: '/pkp_chart',
            data: $('form').serialize(),
            type: 'GET',
            success: function(response){

          var header = document.getElementById('pkp_total');
          while (header.firstChild) {
            header.removeChild(header.firstChild);
          }
          header.appendChild(document.createTextNode(response['total']));
				  var echartBar = echarts.init(document.getElementById('mainb'), theme);

				  echartBar.setOption({
					title: {
					  text: '',
					  subtext: ''
					},
					tooltip: {
					  trigger: 'axis'
					},
					legend: {
					  data: ['pin-sha256', 'max-age', 'includeSubDomains', 'report-uri']
					},
					toolbox: {
					  show: false
					},
					calculable: false,
					xAxis: [{
					  type: 'category',
						data: ['']
					}],
					yAxis: [{
					  type: 'value'
					}],
					series: [{
					  name: 'pin-sha256',
					  type: 'bar',
					  data: [response['pin-sha256']]
					}, {
					  name: 'max-age',
					  type: 'bar',
					  data: [response['max-age']]
					},
					{
					  name: 'includeSubDomains',
					  type: 'bar',
					  data: [response['includeSubDomains']]
					},
					{
					  name: 'report-uri',
					  type: 'bar',
					  data: [response['report-uri']]
					}
					]
				  });
           },
          error: function(error){
            console.log(error);
              }
            });

			}

			   //echart Radar
			if ($('#echart_sonar').length ){

        $.ajax({
          url: '/xss_chart',
          data: $('form').serialize(),
          type: 'GET',
          success: function(response){

        var header = document.getElementById('xss_total');
        while (header.firstChild) {
          header.removeChild(header.firstChild);
        }
        header.appendChild(document.createTextNode(response['total']));
			  var echartRadar = echarts.init(document.getElementById('echart_sonar'), theme);

			  echartRadar.setOption({
				title: {
				  text: '',
				  subtext: ''
				},
				 tooltip: {
					trigger: 'item'
				},
				legend: {
				  orient: 'vertical',
				  x: 'right',
				  y: 'bottom',
				  data: ['']
				},
				toolbox: {
				  show: true,
				  feature: {
					restore: {
					  show: true,
					  title: "Restore"
					},
					saveAsImage: {
					  show: true,
					  title: "Save Image"
					}
				  }
				},
				polar: [{
				  indicator: [{
					text: '0',
					max: 10838
				  }, {
					text: '0; mode=block',
					max: 10838
				  }, {
					text: '1',
					max: response['1']
				  }, {
					text: '1; mode=block',
					max: 10838
				  }, {
					text: 'report',
					max: 10838
				  }, {
					text: 'other',
					max: 10838
				  }]
				}],
				calculable: true,
				series: [{
				  name: '',
				  type: 'radar',
				  data: [{
					value: [
            response['0'],
            response['0-mode-block'],
            response['1'],
            response['1-mode-block'],
            response['report'],
            response['other']
          ],
					name: ''
				  }]
				}]
			  });
          // end ajax
        },
          error: function(error){
            console.log(error);
            }
          });

			}

	   //echart Pie Collapse
			if ($('#xfo').length ){

        $.ajax({
          url: '/xfo_chart',
          data: $('form').serialize(),
          type: 'GET',
          success: function(response){

        var header = document.getElementById('xfo_total');
        while (header.firstChild) {
          header.removeChild(header.firstChild);
        }
        header.appendChild(document.createTextNode(response['total']));
			  var echartPieCollapse = echarts.init(document.getElementById('xfo'), theme);

			  echartPieCollapse.setOption({
				tooltip: {
				  trigger: 'item',
				  formatter: "{a} <br/>{b} : {c} ({d}%)"
				},
				legend: {
				  x: 'center',
				  y: 'bottom',
				  data: ['deny', 'sameorigin', 'allow-from <uri>', 'other']
				},
				toolbox: {
				  show: true,
				  feature: {
					magicType: {
					  show: true,
					  type: ['pie', 'funnel']
					},
					restore: {
					  show: true,
					  title: "Restore"
					},
					saveAsImage: {
					  show: true,
					  title: "Save Image"
					}
				  }
				},
				calculable: true,
				series: [{
				  name: 'x-frame-options',
				  type: 'pie',
				  radius: [25, 90],
				  center: ['50%', 170],
				  roseType: 'area',
				  x: '50%',
				  max: 40,
				  sort: 'ascending',
				  data: [{
					value: response['deny'],
					name: 'deny'
				  }, {
					value: response['sameorigin'],
					name: 'sameorigin'
				  }, {
					value: response['allow-from'],
					name: 'allow-from <uri>'
				  }, {
					value: response['other'],
					name: 'other'
				  }]
				}]
			  });
        },
        error: function(error){
          console.log(error);
            }
          });

			}

			//echart Donut
			if ($('#xcto_donut').length ){

        $.ajax({
          url: '/xcto_chart',
          data: $('form').serialize(),
          type: 'GET',
          success: function(response){

        var header = document.getElementById('xcto_total');
        while (header.firstChild) {
          header.removeChild(header.firstChild);
        }
        header.appendChild(document.createTextNode(response['total']));
			  var echartDonut = echarts.init(document.getElementById('xcto_donut'), theme);

			  echartDonut.setOption({
				tooltip: {
				  trigger: 'item',
				  formatter: "{a} <br/>{b} : {c} ({d}%)"
				},
				calculable: true,
				legend: {
				  x: 'center',
				  y: 'bottom',
				  data: ['nosniff', 'other']
				},
				toolbox: {
				  show: true,
				  feature: {
					magicType: {
					  show: true,
					  type: ['pie', 'funnel'],
					  option: {
						funnel: {
						  x: '25%',
						  width: '50%',
						  funnelAlign: 'center',
						  max: 1548
						}
					  }
					},
					restore: {
					  show: true,
					  title: "Restore"
					},
					saveAsImage: {
					  show: true,
					  title: "Save Image"
					}
				  }
				},
				series: [{
				  name: 'x-content-type-options',
				  type: 'pie',
				  radius: ['35%', '55%'],
				  itemStyle: {
					normal: {
					  label: {
						show: true
					  },
					  labelLine: {
						show: true
					  }
					},
					emphasis: {
					  label: {
						show: true,
						position: 'center',
						textStyle: {
						  fontSize: '14',
						  fontWeight: 'normal'
						}
					  }
					}
				  },
				  data: [{
					value: response['nosniff'],
					name: 'nosniff'
				  }, {
          value: response['other'],
					name: 'other'
          }]
				}]
			  });
        },
        error: function(error){
          console.log(error);
            }
          });
      }

      //echart Pie
      if ($('#echart_pie').length ){

        $.ajax({
          url: '/sts_chart',
          data: $('form').serialize(),
          type: 'GET',
          success: function(response){

        var header = document.getElementById('sts_total');
        while (header.firstChild) {
          header.removeChild(header.firstChild);
        }
        header.appendChild(document.createTextNode(response['total']));
        var echartPie = echarts.init(document.getElementById('echart_pie'), theme);

        echartPie.setOption({
        tooltip: {
          trigger: 'item',
          formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
          x: 'center',
          y: 'bottom',
          data: ['max-age', 'includeSubDomains']
        },
        toolbox: {
          show: true,
          feature: {
          magicType: {
            show: true,
            type: ['pie', 'funnel'],
            option: {
            funnel: {
              x: '25%',
              width: '50%',
              funnelAlign: 'left',
              max: 140
            }
            }
          },
          restore: {
            show: true,
            title: "Restore"
          },
          saveAsImage: {
            show: true,
            title: "Save Image"
          }
          }
        },
        calculable: true,
        series: [{
          name: 'header option:',
          type: 'pie',
          radius: '55%',
          center: ['50%', '48%'],
          data: [{
          value: response['max-age'],
          name: 'max-age'
          }, {
          value: response['includeSubDomains'],
          name: 'includeSubDomains'
          }]
        }]
        });

        var dataStyle = {
        normal: {
          label: {
          show: false
          },
          labelLine: {
          show: false
          }
        }
        };

        var placeHolderStyle = {
        normal: {
          color: 'rgba(0,0,0,0)',
          label: {
          show: false
          },
          labelLine: {
          show: false
          }
        },
        emphasis: {
          color: 'rgba(0,0,0,0)'
        }
        };
      },
      error: function(error){
        console.log(error);
          }
        });
    }

    //echart Line
    if ($('#echart_line').length ){

      $.ajax({
        url: '/csp_chart',
        data: $('form').serialize(),
        type: 'GET',
        success: function(response){

      var header = document.getElementById('csp_total');
      while (header.firstChild) {
        header.removeChild(header.firstChild);
      }
      header.appendChild(document.createTextNode(response['total']));
      // table: csp-options value
      init_DataTables(response);
      var echartLine = echarts.init(document.getElementById('echart_line'), theme);

      echartLine.setOption({
      title: {
        text: '',
        subtext: ''
      },
      tooltip: {
        trigger: 'axis'
      },
      legend: {
        x: 220,
        y: 40,
        data: ['Q1']
      },
      toolbox: {
        show: true,
        feature: {
        magicType: {
          show: true,
          title: {
          line: 'Line',
          bar: 'Bar',
          stack: 'Stack',
          tiled: 'Tiled'
          },
          type: ['line', 'bar', 'stack', 'tiled']
        },
        restore: {
          show: true,
          title: "Restore"
        },
        saveAsImage: {
          show: true,
          title: "Save Image"
        }
        }
      },
      calculable: true,
      xAxis: [{
        type: 'category',
        boundaryGap: false,
        data: [
          'script-src',
          'base-uri',
          'default-src',
          'object-src',
          'style-src',
          'img-src',
          'media-src',
          'frame-src',
          'child-src',
          'frame-ancestors',
          'font-src',
          'connect-src',
          'manifest-src',
          'form-action',
          'sandbox',
          'script-nonce',
          'plugin-types',
          'reflected-xss',
          'block-all-mixed-content',
          'upgrade-insecure-requests',
          'referrer',
          'report-uri',
          'report-to'
        ]
      }],
      yAxis: [{
        type: 'value'
      }],
      series: [{
        name: 'Q1',
        type: 'line',
        smooth: true,
        itemStyle: {
        normal: {
          areaStyle: {
          type: 'default'
          }
        }
        },
        data: [
          response['script-src'],
          response['base-uri'],
          response['default-src'],
          response['object-src'],
          response['style-src'],
          response['img-src'],
          response['media-src'],
          response['frame-src'],
          response['child-src'],
          response['frame-ancestors'],
          response['font-src'],
          response['connect-src'],
          response['manifest-src'],
          response['form-action'],
          response['sandbox'],
          response['script-nonce'],
          response['plugin-types'],
          response['reflected-xss'],
          response['block-all-mixed-content'],
          response['upgrade-insecure-requests'],
          response['referrer'],
          response['report-uri'],
          response['report-to']
        ]
      }]
      });
      },
      error: function(error){
        console.log(error);
            }
          });
    }

    }

	$(document).ready(function() {

		init_sidebar();
		init_echarts();
		//init_DataTables();

	});
